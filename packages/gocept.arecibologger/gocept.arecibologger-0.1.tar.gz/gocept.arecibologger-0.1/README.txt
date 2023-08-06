Arecibo is a GAE application that is useful to gather errors from a set of
servers, specifically errors that occur while processing web requests.

gocept.arecibologger is a patch for Zope 2's site error log that will send as
much data (tracebacks, request data, user name, ...) to the Arecibo server as
possible.

How to use
==========

* Install the gocept.arecibologger egg into your Zope 2 runtime environment.
* Activate it by pulling the egg in via ZCML.
* Configure the Arecibo account and server address in your zope.conf::

    <product-config gocept.arecibologger>
        server http://myarecibo.appspot.com/v/1/
        account u8orukajlfdjklafda
    </product-config>
