"""
Routines related to sending a list of tiddlers out to the web,
including filter those tiddlers and validating request cache headers.
"""

from tiddlyweb.filters import FilterError, recursive_filter
from tiddlyweb.model.collections import Tiddlers
from tiddlyweb.serializer import Serializer, NoSerializationError
from tiddlyweb.util import sha
from tiddlyweb.web.util import \
        get_serialize_type, http_date_from_timestamp, datetime_from_http_date
from tiddlyweb.web.http import HTTP400, HTTP304, HTTP415


def send_tiddlers(environ, start_response, tiddlers=None):
    """
    Output the tiddlers contained in the provided
    bag in a Negotiated representation. Often, but
    not always, a wiki.
    """
    last_modified = None
    etag = None
    download = environ['tiddlyweb.query'].get('download', [None])[0]
    filters = environ['tiddlyweb.filters']
    store = environ['tiddlyweb.store']

    if filters:
        candidate_tiddlers = Tiddlers(store=store)
        try:
            candidate_tiddlers.title = tiddlers.title
            candidate_tiddlers.is_search = tiddlers.is_search
            candidate_tiddlers.is_revisions = tiddlers.is_revisions
        except AttributeError:
            pass
        try:
            for tiddler in recursive_filter(filters, tiddlers):
                recipe = tiddler.recipe
                if not tiddler.store:
                    tiddler = store.get(tiddler)
                    if recipe:
                        tiddler.recipe = recipe
                candidate_tiddlers.add(tiddler)
        except FilterError, exc:
            raise HTTP400('malformed filter: %s' % exc)
    else:
        if hasattr(tiddlers, 'modified'):
            candidate_tiddlers = tiddlers
        else:
            candidate_tiddlers = Tiddlers(store=store)
            # Don't need to worry about recipes here as this
            # branch can only happen when tiddlers have been loaded
            # via a bag.
            for tiddler in tiddlers:
                candidate_tiddlers.add(tiddler)

    last_modified, etag = _validate_tiddler_list(environ, candidate_tiddlers)

    serialize_type, mime_type = get_serialize_type(environ)

    content_header = ('Content-Type', mime_type)
    cache_header = ('Cache-Control', 'no-cache')
    vary_header = ('Vary', 'Accept')
    response = [content_header, cache_header, vary_header]

    if download:
        response.append(('Content-Disposition',
            'attachment; filename="%s"' % download.encode('utf-8')))

    if last_modified:
        response.append(last_modified)

    if etag:
        response.append(etag)

    try:
        serializer = Serializer(serialize_type, environ)
        output = serializer.list_tiddlers(candidate_tiddlers)
    except NoSerializationError, exc:
        raise HTTP415('Content type not supported: %s:%s, %s' %
                (serialize_type, mime_type, exc))

    start_response("200 OK", response)

    if isinstance(output, basestring):
        return [output]
    else:
        return output


def _validate_tiddler_list(environ, tiddlers):
    """
    Do Etag and Last modified checks on the
    collection of tiddlers.

    If ETag testing is done, no last modified handling
    is done, even if the ETag testing fails.

    If no 304 is raised, then just return last-modified
    and ETag for the caller to use in constructing
    its HTTP response.
    """
    last_modified_number = tiddlers.modified
    last_modified_string = http_date_from_timestamp(last_modified_number)
    last_modified = ('Last-Modified', last_modified_string)

    username = environ.get('tiddlyweb.usersign', {}).get('name', '')

    try:
        _, mime_type = get_serialize_type(environ)
        mime_type = mime_type.split(';', 1)[0].strip()
    except TypeError:
        mime_type = ''
    etag_string = '"%s:%s;%s"' % (tiddlers.hexdigest(),
            str(last_modified_number), sha('%s:%s' %
                (username, mime_type)).hexdigest())
    etag = ('Etag', etag_string)

    incoming_etag = environ.get('HTTP_IF_NONE_MATCH', None)
    if incoming_etag:
        if incoming_etag == etag_string:
            raise HTTP304(incoming_etag)
    else:
        incoming_modified = environ.get('HTTP_IF_MODIFIED_SINCE', None)
        if incoming_modified and \
                (datetime_from_http_date(incoming_modified) >= \
                datetime_from_http_date(last_modified_string)):
            raise HTTP304('')

    return last_modified, etag
