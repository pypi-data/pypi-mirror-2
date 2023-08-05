============
mobi.devices
============

``mobi.devices`` is the set of tools to detect mobile user agents.
It uses `WURFL database <http://wurfl.sourceforce.net>`_ as well as data from
`MIT mobile project <http://m.mit.edu>`_.

It also provides wsgi middlewares that can tag the request with some information
about the devices performing the request.

Run the tests ::

    python setup.py nosetests

