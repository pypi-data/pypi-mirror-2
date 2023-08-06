""" Utility functions for dealing with URLs in pyramid """

import os

from repoze.lru import lru_cache

from pyramid.interfaces import IContextURL
from pyramid.interfaces import IRoutesMapper
from pyramid.interfaces import IStaticURLInfo

from pyramid.encode import urlencode
from pyramid.path import caller_package
from pyramid.threadlocal import get_current_registry
from pyramid.traversal import TraversalContextURL
from pyramid.traversal import quote_path_segment

def route_url(route_name, request, *elements, **kw):
    """Generates a fully qualified URL for a named :app:`Pyramid`
    :term:`route configuration`.

    Use the route's ``name`` as the first positional argument.  Use a
    request object as the second positional argument.  Additional
    positional arguments are appended to the URL as path segments
    after it is generated.

    Use keyword arguments to supply values which match any dynamic
    path elements in the route definition.  Raises a :exc:`KeyError`
    exception if the URL cannot be generated for any reason (not
    enough arguments, for example).

    For example, if you've defined a route named "foobar" with the path
    ``:foo/:bar/*traverse``::

        route_url('foobar', request, foo='1')          => <KeyError exception>
        route_url('foobar', request, foo='1', bar='2') => <KeyError exception>
        route_url('foobar', request, foo='1', bar='2',
                  traverse=('a','b'))                  => http://e.com/1/2/a/b
        route_url('foobar', request, foo='1', bar='2',
                  traverse='/a/b')                     => http://e.com/1/2/a/b

    Values replacing ``:segment`` arguments can be passed as strings
    or Unicode objects.  They will be encoded to UTF-8 and URL-quoted
    before being placed into the generated URL.

    Values replacing ``*remainder`` arguments can be passed as strings
    *or* tuples of Unicode/string values.  If a tuple is passed as a
    ``*remainder`` replacement value, its values are URL-quoted and
    encoded to UTF-8.  The resulting strings are joined with slashes
    and rendered into the URL.  If a string is passed as a
    ``*remainder`` replacement value, it is tacked on to the URL
    untouched.

    If a keyword argument ``_query`` is present, it will used to
    compose a query string that will be tacked on to the end of the
    URL.  The value of ``_query`` must be a sequence of two-tuples
    *or* a data structure with an ``.items()`` method that returns a
    sequence of two-tuples (presumably a dictionary).  This data
    structure will be turned into a query string per the documentation
    of :func:`pyramid.encode.urlencode` function.  After the query
    data is turned into a query string, a leading ``?`` is prepended,
    and the resulting string is appended to the generated URL.

    .. note:: Python data structures that are passed as ``_query``
              which are sequences or dictionaries are turned into a
              string under the same rules as when run through
              :func:`urllib.urlencode` with the ``doseq`` argument
              equal to ``True``.  This means that sequences can be
              passed as values, and a k=v pair will be placed into the
              query string for each value.

    If a keyword argument ``_anchor`` is present, its string
    representation will be used as a named anchor in the generated URL
    (e.g. if ``_anchor`` is passed as ``foo`` and the model URL is
    ``http://example.com/model/url``, the resulting generated URL will
    be ``http://example.com/model/url#foo``).

    .. note:: If ``_anchor`` is passed as a string, it should be UTF-8
              encoded. If ``_anchor`` is passed as a Unicode object, it
              will be converted to UTF-8 before being appended to the
              URL.  The anchor value is not quoted in any way before
              being appended to the generated URL.

    If both ``_anchor`` and ``_query`` are specified, the anchor
    element will always follow the query element,
    e.g. ``http://example.com?foo=1#bar``.

    If a keyword ``_app_url`` is present, it will be used as the
    protocol/hostname/port/leading path prefix of the generated URL.
    For example, using an ``_app_url`` of
    ``http://example.com:8080/foo`` would cause the URL
    ``http://example.com:8080/foo/fleeb/flub`` to be returned from
    this function if the expansion of the route pattern associated
    with the ``route_name`` expanded to ``/fleeb/flub``.  If
    ``_app_url`` is not specified, the result of
    ``request.application_url`` will be used as the prefix (the
    default).

    This function raises a :exc:`KeyError` if the URL cannot be
    generated due to missing replacement names.  Extra replacement
    names are ignored.

    If the route object which matches the ``route_name`` argument has
    a :term:`pregenerator`, the ``*elements`` and ``**kw`` arguments
    arguments passed to this function might be augmented or changed.
    """
    try:
        reg = request.registry
    except AttributeError:
        reg = get_current_registry() # b/c
    mapper = reg.getUtility(IRoutesMapper)
    route = mapper.get_route(route_name)

    if route is None:
        raise KeyError('No such route named %s' % route_name)

    if route.pregenerator is not None:
        elements, kw = route.pregenerator(request, elements, kw)

    anchor = ''
    qs = ''
    app_url = None

    if '_query' in kw:
        qs = '?' + urlencode(kw.pop('_query'), doseq=True)

    if '_anchor' in kw:
        anchor = kw.pop('_anchor')
        if isinstance(anchor, unicode):
            anchor = anchor.encode('utf-8')
        anchor = '#' + anchor

    if '_app_url' in kw:
        app_url = kw.pop('_app_url')

    path = route.generate(kw) # raises KeyError if generate fails

    if elements:
        suffix = _join_elements(elements)
        if not path.endswith('/'):
            suffix = '/' + suffix
    else:
        suffix = ''

    if app_url is None:
        # we only defer lookup of application_url until here because
        # it's somewhat expensive; we won't need to do it if we've
        # been passed _app_url
        app_url = request.application_url

    return app_url + path + suffix + qs + anchor

