from webob import Request

from mobi.devices.classifiers import MITClassifier, WurflClassifier
from mobi.devices.device import Device
from mobi.caching import Cache
from mobi.interfaces.devices import (
    IBasicDeviceType, IStandardDeviceType, IAdvancedDeviceType)


import logging
import base64
import json

logger = logging.getLogger('mobi.devices.wsgi')

_marker = object()

def serialize_cookie(data):
    return base64.b64encode(json.dumps(data))

def deserialize_cookie(data):
    return json.loads(base64.b64decode(data) or '{}')

class MobiDeviceMiddleware(object):
    """ The middleware aims at detecting devices type from User agents.
    Once found a cookie is set to cache the result for later queries.

    In debugging mode the GET parameter "PARAM_NAME" can be manually set
    to simulate device detection. It can then be disabled by setting it to
    "off".
    """

    cache_engine = Cache(
        namespace=__module__)
    cache = cache_engine.cache

    PARAM_NAME = '__devinfo'

    _mapping = [
        ('advanced', IAdvancedDeviceType),
        ('standard', IStandardDeviceType),
        ('basic', IBasicDeviceType),
    ]

    mapping = dict(_mapping)
    reverse_mapping = dict(map(lambda (a,b,): (b,a,), _mapping))

    def __init__(self, app, debug=False, cookie_max_age=0):
        self.debug = debug
        if self.debug:
            logger.info('MobiDeviceMiddleware start in debug mode.')
        self.app = app
        self.set_cookie_max_age(int(cookie_max_age))
        self.classifiers = [MITClassifier(), WurflClassifier()]

    def __call__(self, environ, start_response):
        request = Request(environ)
        device = self.device_from_get_params(request) or \
            self.device_from_cookie(request) or \
            self.device_from_user_agent(request)

        if device is not None:
            self.set_device_on_request(request, device)

        response = request.get_response(self.app)

        logger.info('device: %s - %s' %
            (device.get_type(), device.get_platform(),))

        if device is not None:
            self.set_device_on_cookie(response, device)

        start_response(response.status,
            [a for a in response.headers.iteritems()])
        return response.app_iter

    def set_cookie_max_age(self, max_age):
        if max_age <= 0:
            self._cookie_max_age = None
        else:
            self._cookie_max_age = max_age

    def set_device_on_request(self, request, device):
        dtype = device.get_type() or IBasicDeviceType
        platform = device.get_platform() or 'computer'

        request.environ['mobi.devices.type'] = \
            self.reverse_mapping[dtype]
        request.environ['mobi.devices.marker'] = dtype
        request.environ['mobi.devices.marker_name'] = dtype.__name__
        request.environ['mobi.devices.platform'] = platform
        if self._is_mobile(platform):
            request.environ['mobi.devices.is_mobile'] = 'yes'

    def _is_mobile(self, platform):
        return platform not in ('computer', 'spider',)

    def device_from_cookie(self, request):
        data = request.cookies.get(self.PARAM_NAME, None)
        if data is not None:
            cookie_val = deserialize_cookie(data)
            dtype = self.mapping.get(cookie_val['type'],
                IBasicDeviceType)
            return Device(request.environ.get('HTTP_USER_AGENT'),
                dtype, platform=cookie_val['platform'])
        return None

    def device_from_get_params(self, request):
        if not self.debug: return None

        param = request.GET.get(self.PARAM_NAME)
        if param == 'off':
            return self.device_from_user_agent(request)

        dtype = self.mapping.get(param)
        platform = request.GET.get(self.PARAM_NAME + '_platform', '')
        if dtype is not None:
            logger.debug('device manually set to %s' % dtype.__name__)
            return Device(request.environ.get('HTTP_USER_AGENT'),
                dtype, platform)
        return None

    def device_from_user_agent(self, request):
        ua = request.environ.get('HTTP_USER_AGENT', '')
        logger.debug("get device from UserAgent: %s" % ua)
        device = self.cache('select_ua:%s' % ua, lambda : self._get_device(ua))
        return device

    def set_device_on_cookie(self, response, device):
        type_val = self.reverse_mapping.get(device.get_type(),
            'basic')
        data = {'type': type_val, 'platform': device.get_platform()}
        encdata = response.request.cookies.get(self.PARAM_NAME)
        if encdata is None or \
                deserialize_cookie(encdata) != data:
            response.set_cookie(self.PARAM_NAME,
                                serialize_cookie(data),
                                max_age=self._cookie_max_age,
                                path='/', secure=False)

    def _get_device(self, ua):
        for classifier in self.classifiers:
            device = classifier(ua)
            if device is not None: return device
        return Device(ua, IBasicDeviceType)


def device_middleware_filter_factory(global_conf, **local_conf):
    def filter(app):
        debug = global_conf.get('debug', False) or \
            local_conf.get('debug', False)
        cookie_max_age = int(local_conf.get('cookie_max_age', 0))
        return MobiDeviceMiddleware(app,
                                          debug=debug,
                                          cookie_max_age=cookie_max_age)
    return filter

