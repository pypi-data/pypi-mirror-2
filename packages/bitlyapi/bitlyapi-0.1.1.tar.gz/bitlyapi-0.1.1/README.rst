=====================
Python bit.ly wrapper
=====================

This is a thin Python wrapper for the `bit.ly API`_.  Basic usage looks like
this::

  >>> import bitlyapi
  >>> b = bitlyapi.BitLy(api_user, api_key)
  >>> res = b.shorten(longUrl='http://www.google.com/')
  >>> print res['url']
  'http://bit.ly/6Hwstb'
  >>> print res['long_url']
  'http://www.google.com/'

The return from any method call is a dict containing the results of
decoding the JSON returned from bit.ly.  For example::

  >>> import pprint
  >>> pprint.pprint(res)
  {'global_hash': '2V6CFi',
   'hash': '9gOd4I',
   'long_url': 'http://www.google.com/',
   'new_hash': 1,
   'url': 'http://bit.ly/9gOd4I'}

You can supply arbitrary keywords to method calls and they will be passed
to the `bit.ly API`_::

  >>> res = api.shorten(domain="j.mp", longUrl="http://www.example.com/foobar.html")
  >>> pprint.pprint(res)
  {'global_hash': 'cITxl0',
   'hash': 'cY4460',
   'long_url': 'http://www.example.com/foobar.html',
   'new_hash': 1,
   'url': 'http://j.mp/cY4460'}

.. _bit.ly API: http://code.google.com/p/bitly-api/wiki/ApiDocumentation