def model_url(model, request, *elements, **kw):
    """
    Generate a string representing the absolute URL of the ``model``
    object based on the ``wsgi.url_scheme``, ``HTTP_HOST`` or
    ``SERVER_NAME`` in the ``request``, plus any ``SCRIPT_NAME``.  The
    overall result of this function is always a UTF-8 encoded string
    (never Unicode).

    Examples::

        model_url(context, request) =>

                                   http://example.com/

        model_url(context, request, 'a.html') =>

                                   http://example.com/a.html

        model_url(context, request, 'a.html', query={'q':'1'}) =>

                                   http://example.com/a.html?q=1

        model_url(context, request, 'a.html', anchor='abc') =>

                                   http://example.com/a.html#abc

    Any positional arguments passed in as ``elements`` must be strings
    or Unicode objects.  These will be joined by slashes and appended
    to the generated model URL.  Each of the elements passed in is
    URL-quoted before being appended; if any element is Unicode, it
    will converted to a UTF-8 bytestring before being URL-quoted.

    .. warning:: if no ``elements`` arguments are specified, the model
                 URL will end with a trailing slash.  If any
                 ``elements`` are used, the generated URL will *not*
                 end in trailing a slash.

    If a keyword argument ``query`` is present, it will used to
    compose a query string that will be tacked on to the end of the
    URL.  The value of ``query`` must be a sequence of two-tuples *or*
    a data structure with an ``.items()`` method that returns a
    sequence of two-tuples (presumably a dictionary).  This data
    structure will be turned into a query string per the documentation
    of ``repoze.url.urlencode`` function.  After the query data is
    turned into a query string, a leading ``?`` is prepended, and the
    resulting string is appended to the generated URL.

    .. note:: Python data structures that are passed as ``query``
              which are sequences or dictionaries are turned into a
              string under the same rules as when run through
              :func:`urllib.urlencode` with the ``doseq`` argument
              equal to ``True``.  This means that sequences can be
              passed as values, and a k=v pair will be placed into the
              query string for each value.

    If a keyword argument ``anchor`` is present, its string
    representation will be used as a named anchor in the generated URL
    (e.g. if ``anchor`` is passed as ``foo`` and the model URL is
    ``http://example.com/model/url``, the resulting generated URL will
    be ``http://example.com/model/url#foo``).

    .. note:: If ``anchor`` is passed as a string, it should be UTF-8
              encoded. If ``anchor`` is passed as a Unicode object, it
              will be converted to UTF-8 before being appended to the
              URL.  The anchor value is not quoted in any way before
              being appended to the generated URL.

    If both ``anchor`` and ``query`` are specified, the anchor element
    will always follow the query element,
    e.g. ``http://example.com?foo=1#bar``.

    .. note:: If the ``model`` used is the result of a
             :term:`traversal`, it must be :term:`location`-aware.
             The ``model`` can also be the context of a :term:`URL
             dispatch`; contexts found this way do not need to be
             location-aware.

    .. note:: If a 'virtual root path' is present in the request
              environment (the value of the WSGI environ key
              ``HTTP_X_VHM_ROOT``), and the ``model`` was obtained via
              :term:`traversal`, the URL path will not include the
              virtual root prefix (it will be stripped off the
              left hand side of the generated URL).
    """
    try:
        reg = request.registry
    except AttributeError:
        reg = get_current_registry() # b/c
    
    context_url = reg.queryMultiAdapter((model, request), IContextURL)
    if context_url is None:
        context_url = TraversalContextURL(model, request)
    model_url = context_url()

    qs = ''
    anchor = ''

    if 'query' in kw:
        qs = '?' + urlencode(kw['query'], doseq=True)

    if 'anchor' in kw:
        anchor = kw['anchor']
        if isinstance(anchor, unicode):
            anchor = anchor.encode('utf-8')
        anchor = '#' + anchor

    if elements:
        suffix = _join_elements(elements)
    else:
        suffix = ''

    return model_url + suffix + qs + anchor

