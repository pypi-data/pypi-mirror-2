PipeStack Gateway Interface
===========================

See also the HTTPKit docs.

PSGI is a re-formulation of the WSGI designed to accomodate working with Unicode rather than byte-streams and to be very compatible with PipeStack applications. Here's the spec.

The bag will contain two marbles (which can be named with other aliases). These are:

``environ``
    The WSGI environ.

``response``
    An object representing the response.

    The response object has the following attributes:
    
    ``status``
        A bytes object or Unicode string defaulting to ``u'200 OK'``
    
    ``header_list``
        An object with a ``as_list()`` method which when called returns a list of
        tuples where each tuple is represents and HTTP header and its value, both
        encoded to bytes based on the format specified by ``header_list``. Defaults
        to a value that when converted would give ``[('Content-type', 'text/html; charset=utf-8')]``
    
    ``body``
        An object which when iterated over yields bytes objects or Unicode strings
        depending on the value of ``body_format``.
    
    ``status_format``
    ``header_list_format``
    ``body_format``
    
        A Unicode string taking the value ``unicode`` or a string representing the
        current encoding used. If a string representing the encoding is used it implies
        the format is a bytes string. Defaults to ``u'unicode'``.

There are three helpers to help a server utilize the response information:

``encode_status(response)``
    Return the status as a bytes object

``encode_headers(response)``
    Return the result of calling ``as_list()`` on the object specified in ``headers``

``stream_body(response)``
    Iterate over the object stored in ``body``, encoding results as necessary based on the format in ``body_format``.

The server which finally sends the response will use these helpers to generate the response.

A suitable object for the ``headers`` attribute might be:

::

    class Headers(list):
        def as_list(self):
            return self

A more sophisticated implementation can treat the headers as a dictionary. An example based on WebOb might be:

::

    class Headers(webob.headers.ResponseHeaders):
        def as_list(self):
            return self._items


