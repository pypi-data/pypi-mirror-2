Manual
++++++

If you are calling a WSGI application you will need to provide ``environ`` and
``start_response()`` objects as well as pass the result back to the HTTP
service. The ``WSGIService`` provides objects which handle this for you:

``flow.wsgi.environ``
    The WSGI ``environ`` object containing all the request information

``flow.wsgi.start_response()``
    The WSGI ``start_response()`` callable which sets the status and headers

``flow.wsgi.result``
    A list of strings or an iterator which when iterated over, produces the
    response you wish to send. This **must** be set exactly once for the
    result to actually be passed on to Flows. If you set it more than once 
    the previous data will be lost, if you don't set it at all, any data 
    written to the object returned from ``start_response()`` will not be
    passed on to Flows.


The WSGI service then lets you call WSGI applications like this:

::

    flow.wsgi.result = application(
        flow.wsgi.start_response,
        flow.wsgi.environ,
    )

The WSGI application will be called and the correct data will be set up for
``flow.http.response.status``, ``flow.http.response.headers`` and
``flow.http.response.body``.

The ``flow.wsgi.environ`` object has a ``flows.flow`` key representing the
current flow so that the flow can be accessed from within the WSGI
application.

Data written to the writable object returned from ``start_response()`` is
buffered, not streamed, but the result returned from the WSGI application is
streamed.

Here's an example demonstrating all the features:

::

    import time
    
    def hello(environ, start_response):
        write = start_response('200 OK', [('Content-type', 'text/html')])
        write('Hello')
        def result():
            yield ' World! Environ keys: '
            for name in environ['flows.flow'].keys():
                yield name + ', '
                time.sleep(1)
        return result()
    
    def on_action_wsgi(flow):
        flow.provider.start('wsgi')
        flow.wsgi.result = hello(flow.wsgi.environ, flow.wsgi.start_response)

