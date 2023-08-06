======
README
======

This package offers a JSON-RPC proxy which can connect to a s01.worker server.


Usage
-----

  >>> from s01.client.proxy import getScrapyProxy

Let's setup a proxy:

  >>> proxy = getScrapyProxy('http://nada')
  >>> proxy.getStartTime()
  Traceback (most recent call last):
  ...
  ResponseError: JSONRPC server connection error.

Of corse, we can't connect to a s01.worker since there is non available.
