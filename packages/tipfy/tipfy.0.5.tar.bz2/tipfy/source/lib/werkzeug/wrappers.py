# -*- coding: utf-8 -*-
"""
    werkzeug.wrappers
    ~~~~~~~~~~~~~~~~~

    The wrappers are simple request and response objects which you can
    subclass to do whatever you want them to do.  The request object contains
    the information transmitted by the client (webbrowser) and the response
    object contains all the information sent back to the browser.

    An important detail is that the request object is created with the WSGI
    environ and will act as high-level proxy whereas the response object is an
    actual WSGI application.

    Like everything else in Werkzeug these objects will work correctly with
    unicode data.  Incoming form data parsed by the response object will be
    decoded into an unicode object if possible and if it makes sense.


    :copyright: (c) 2010 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import tempfile
import urlparse
from datetime import datetime, timedelta

from werkzeug.http import HTTP_STATUS_CODES, \
     parse_accept_header, parse_cache_control_header, parse_etags, \
     parse_date, generate_etag, is_resource_modified, unquote_etag, \
     quote_etag, parse_set_header, parse_authorization_header, \
     parse_www_authenticate_header, remove_entity_headers, \
     parse_options_header, dump_options_header
from werkzeug.urls import url_decode, iri_to_uri
from werkzeug.formparser import parse_form_data, default_stream_factory
from werkzeug.utils import cached_property, environ_property, \
     cookie_date, parse_cookie, dump_cookie, http_date, escape, \
     header_property, get_content_type
from werkzeug.wsgi import get_current_url, get_host, LimitedStream
from werkzeug.datastructures import MultiDict, CombinedMultiDict, Headers, \
     EnvironHeaders, ImmutableMultiDict, ImmutableTypeConversionDict, \
     ImmutableList, MIMEAccept, CharsetAccept, LanguageAccept, \
     ResponseCacheControl, RequestCacheControl, CallbackDict
from werkzeug._internal import _empty_stream, _decode_unicode, \
     _patch_wrapper


def _run_wsgi_app(*args):
    """This function replaces itself to ensure that the test module is not
    imported unless required.  DO NOT USE!
    """
    global _run_wsgi_app
    from werkzeug.test import run_wsgi_app as _run_wsgi_app
    return _run_wsgi_app(*args)


def _warn_if_string(iterable):
    """Helper for the response objects to check if the iterable returned
    to the WSGI server is not a string.
    """
    if isinstance(iterable, basestring):
        from warnings import Warning
        warn(Warning('response iterable was set to a string.  This appears '
                     'to work but means that the server will send the '
                     'data to the client char, by char.  This is almost '
                     'never intended behavior, use response.data to assign '
                     'strings to the response object.'), stacklevel=2)


class BaseRequest(object):
    """Very basic request object.  This does not implement advanced stuff like
    entity tag parsing or cache controls.  The request object is created with
    the WSGI environment as first argument and will add itself to the WSGI
    environment as ``'werkzeug.request'`` unless it's created with
    `populate_request` set to False.

    There are a couple of mixins available that add additional functionality
    to the request object, there is also a class called `Request` which
    subclasses `BaseRequest` and all the important mixins.

    It's a good idea to create a custom subclass of the :class:`BaseRequest`
    and add missing functionality either via mixins or direct implementation.
    Here an example for such subclasses::

        from werkzeug import BaseRequest, ETagRequestMixin

        class Request(BaseRequest, ETagRequestMixin):
            pass

    Request objects are **read only**.  As of 0.5 modifications are not
    allowed in any place.  Unlike the lower level parsing functions the
    request object will use immutable objects everywhere possible.

    Per default the request object will assume all the text data is `utf-8`
    encoded.  Please refer to `the unicode chapter <unicode.txt>`_ for more
    details about customizing the behavior.

    Per default the request object will be added to the WSGI
    environment as `werkzeug.request` to support the debugging system.
    If you don't want that, set `populate_request` to `False`.

    If `shallow` is `True` the environment is initialized as shallow
    object around the environ.  Every operation that would modify the
    environ in any way (such as consuming form data) raises an exception
    unless the `shallow` attribute is explicitly set to `False`.  This
    is useful for middlewares where you don't want to consume the form
    data by accident.  A shallow request is not populated to the WSGI
    environment.

    .. versionchanged:: 0.5
       read-only mode was enforced by using immutables classes for all
       data.
    """

    #: the charset for the request, defaults to utf-8
    charset = 'utf-8'

    #: the error handling procedure for errors, defaults to 'ignore'
    encoding_errors = 'ignore'

    #: set to True if the application runs behind an HTTP proxy
    is_behind_proxy = False

    #: the maximum content length.  This is forwarded to the form data
    #: parsing function (:func:`parse_form_data`).  When set and the
    #: :attr:`form` or :attr:`files` attribute is accessed and the
    #: parsing fails because more than the specified value is transmitted
    #: a :exc:`~exceptions.RequestEntityTooLarge` exception is raised.
    #:
    #: Have a look at :ref:`dealing-with-request-data` for more details.
    #:
    #: .. versionadded:: 0.5
    max_content_length = None

    #: the maximum form field size.  This is forwarded to the form data
    #: parsing function (:func:`parse_form_data`).  When set and the
    #: :attr:`form` or :attr:`files` attribute is accessed and the
    #: data in memory for post data is longer than the specified value a
    #: :exc:`~exceptions.RequestEntityTooLarge` exception is raised.
    #:
    #: Have a look at :ref:`dealing-with-request-data` for more details.
    #:
    #: .. versionadded:: 0.5
    max_form_memory_size = None

    #: the class to use for `args` and `form`.  The default is an
    #: :class:`ImmutableMultiDict` which supports multiple values per key.
    #: alternatively it makes sense to use an :class:`ImmutableOrderedMultiDict`
    #: which preserves order or a :class:`ImmutableDict` which is
    #: the fastest but only remembers the last key.  It is also possible
    #: to use mutable structures, but this is not recommended.
    #:
    #: .. versionadded:: 0.6
    parameter_storage_class = ImmutableMultiDict

    #: the type to be used for list values from the incoming WSGI
    #: environment.  By default an :class:`ImmutableList` is used
    #: (for example for :attr:`access_list`).
    #:
    #: .. versionadded:: 0.6
    list_storage_class = ImmutableList

    #: the type to be used for dict values from the incoming WSGI
    #: environment.  By default an :class:`ImmutableTypeConversionDict`
    #: is used (for example for :attr:`cookies`).
    #:
    #: .. versionadded:: 0.6
    dict_storage_class = ImmutableTypeConversionDict

    def __init__(self, environ, populate_request=True, shallow=False):
        self.environ = environ
        if populate_request and not shallow:
            self.environ['werkzeug.request'] = self
        self.shallow = shallow

    def __repr__(self):
        # make sure the __repr__ even works if the request was created
        # from an invalid WSGI environment.  If we display the request
        # in a debug session we don't want the repr to blow up.
        args = []
        try:
            args.append("'%s'" % self.url)
            args.append('[%s]' % self.method)
        except:
            args.append('(invalid WSGI environ)')

        return '<%s %s>' % (
            self.__class__.__name__,
            ' '.join(args)
        )

    @property
    def url_charset(self):
        """The charset that is assumed for URLs.  Defaults to the value
        of :attr:`charset`.

        .. versionadded:: 0.6
        """
        return self.charset

    @classmethod
    def from_values(cls, *args, **kwargs):
        """Create a new request object based on the values provided.  If
        environ is given missing values are filled from there.  This method is
        useful for small scripts when you need to simulate a request from an URL.
        Do not use this method for unittesting, there is a full featured client
        object (:class:`Client`) that allows to create multipart requests,
        support for cookies etc.

        This accepts the same options as the :class:`EnvironBuilder`.

        .. versionchanged:: 0.5
           This method now accepts the same arguments as
           :class:`EnvironBuilder`.  Because of this the `environ` parameter
           is now called `environ_overrides`.

        :return: request object
        """
        from werkzeug.test import EnvironBuilder
        charset = kwargs.pop('charset', cls.charset)
        builder = EnvironBuilder(*args, **kwargs)
        try:
            return builder.get_request(cls)
        finally:
            builder.close()

    @classmethod
    def application(cls, f):
        """Decorate a function as responder that accepts the request as first
        argument.  This works like the :func:`responder` decorator but the
        function is passed the request object as first argument::

            @Request.application
            def my_wsgi_app(request):
                return Response('Hello World!')

        :param f: the WSGI callable to decorate
        :return: a new WSGI callable
        """
        #: return a callable that wraps the -2nd argument with the request
        #: and calls the function with all the arguments up to that one and
        #: the request.  The return value is then called with the latest
        #: two arguments.  This makes it possible to use this decorator for
        #: both methods and standalone WSGI functions.
        return _patch_wrapper(f, lambda *a: f(*a[:-2]+(cls(a[-2]),))(*a[-2:]))

    def _get_file_stream(self, total_content_length, content_type, filename=None,
                         content_length=None):
        """Called to get a stream for the file upload.

        This must provide a file-like class with `read()`, `readline()`
        and `seek()` methods that is both writeable and readable.

        The default implementation returns a temporary file if the total
        content length is higher than 500KB.  Because many browsers do not
        provide a content length for the files only the total content
        length matters.

        .. versionchanged:: 0.5
           Previously this function was not passed any arguments.  In 0.5 older
           functions not accepting any arguments are still supported for
           backwards compatibility.

        :param total_content_length: the total content length of all the
                                     data in the request combined.  This value
                                     is guaranteed to be there.
        :param content_type: the mimetype of the uploaded file.
        :param filename: the filename of the uploaded file.  May be `None`.
        :param content_length: the length of this file.  This value is usually
                               not provided because webbrowsers do not provide
                               this value.
        """
        return default_stream_factory(total_content_length, content_type,
                                      filename, content_length)

    def _load_form_data(self):
        """Method used internally to retrieve submitted data.  After calling
        this sets `form` and `files` on the request object to multi dicts
        filled with the incoming form data.  As a matter of fact the input
        stream will be empty afterwards.

        :internal:
        """
        # abort early if we have already consumed the stream
        if 'stream' in self.__dict__:
            return
        if self.shallow:
            raise RuntimeError('A shallow request tried to consume '
                               'form data.  If you really want to do '
                               'that, set `shallow` to False.')
        data = None
        stream = _empty_stream
        if self.environ['REQUEST_METHOD'] in ('POST', 'PUT'):
            try:
                data = parse_form_data(self.environ, self._get_file_stream,
                                       self.charset, self.encoding_errors,
                                       self.max_form_memory_size,
                                       self.max_content_length,
                                       cls=self.parameter_storage_class,
                                       silent=False)
            except ValueError, e:
                self._form_parsing_failed(e)
        else:
            # if we have a content length header we are able to properly
            # guard the incoming stream, no matter what request method is
            # used.
            content_length = self.headers.get('content-length', type=int)
            if content_length is not None:
                stream = LimitedStream(self.environ['wsgi.input'],
                                       content_length)

        if data is None:
            data = (stream, self.parameter_storage_class(),
                    self.parameter_storage_class())

        # inject the values into the instance dict so that we bypass
        # our cached_property non-data descriptor.
        d = self.__dict__
        d['stream'], d['form'], d['files'] = data

    def _form_parsing_failed(self, error):
        """Called if parsing of form data failed.  This is currently only
        invoked for failed multipart uploads.  By default this method does
        nothing.

        :param error: a `ValueError` object with a message why the
                      parsing failed.

        .. versionadded:: 0.5.1
        """

    @cached_property
    def stream(self):
        """The parsed stream if the submitted data was not multipart or
        urlencoded form data.  This stream is the stream left by the form data
        parser module after parsing.  This is *not* the WSGI input stream but
        a wrapper around it that ensures the caller does not accidentally
        read past `Content-Length`.
        """
        self._load_form_data()
        return self.stream

    input_stream = environ_property('wsgi.input', 'The WSGI input stream.\n'
        'In general it\'s a bad idea to use this one because you can easily '
        'read past the boundary.  Use the :attr:`stream` instead.')

    @cached_property
    def args(self):
        """The parsed URL parameters.  By default a :class:`ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        """
        return url_decode(self.environ.get('QUERY_STRING', ''),
                          self.url_charset, errors=self.encoding_errors,
                          cls=self.parameter_storage_class)

    @cached_property
    def data(self):
        """This reads the buffered incoming data from the client into the
        string.  Usually it's a bad idea to access :attr:`data` because a client
        could send dozens of megabytes or more to cause memory problems on the
        server.

        To circumvent that make sure to check the content length first.
        """
        return self.stream.read()

    @cached_property
    def form(self):
        """The form parameters.  By default a :class:`ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        """
        self._load_form_data()
        return self.form

    @cached_property
    def values(self):
        """Combined multi dict for :attr:`args` and :attr:`form`."""
        args = []
        for d in self.args, self.form:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombinedMultiDict(args)

    @cached_property
    def files(self):
        """:class:`MultiDict` object containing all uploaded files.  Each key in
        :attr:`files` is the name from the ``<input type="file" name="">``.  Each
        value in :attr:`files` is a Werkzeug :class:`FileStorage` object.

        Note that :attr:`files` will only contain data if the request method was
        POST or PUT and the ``<form>`` that posted to the request had
        ``enctype="multipart/form-data"``.  It will be empty otherwise.

        See the :class:`MultiDict` / :class:`FileStorage` documentation for more
        details about the used data structure.
        """
        self._load_form_data()
        return self.files

    @cached_property
    def cookies(self):
        """Read only access to the retrieved cookie values as dictionary."""
        return parse_cookie(self.environ, self.charset,
                            cls=self.dict_storage_class)

    @cached_property
    def headers(self):
        """The headers from the WSGI environ as immutable
        :class:`EnvironHeaders`.
        """
        return EnvironHeaders(self.environ)

    @cached_property
    def path(self):
        """Requested path as unicode.  This works a bit like the regular path
        info in the WSGI environment but will always include a leading slash,
        even if the URL root is accessed.
        """
        path = '/' + (self.environ.get('PATH_INFO') or '').lstrip('/')
        return _decode_unicode(path, self.url_charset, self.encoding_errors)

    @cached_property
    def script_root(self):
        """The root path of the script without the trailing slash."""
        path = (self.environ.get('SCRIPT_NAME') or '').rstrip('/')
        return _decode_unicode(path, self.url_charset, self.encoding_errors)

    @cached_property
    def url(self):
        """The reconstructed current URL"""
        return get_current_url(self.environ)

    @cached_property
    def base_url(self):
        """Like :attr:`url` but without the querystring"""
        return get_current_url(self.environ, strip_querystring=True)

    @cached_property
    def url_root(self):
        """The full URL root (with hostname), this is the application root."""
        return get_current_url(self.environ, True)

    @cached_property
    def host_url(self):
        """Just the host with scheme."""
        return get_current_url(self.environ, host_only=True)

    @cached_property
    def host(self):
        """Just the host including the port if available."""
        return get_host(self.environ)

    query_string = environ_property('QUERY_STRING', '', read_only=True, doc=
        '''The URL parameters as raw bytestring.''')
    method = environ_property('REQUEST_METHOD', 'GET', read_only=True, doc=
        '''The transmission method. (For example ``'GET'`` or ``'POST'``).''')

    @cached_property
    def access_route(self):
        """If a forwarded header exists this is a list of all ip addresses
        from the client ip to the last proxy server.
        """
        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            addr = self.environ['HTTP_X_FORWARDED_FOR'].split(',')
            return self.list_storage_class([x.strip() for x in addr])
        elif 'REMOTE_ADDR' in self.environ:
            return self.list_storage_class([self.environ['REMOTE_ADDR']])
        return self.list_storage_class()

    @property
    def remote_addr(self):
        """The remote address of the client."""
        if self.is_behind_proxy and self.access_route:
            return self.access_route[0]
        return self.environ.get('REMOTE_ADDR')

    remote_user = environ_property('REMOTE_USER', doc='''
        If the server supports user authentication, and the script is
        protected, this attribute contains the username the user has
        authenticated as.''')

    is_xhr = property(lambda x: x.environ.get('HTTP_X_REQUESTED_WITH', '')
                      .lower() == 'xmlhttprequest', doc='''
        True if the request was triggered via a JavaScript XMLHttpRequest.
        This only works with libraries that support the `X-Requested-With`
        header and set it to "XMLHttpRequest".  Libraries that do that are
        prototype, jQuery and Mochikit and probably some more.''')
    is_secure = property(lambda x: x.environ['wsgi.url_scheme'] == 'https',
                         doc='`True` if the request is secure.')
    is_multithread = environ_property('wsgi.multithread', doc='''
        boolean that is `True` if the application is served by
        a multithreaded WSGI server.''')
    is_multiprocess = environ_property('wsgi.multiprocess', doc='''
        boolean that is `True` if the application is served by
        a WSGI server that spawns multiple processes.''')
    is_run_once = environ_property('wsgi.run_once', doc='''
        boolean that is `True` if the application will be executed only
        once in a process lifetime.  This is the case for CGI for example,
        but it's not guaranteed that the exeuction only happens one time.''')


class BaseResponse(object):
    """Base response class.  The most important fact about a response object
    is that it's a regular WSGI application.  It's initialized with a couple
    of response parameters (headers, body, status code etc.) and will start a
    valid WSGI response when called with the environ and start response
    callable.

    Because it's a WSGI application itself processing usually ends before the
    actual response is sent to the server.  This helps debugging systems
    because they can catch all the exceptions before responses are started.

    Here a small example WSGI application that takes advantage of the
    response objects::

        from werkzeug import BaseResponse as Response

        def index():
            return Response('Index page')

        def application(environ, start_response):
            path = environ.get('PATH_INFO') or '/'
            if path == '/':
                response = index()
            else:
                response = Response('Not Found', status=404)
            return response(environ, start_response)

    Like :class:`BaseRequest` which object is lacking a lot of functionality
    implemented in mixins.  This gives you a better control about the actual
    API of your response objects, so you can create subclasses and add custom
    functionality.  A full featured response object is available as
    :class:`Response` which implements a couple of useful mixins.

    To enforce a new type of already existing responses you can use the
    :meth:`force_type` method.  This is useful if you're working with different
    subclasses of response objects and you want to post process them with a
    know interface.

    Per default the request object will assume all the text data is `utf-8`
    encoded.  Please refer to `the unicode chapter <unicode.txt>`_ for more
    details about customizing the behavior.

    Response can be any kind of iterable or string.  If it's a string
    it's considered being an iterable with one item which is the string
    passed.  Headers can be a list of tuples or a :class:`Headers` object.

    Special note for `mimetype` and `content_type`:  For most mime types
    `mimetype` and `content_type` work the same, the difference affects
    only 'text' mimetypes.  If the mimetype passed with `mimetype` is a
    mimetype starting with `text/` it becomes a charset parameter defined
    with the charset of the response object.  In contrast the
    `content_type` parameter is always added as header unmodified.

    .. versionchanged:: 0.5
       the `direct_passthrough` parameter was added.

    :param response: a string or response iterable.
    :param status: a string with a status or an integer with the status code.
    :param headers: a list of headers or an :class:`Headers` object.
    :param mimetype: the mimetype for the request.  See notice above.
    :param content_type: the content type for the request.  See notice above.
    :param direct_passthrough: if set to `True` :meth:`iter_encoded` is not
                               called before iteration which makes it
                               possible to pass special iterators though
                               unchanged (see :func:`wrap_file` for more
                               details.)
    """

    #: the charset of the response.
    charset = 'utf-8'

    #: the default status if none is provided.
    default_status = 200

    #: the default mimetype if none is provided.
    default_mimetype = 'text/plain'

    #: if set to `False` accessing properties on the response object will
    #: not try to consume the response iterator and convert it into a list.
    implicit_seqence_conversion = True

    def __init__(self, response=None, status=None, headers=None,
                 mimetype=None, content_type=None, direct_passthrough=False):
        if isinstance(headers, Headers):
            self.headers = headers
        elif not headers:
            self.headers = Headers()
        else:
            self.headers = Headers(headers)

        if content_type is None:
            if mimetype is None and 'content-type' not in self.headers:
                mimetype = self.default_mimetype
            if mimetype is not None:
                mimetype = get_content_type(mimetype, self.charset)
            content_type = mimetype
        if content_type is not None:
            self.headers['Content-Type'] = content_type
        if status is None:
            status = self.default_status
        if isinstance(status, (int, long)):
            self.status_code = status
        else:
            self.status = status

        self.direct_passthrough = direct_passthrough
        self._on_close = []

        # we set the response after the headers so that if a class changes
        # the charset attribute, the data is set in the correct charset.
        if response is None:
            self.response = []
        elif isinstance(response, basestring):
            self.data = response
        else:
            self.response = response

    def call_on_close(self, func):
        """Adds a function to the internal list of functions that should
        be called as part of closing down the response.

        .. versionadded:: 0.6
        """
        self._on_close.append(func)

    def __repr__(self):
        if self.is_sequence:
            body_info = '%d bytes' % sum(map(len, self.iter_encoded()))
        else:
            body_info = self.is_streamed and 'streamed' or 'likely-streamed'
        return '<%s %s [%s]>' % (
            self.__class__.__name__,
            body_info,
            self.status
        )

    @classmethod
    def force_type(cls, response, environ=None):
        """Enforce that the WSGI response is a response object of the current
        type.  Werkzeug will use the :class:`BaseResponse` internally in many
        situations like the exceptions.  If you call :meth:`get_response` on an
        exception you will get back a regular :class:`BaseResponse` object, even
        if you are using a custom subclass.

        This method can enforce a given response type, and it will also
        convert arbitrary WSGI callables into response objects if an environ
        is provided::

            # convert a Werkzeug response object into an instance of the
            # MyResponseClass subclass.
            response = MyResponseClass.force_type(response)

            # convert any WSGI application into a response object
            response = MyResponseClass.force_type(response, environ)

        This is especially useful if you want to post-process responses in
        the main dispatcher and use functionality provided by your subclass.

        Keep in mind that this will modify response objects in place if
        possible!

        :param response: a response object or wsgi application.
        :param environ: a WSGI environment object.
        :return: a response object.
        """
        if not isinstance(response, BaseResponse):
            if environ is None:
                raise TypeError('cannot convert WSGI application into '
                                'response objects without an environ')
            response = BaseResponse(*_run_wsgi_app(response, environ))
        response.__class__ = cls
        return response

    @classmethod
    def from_app(cls, app, environ, buffered=False):
        """Create a new response object from an application output.  This
        works best if you pass it an application that returns a generator all
        the time.  Sometimes applications may use the `write()` callable
        returned by the `start_response` function.  This tries to resolve such
        edge cases automatically.  But if you don't get the expected output
        you should set `buffered` to `True` which enforces buffering.

        :param app: the WSGI application to execute.
        :param environ: the WSGI environment to execute against.
        :param buffered: set to `True` to enforce buffering.
        :return: a response object.
        """
        return cls(*_run_wsgi_app(app, environ, buffered))

    def _get_status_code(self):
        try:
            return int(self.status.split(None, 1)[0])
        except ValueError:
            return 0
    def _set_status_code(self, code):
        try:
            self.status = '%d %s' % (code, HTTP_STATUS_CODES[code].upper())
        except KeyError:
            self.status = '%d UNKNOWN' % code
    status_code = property(_get_status_code, _set_status_code,
                           'The HTTP Status code as number')
    del _get_status_code, _set_status_code

    def _get_data(self):
        """The string representation of the request body.  Whenever you access
        this property the request iterable is encoded and flattened.  This
        can lead to unwanted behavior if you stream big data.

        This behavior can be disabled by setting
        :attr:`implicit_seqence_conversion` to `False`.
        """
        self._ensure_sequence()
        return ''.join(self.iter_encoded())
    def _set_data(self, value):
        # if an unicode string is set, it's encoded directly.  this allows
        # us to guess the content length automatically in `get_wsgi_headers`.
        if isinstance(value, unicode):
            value = value.encode(self.charset)
        self.response = [value]
    data = property(_get_data, _set_data, doc=_get_data.__doc__)
    del _get_data, _set_data

    def _ensure_sequence(self, mutable=False):
        """This method can be called by methods that need a sequence.  If
        `mutable` is true, it will also ensure that the response sequence
        is a standard Python list.

        .. versionadded:: 0.6
        """
        if self.is_sequence:
            # if we need a mutable object, we ensure it's a list.
            if mutable and not isinstance(self.response, list):
                self.response = list(self.response)
            return
        if not self.implicit_seqence_conversion:
            raise RuntimeError('The response object required the iterable '
                               'to be a sequence, but the implicit '
                               'conversion was disabled.  Call '
                               'make_sequence() yourself.')
        self.make_sequence()

    def make_sequence(self):
        """Converts the response iterator in a list.  By default this happens
        automatically if required.  If `implicit_seqence_conversion` is
        disabled, this method is not automatically called and some properties
        might raise exceptions.  This also encodes all the items.

        .. versionadded:: 0.6
        """
        if not self.is_sequence:
            # if we consume an iterable we have to ensure that the close
            # method of the iterable is called if available when we tear
            # down the response
            close = getattr(self.response, 'close', None)
            self.response = list(self.iter_encoded())
            if close is not None:
                self.call_on_close(close)

    def iter_encoded(self, charset=None):
        """Iter the response encoded with the encoding of the response.
        If the response object is invoked as WSGI application the return
        value of this method is used as application iterator unless
        :attr:`direct_passthrough` was activated.

        .. versionchanged:: 0.6

           The `charset` parameter was deprecated and became a no-op.
        """
        # XXX: deprecated
        if __debug__ and charset is not None:
            from warnings import warn
            warn(DeprecationWarning('charset was deprecated and is ignored.'),
                 stacklevel=2)
        charset = self.charset
        if __debug__:
            _warn_if_string(self.response)
        for item in self.response:
            if isinstance(item, unicode):
                yield item.encode(charset)
            else:
                yield str(item)

    def set_cookie(self, key, value='', max_age=None, expires=None,
                   path='/', domain=None, secure=None, httponly=False):
        """Sets a cookie. The parameters are the same as in the cookie `Morsel`
        object in the Python standard library but it accepts unicode data, too.

        :param key: the key (name) of the cookie to be set.
        :param value: the value of the cookie.
        :param max_age: should be a number of seconds, or `None` (default) if
                        the cookie should last only as long as the client's
                        browser session.
        :param expires: should be a `datetime` object or UNIX timestamp.
        :param domain: if you want to set a cross-domain cookie.  For example,
                       ``domain=".example.com"`` will set a cookie that is
                       readable by the domain ``www.example.com``,
                       ``foo.example.com`` etc.  Otherwise, a cookie will only
                       be readable by the domain that set it.
        :param path: limits the cookie to a given path, per default it will
                     span the whole domain.
        """
        self.headers.add('Set-Cookie', dump_cookie(key, value, max_age,
                         expires, path, domain, secure, httponly,
                         self.charset))

    def delete_cookie(self, key, path='/', domain=None):
        """Delete a cookie.  Fails silently if key doesn't exist.

        :param key: the key (name) of the cookie to be deleted.
        :param path: if the cookie that should be deleted was limited to a
                     path, the path has to be defined here.
        :param domain: if the cookie that should be deleted was limited to a
                       domain, that domain has to be defined here.
        """
        self.set_cookie(key, expires=0, max_age=0, path=path, domain=domain)

    @property
    def header_list(self):
        # XXX: deprecated
        if __debug__:
            from warnings import warn
            warn(DeprecationWarning('header_list is deprecated'),
                 stacklevel=2)
        return self.headers.to_list(self.charset)

    @property
    def is_streamed(self):
        """If the response is streamed (the response is not an iterable with
        a length information) this property is `True`.  In this case streamed
        means that there is no information about the number of iterations.
        This is usually `True` if a generator is passed to the response object.

        This is useful for checking before applying some sort of post
        filtering that should not take place for streamed responses.
        """
        try:
            len(self.response)
        except TypeError:
            return True
        return False

    @property
    def is_sequence(self):
        """If the iterator is buffered, this property will be `True`.  A
        response object will consider an iterator to be buffered if the
        response attribute is a list or tuple.

        .. versionadded:: 0.6
        """
        return isinstance(self.response, (tuple, list))

    def close(self):
        """Close the wrapped response if possible."""
        if hasattr(self.response, 'close'):
            self.response.close()
        for func in self._on_close:
            func()

    def freeze(self):
        """Call this method if you want to make your response object ready for
        being pickled.  This buffers the generator if there is one.  It will
        also set the `Content-Length` header to the length of the body.

        .. versionchanged:: 0.6
           The `Content-Length` header is now set.
        """
        # we explicitly set the length to a list of the *encoded* response
        # iterator.  Even if the implicit sequence conversion is disabled.
        self.response = list(self.iter_encoded())
        self.headers['Content-Length'] = str(sum(map(len, self.response)))

    def fix_headers(self, environ):
        # XXX: deprecated
        if __debug__:
            from warnings import warn
            warn(DeprecationWarning('called into deprecated fix_headers baseclass '
                                    'method.  Use get_wsgi_headers instead.'),
                 stacklevel=2)
        self.headers[:] = self.get_wsgi_headers(environ)

    def get_wsgi_headers(self, environ):
        """This is automatically called right before the response is started
        and returns headers modified for the given environment.  It returns a
        copy of the headers from the response with some modifications applied
        if necessary.

        For example the location header (if present) is joined with the root
        URL of the environment.  Also the content length is automatically set
        to zero here for certain status codes.

        .. versionchanged:: 0.6
           Previously that function was called `fix_headers` and modified
           the response object in place.  Also since 0.6, IRIs in location
           and content-location headers are handled properly.

           Also starting with 0.6, Werkzeug will attempt to set the content
           length if it is able to figure it out on its own.  This is the
           case if all the strings in the response iterable are already
           encoded and the iterable is buffered.

        :param environ: the WSGI environment of the request.
        :return: returns a new :class:`Headers` object.
        """
        headers = Headers(self.headers)

        # make sure the location header is an absolute URL
        location = headers.get('location')
        if location is not None:
            if isinstance(location, unicode):
                location = iri_to_uri(location)
            headers['Location'] = urlparse.urljoin(
                get_current_url(environ, root_only=True),
                location
            )

        # make sure the content location is a URL
        content_location = headers.get('content-location')
        if content_location is not None and \
           isinstance(content_location, unicode):
            headers['Content-Location'] = iri_to_uri(content_location)

        if 100 <= self.status_code < 200 or self.status_code == 204:
            headers['Content-Length'] = '0'
        elif self.status_code == 304:
            remove_entity_headers(headers)

        # if we can determine the content length automatically, we
        # should try to do that.  But only if this does not involve
        # flattening the iterator or encoding of unicode strings in
        # the response.
        if self.is_sequence and 'content-length' not in self.headers:
            try:
                content_length = sum(len(str(x)) for x in self.response)
            except UnicodeError:
                # aha, something non-bytestringy in there, too bad, we
                # can't safely figure out the length of the response.
                pass
            else:
                headers['Content-Length'] = str(content_length)

        return headers

    def get_app_iter(self, environ):
        """Returns the application iterator for the given environ.  Depending
        on the request method and the current status code the return value
        might be an empty response rather than the one from the response.

        If the request method is `HEAD` or the status code is in a range
        where the HTTP specification requires an empty response, an empty
        iterable is returned.

        .. versionadded:: 0.6

        :param environ: the WSGI environment of the request.
        :return: a response iterable.
        """
        if environ['REQUEST_METHOD'] == 'HEAD' or \
           100 <= self.status_code < 200 or self.status_code in (204, 304):
            return ()
        if self.direct_passthrough:
            if __debug__:
                _warn_if_string(self.response)
            return self.response
        return self.iter_encoded()

    def get_wsgi_response(self, environ):
        """Returns the final WSGI response as tuple.  The first item in
        the tuple is the application iterator, the second the status and
        the third the list of headers.  The response returned is created
        specially for the given environment.  For example if the request
        method in the WSGI environment is ``'HEAD'`` the response will
        be empty and only the headers and status code will be present.

        .. versionadded:: 0.6

        :param environ: the WSGI environment of the request.
        :return: an ``(app_iter, status, headers)`` tuple.
        """
        # XXX: code for backwards compatibility with custom fix_headers
        # methods.
        if self.fix_headers.func_code is not \
           BaseResponse.fix_headers.func_code:
            if __debug__:
                from warnings import warn
                warn(DeprecationWarning('fix_headers changed behavior in 0.6 '
                                        'and is now called get_wsgi_headers. '
                                        'See documentation for more details.'),
                     stacklevel=2)
            self.fix_headers(environ)
            headers = self.headers
        else:
            headers = self.get_wsgi_headers(environ)
        app_iter = self.get_app_iter(environ)
        return app_iter, self.status, headers.to_list(self.charset)

    def __call__(self, environ, start_response):
        """Process this response as WSGI application.

        :param environ: the WSGI environment.
        :param start_response: the response callable provided by the WSGI
                               server.
        :return: an application iterator
        """
        app_iter, status, headers = self.get_wsgi_response(environ)
        start_response(status, headers)
        return app_iter


class AcceptMixin(object):
    """A mixin for classes with an :attr:`~BaseResponse.environ` attribute to
    get all the HTTP accept headers as :class:`Accept` objects (or subclasses
    thereof).
    """

    @cached_property
    def accept_mimetypes(self):
        """List of mimetypes this client supports as :class:`MIMEAccept`
        object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT'), MIMEAccept)

    @cached_property
    def accept_charsets(self):
        """List of charsets this client supports as :class:`CharsetAccept`
        object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_CHARSET'),
                                   CharsetAccept)

    @cached_property
    def accept_encodings(self):
        """List of encodings this client accepts.  Encodings in a HTTP term
        are compression encodings such as gzip.  For charsets have a look at
        :attr:`accept_charset`.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_ENCODING'))

    @cached_property
    def accept_languages(self):
        """List of languages this client accepts as :class:`LanguageAccept`
        object.

        .. versionchanged 0.5
           In previous versions this was a regular :class:`Accept` object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_LANGUAGE'),
                                   LanguageAccept)


class ETagRequestMixin(object):
    """Add entity tag and cache descriptors to a request object or object with
    a WSGI environment available as :attr:`~BaseRequest.environ`.  This not
    only provides access to etags but also to the cache control header.
    """

    @cached_property
    def cache_control(self):
        """A :class:`RequestCacheControl` object for the incoming cache control
        headers.
        """
        cache_control = self.environ.get('HTTP_CACHE_CONTROL')
        return parse_cache_control_header(cache_control, None,
                                          RequestCacheControl)

    @cached_property
    def if_match(self):
        """An object containing all the etags in the `If-Match` header."""
        return parse_etags(self.environ.get('HTTP_IF_MATCH'))

    @cached_property
    def if_none_match(self):
        """An object containing all the etags in the `If-None-Match` header."""
        return parse_etags(self.environ.get('HTTP_IF_NONE_MATCH'))

    @cached_property
    def if_modified_since(self):
        """The parsed `If-Modified-Since` header as datetime object."""
        return parse_date(self.environ.get('HTTP_IF_MODIFIED_SINCE'))

    @cached_property
    def if_unmodified_since(self):
        """The parsed `If-Unmodified-Since` header as datetime object."""
        return parse_date(self.environ.get('HTTP_IF_UNMODIFIED_SINCE'))


class UserAgentMixin(object):
    """Adds a `user_agent` attribute to the request object which contains the
    parsed user agent of the browser that triggered the request as `UserAgent`
    object.
    """

    @cached_property
    def user_agent(self):
        """The current user agent."""
        from werkzeug.useragents import UserAgent
        return UserAgent(self.environ)


class AuthorizationMixin(object):
    """Adds an :attr:`authorization` property that represents the parsed value
    of the `Authorization` header as :class:`Authorization` object.
    """

    @cached_property
    def authorization(self):
        """The `Authorization` object in parsed form."""
        header = self.environ.get('HTTP_AUTHORIZATION')
        return parse_authorization_header(header)


class ETagResponseMixin(object):
    """Adds extra functionality to a response object for etag and cache
    handling.  This mixin requires an object with at least a `headers`
    object that implements a dict like interface similar to :class:`Headers`.
    """

    @property
    def cache_control(self):
        """The Cache-Control general-header field is used to specify
        directives that MUST be obeyed by all caching mechanisms along the
        request/response chain.
        """
        def on_update(cache_control):
            if not cache_control and 'cache-control' in self.headers:
                del self.headers['cache-control']
            elif cache_control:
                self.headers['Cache-Control'] = cache_control.to_header()
        return parse_cache_control_header(self.headers.get('cache-control'),
                                          on_update,
                                          ResponseCacheControl)

    def make_conditional(self, request_or_environ):
        """Make the response conditional to the request.  This method works
        best if an etag was defined for the response already.  The `add_etag`
        method can be used to do that.  If called without etag just the date
        header is set.

        This does nothing if the request method in the request or environ is
        anything but GET or HEAD.

        It does not remove the body of the response because that's something
        the :meth:`__call__` function does for us automatically.

        Returns self so that you can do ``return resp.make_conditional(req)``
        but modifies the object in-place.

        :param request_or_environ: a request object or WSGI environment to be
                                   used to make the response conditional
                                   against.
        """
        environ = getattr(request_or_environ, 'environ', request_or_environ)
        if environ['REQUEST_METHOD'] in ('GET', 'HEAD'):
            self.headers['Date'] = http_date()
            if 'content-length' in self.headers:
                self.headers['Content-Length'] = len(self.data)
            if not is_resource_modified(environ, self.headers.get('etag'), None,
                                        self.headers.get('last-modified')):
                self.status_code = 304
        return self

    def add_etag(self, overwrite=False, weak=False):
        """Add an etag for the current response if there is none yet."""
        if overwrite or 'etag' not in self.headers:
            self.set_etag(generate_etag(self.data), weak)

    def set_etag(self, etag, weak=False):
        """Set the etag, and override the old one if there was one."""
        self.headers['ETag'] = quote_etag(etag, weak)

    def get_etag(self):
        """Return a tuple in the form ``(etag, is_weak)``.  If there is no
        ETag the return value is ``(None, None)``.
        """
        return unquote_etag(self.headers.get('ETag'))

    def freeze(self, no_etag=False):
        """Call this method if you want to make your response object ready for
        pickeling.  This buffers the generator if there is one.  This also
        sets the etag unless `no_etag` is set to `True`.
        """
        if not no_etag:
            self.add_etag()
        super(ETagResponseMixin, self).freeze()


class ResponseStream(object):
    """A file descriptor like object used by the :class:`ResponseStreamMixin` to
    represent the body of the stream.  It directly pushes into the response
    iterable of the response object.
    """

    mode = 'wb+'

    def __init__(self, response):
        self.response = response
        self.closed = False

    def write(self, value):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        self.response._ensure_sequence(mutable=True)
        self.response.response.append(value)

    def writelines(self, seq):
        for item in seq:
            self.write(item)

    def close(self):
        self.closed = True

    def flush(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')

    def isatty(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return False

    @property
    def encoding(self):
        return self.response.charset


class ResponseStreamMixin(object):
    """Mixin for :class:`BaseRequest` subclasses.  Classes that inherit from
    this mixin will automatically get a :attr:`stream` property that provides
    a write-only interface to the response iterable.
    """

    @cached_property
    def stream(self):
        """The response iterable as write-only stream."""
        return ResponseStream(self)


class CommonRequestDescriptorsMixin(object):
    """A mixin for :class:`BaseRequest` subclasses.  Request objects that
    mix this class in will automatically get descriptors for a couple of
    HTTP headers with automatic type conversion.

    .. versionadded:: 0.5
    """

    content_type = environ_property('CONTENT_TYPE', doc='''
         The Content-Type entity-header field indicates the media type of
         the entity-body sent to the recipient or, in the case of the HEAD
         method, the media type that would have been sent had the request
         been a GET.''')
    content_length = environ_property('CONTENT_LENGTH', None, int, str, doc='''
         The Content-Length entity-header field indicates the size of the
         entity-body in bytes or, in the case of the HEAD method, the size of
         the entity-body that would have been sent had the request been a
         GET.''')
    referrer = environ_property('HTTP_REFERER', doc='''
        The Referer[sic] request-header field allows the client to specify,
        for the server's benefit, the address (URI) of the resource from which
        the Request-URI was obtained (the "referrer", although the header
        field is misspelled).''')
    date = environ_property('HTTP_DATE', None, parse_date, doc='''
        The Date general-header field represents the date and time at which
        the message was originated, having the same semantics as orig-date
        in RFC 822.''')
    max_forwards = environ_property('HTTP_MAX_FORWARDS', None, int, doc='''
         The Max-Forwards request-header field provides a mechanism with the
         TRACE and OPTIONS methods to limit the number of proxies or gateways
         that can forward the request to the next inbound server.''')

    def _parse_content_type(self):
        if not hasattr(self, '_parsed_content_type'):
            self._parsed_content_type = \
                parse_options_header(self.environ.get('CONTENT_TYPE', ''))

    @property
    def mimetype(self):
        """Like :attr:`content_type` but without parameters (eg, without
        charset, type etc.).  For example if the content
        type is ``text/html; charset=utf-8`` the mimetype would be
        ``'text/html'``.
        """
        self._parse_content_type()
        return self._parsed_content_type[0]

    @property
    def mimetype_params(self):
        """The mimetype parameters as dict.  For example if the content
        type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.
        """
        self._parse_content_type()
        return self._parsed_content_type[1]

    @cached_property
    def pragma(self):
        """The Pragma general-header field is used to include
        implementation-specific directives that might apply to any recipient
        along the request/response chain.  All pragma directives specify
        optional behavior from the viewpoint of the protocol; however, some
        systems MAY require that behavior be consistent with the directives.
        """
        return parse_set_header(self.environ.get('HTTP_PRAGMA', ''))


class CommonResponseDescriptorsMixin(object):
    """A mixin for :class:`BaseResponse` subclasses.  Response objects that
    mix this class in will automatically get descriptors for a couple of
    HTTP headers with automatic type conversion.
    """

    def _get_mimetype(self):
        ct = self.headers.get('content-type')
        if ct:
            return ct.split(';')[0].strip()

    def _set_mimetype(self, value):
        self.headers['Content-Type'] = get_content_type(value, self.charset)

    def _get_mimetype_params(self):
        def on_update(d):
            self.headers['Content-Type'] = \
                dump_options_header(self.mimetype, d)
        d = parse_options_header(self.headers.get('content-type', ''))[1]
        return CallbackDict(d, on_update)

    mimetype = property(_get_mimetype, _set_mimetype, doc='''
        The mimetype (content type without charset etc.)''')
    mimetype_params = property(_get_mimetype_params, doc='''
        The mimetype parameters as dict.  For example if the content
        type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.

        .. versionadded:: 0.5
        ''')
    location = header_property('Location', doc='''
        The Location response-header field is used to redirect the recipient
        to a location other than the Request-URI for completion of the request
        or identification of a new resource.''')
    age = header_property('Age', None, parse_date, http_date, doc='''
        The Age response-header field conveys the sender's estimate of the
        amount of time since the response (or its revalidation) was
        generated at the origin server.

        Age values are non-negative decimal integers, representing time in
        seconds.''')
    content_type = header_property('Content-Type', doc='''
        The Content-Type entity-header field indicates the media type of the
        entity-body sent to the recipient or, in the case of the HEAD method,
        the media type that would have been sent had the request been a GET.
    ''')
    content_length = header_property('Content-Length', None, int, str, doc='''
        The Content-Length entity-header field indicates the size of the
        entity-body, in decimal number of OCTETs, sent to the recipient or,
        in the case of the HEAD method, the size of the entity-body that would
        have been sent had the request been a GET.''')
    content_location = header_property('Content-Location', doc='''
        The Content-Location entity-header field MAY be used to supply the
        resource location for the entity enclosed in the message when that
        entity is accessible from a location separate from the requested
        resource's URI.''')
    content_encoding = header_property('Content-Encoding', doc='''
        The Content-Encoding entity-header field is used as a modifier to the
        media-type.  When present, its value indicates what additional content
        codings have been applied to the entity-body, and thus what decoding
        mechanisms must be applied in order to obtain the media-type
        referenced by the Content-Type header field.''')
    content_md5 = header_property('Content-MD5', doc='''
         The Content-MD5 entity-header field, as defined in RFC 1864, is an
         MD5 digest of the entity-body for the purpose of providing an
         end-to-end message integrity check (MIC) of the entity-body.  (Note:
         a MIC is good for detecting accidental modification of the
         entity-body in transit, but is not proof against malicious attacks.)
        ''')
    date = header_property('Date', None, parse_date, http_date, doc='''
        The Date general-header field represents the date and time at which
        the message was originated, having the same semantics as orig-date
        in RFC 822.''')
    expires = header_property('Expires', None, parse_date, http_date, doc='''
        The Expires entity-header field gives the date/time after which the
        response is considered stale. A stale cache entry may not normally be
        returned by a cache.''')
    last_modified = header_property('Last-Modified', None, parse_date,
                                    http_date, doc='''
        The Last-Modified entity-header field indicates the date and time at
        which the origin server believes the variant was last modified.''')

    def _get_retry_after(self):
        value = self.headers.get('retry-after')
        if value is None:
            return
        elif value.isdigit():
            return datetime.utcnow() + timedelta(seconds=int(value))
        return parse_date(value)
    def _set_retry_after(self, value):
        if value is None:
            if 'retry-after' in self.headers:
                del self.headers['retry-after']
            return
        elif isinstance(value, datetime):
            value = http_date(value)
        else:
            value = str(value)
        self.headers['Retry-After'] = value

    retry_after = property(_get_retry_after, _set_retry_after, doc='''
        The Retry-After response-header field can be used with a 503 (Service
        Unavailable) response to indicate how long the service is expected
        to be unavailable to the requesting client.

        Time in seconds until expiration or date.''')

    def _set_property(name, doc=None):
        def fget(self):
            def on_update(header_set):
                if not header_set and name in self.headers:
                    del self.headers[name]
                elif header_set:
                    self.headers[name] = header_set.to_header()
            return parse_set_header(self.headers.get(name), on_update)
        return property(fget, doc=doc)

    vary = _set_property('Vary', doc='''
         The Vary field value indicates the set of request-header fields that
         fully determines, while the response is fresh, whether a cache is
         permitted to use the response to reply to a subsequent request
         without revalidation.''')
    content_language = _set_property('Content-Language', doc='''
         The Content-Language entity-header field describes the natural
         language(s) of the intended audience for the enclosed entity.  Note
         that this might not be equivalent to all the languages used within
         the entity-body.''')
    allow = _set_property('Allow', doc='''
        The Allow entity-header field lists the set of methods supported
        by the resource identified by the Request-URI. The purpose of this
        field is strictly to inform the recipient of valid methods
        associated with the resource. An Allow header field MUST be
        present in a 405 (Method Not Allowed) response.''')

    del _set_property, _get_mimetype, _set_mimetype, _get_retry_after, \
        _set_retry_after


class WWWAuthenticateMixin(object):
    """Adds a :attr:`www_authenticate` property to a response object."""

    @property
    def www_authenticate(self):
        """The `WWW-Authenticate` header in a parsed form."""
        def on_update(www_auth):
            if not www_auth and 'www-authenticate' in self.headers:
                del self.headers['www-authenticate']
            elif www_auth:
                self.headers['WWW-Authenticate'] = www_auth.to_header()
        header = self.headers.get('www-authenticate')
        return parse_www_authenticate_header(header, on_update)


class Request(BaseRequest, AcceptMixin, ETagRequestMixin,
              UserAgentMixin, AuthorizationMixin,
              CommonRequestDescriptorsMixin):
    """Full featured request object implementing the following mixins:

    - :class:`AcceptMixin` for accept header parsing
    - :class:`ETagRequestMixin` for etag and cache control handling
    - :class:`UserAgentMixin` for user agent introspection
    - :class:`AuthorizationMixin` for http auth handling
    - :class:`CommonRequestDescriptorsMixin` for common headers
    """


class Response(BaseResponse, ETagResponseMixin, ResponseStreamMixin,
               CommonResponseDescriptorsMixin,
               WWWAuthenticateMixin):
    """Full featured response object implementing the following mixins:

    - :class:`ETagResponseMixin` for etag and cache control handling
    - :class:`ResponseStreamMixin` to add support for the `stream` property
    - :class:`CommonResponseDescriptorsMixin` for various HTTP descriptors
    - :class:`WWWAuthenticateMixin` for HTTP authentication support
    """