def static_url(path, request, **kw):
    """
    Generates a fully qualified URL for a static :term:`resource`.
    The resource must live within a location defined via the
    :meth:`pyramid.configuration.Configurator.add_static_view`
    :term:`configuration declaration` or the ``<static>`` ZCML
    directive (see :ref:`static_resources_section`).

    Example::

        static_url('mypackage:static/foo.css', request) =>

                                http://example.com/static/foo.css


    The ``path`` argument points at a file or directory on disk which
    a URL should be generated for.  The ``path`` may be either a
    relative path (e.g. ``static/foo.css``) or a :term:`resource
    specification` (e.g. ``mypackage:static/foo.css``).  A ``path``
    may not be an absolute filesystem path (a :exc:`ValueError` will
    be raised if this function is supplied with an absolute path).

    The ``request`` argument should be a :term:`request` object.

    The purpose of the ``**kw`` argument is the same as the purpose of
    the :func:`pyramid.url.route_url` ``**kw`` argument.  See the
    documentation for that function to understand the arguments which
    you can provide to it.  However, typically, you don't need to pass
    anything as ``*kw`` when generating a static resource URL.

    This function raises a :exc:`ValueError` if a static view
    definition cannot be found which matches the path specification.

    """
    if os.path.isabs(path):
        raise ValueError('Absolute paths cannot be used to generate static '
                         'urls (use a package-relative path or a resource '
                         'specification).')
    if not ':' in path:
        # if it's not a package:relative/name and it's not an
        # /absolute/path it's a relative/path; this means its relative
        # to the package in which the caller's module is defined.
        package = caller_package()
        path = '%s:%s' % (package.__name__, path)

    try:
        reg = request.registry
    except AttributeError:
        reg = get_current_registry() # b/c
    
    info = reg.queryUtility(IStaticURLInfo)
    if info is None:
        raise ValueError('No static URL definition matching %s' % path)
        
    return info.generate(path, request, **kw)

@lru_cache(1000)
def _join_elements(elements):
    return '/'.join([quote_path_segment(s) for s in elements])
