# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Base classes for HTTP resources."""

__metaclass__ = type

__all__ = [
    'BatchingResourceMixin',
    'Collection',
    'CollectionResource',
    'Entry',
    'EntryAdapterUtility',
    'EntryField',
    'EntryFieldResource',
    'EntryHTMLView',
    'EntryResource',
    'HTTPResource',
    'JSONItem',
    'ReadOnlyResource',
    'RedirectResource',
    'register_versioned_request_utility',
    'render_field_to_html',
    'ResourceJSONEncoder',
    'RESTUtilityBase',
    'ScopedCollection',
    'ServiceRootResource',
    'WADL_SCHEMA_FILE',
    ]


import cgi
import copy
from cStringIO import StringIO
from datetime import datetime, date
from email.Utils import formatdate
from gzip import GzipFile
import os
import simplejson
import time
import zlib

# Import SHA in a way compatible with both Python 2.4 and Python 2.6.
try:
    import hashlib
    sha_constructor = hashlib.sha1
except ImportError:
     import sha
     sha_constructor = sha.new

from zope.app.pagetemplate.engine import TrustedAppPT
from zope import component
from zope.component import (
    adapts, getAdapters, getAllUtilitiesRegisteredFor,
    getGlobalSiteManager, getMultiAdapter, getSiteManager, getUtility,
    queryMultiAdapter)
from zope.component.interfaces import ComponentLookupError
from zope.event import notify
from zope.publisher.http import init_status_codes, status_reasons
from zope.interface import (
    alsoProvides, implementer, implements, implementedBy, providedBy,
    Interface)
from zope.interface.common.sequence import IFiniteSequence
from zope.interface.interfaces import IInterface
from zope.location.interfaces import ILocation
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.proxy import isProxy
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema import ValidationError, getFieldsInOrder
from zope.schema.interfaces import (
    ConstraintNotSatisfied, IBytes, IField, IObject, RequiredMissing)
from zope.security.interfaces import Unauthorized
from zope.security.proxy import removeSecurityProxy
from zope.security.management import checkPermission
from zope.traversing.browser import absoluteURL, AbsoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL

from lazr.batchnavigator import BatchNavigator
from lazr.delegates import Passthrough
from lazr.enum import BaseItem
from lazr.lifecycle.event import ObjectModifiedEvent
from lazr.lifecycle.snapshot import Snapshot

from lazr.restful.interfaces import (
    ICollection, ICollectionField, ICollectionResource, IEntry, IEntryField,
    IEntryFieldResource, IEntryResource, IFieldHTMLRenderer, IFieldMarshaller,
    IHTTPResource, IJSONPublishable, IReferenceChoice,
    IResourceDELETEOperation, IResourceGETOperation, IResourcePOSTOperation,
    IScopedCollection, IServiceRootResource, ITopLevelEntryLink,
    IUnmarshallingDoesntNeedValue, IWebServiceClientRequest,
    IWebServiceConfiguration, IWebServiceLayer, IWebServiceVersion,
    LAZR_WEBSERVICE_NAME)
from lazr.restful.utils import get_current_web_service_request


# The path to the WADL XML Schema definition.
WADL_SCHEMA_FILE = os.path.join(os.path.dirname(__file__),
                                'wadl20061109.xsd')

# Levels of detail to use when unmarshalling the data.
NORMAL_DETAIL = object()
CLOSEUP_DETAIL = object()

# XXX leonardr 2009-01-29
# bug=https://bugs.edge.launchpad.net/zope3/+bug/322486:
# Add nonstandard status methods to Zope's status_reasons dictionary.
for code, reason in [(209, 'Content Returned')]:
    if not code in status_reasons:
        status_reasons[code] = reason
init_status_codes()

def decode_value(value):
    """Return a unicode value curresponding to `value`."""
    if isinstance(value, unicode):
        return value
    elif isinstance(value, str):
        return value.decode("utf-8")
    else:
        return unicode(value)


def register_versioned_request_utility(interface, version):
    """Registers a marker interface as a utility for version lookup.

    This function registers the given interface class as the
    IWebServiceVersion utility for the given version string.
    """
    alsoProvides(interface, IWebServiceVersion)
    getSiteManager().registerUtility(
        interface, IWebServiceVersion, name=version)


class LazrPageTemplateFile(TrustedAppPT, PageTemplateFile):
    "A page template class for generating web service-related documents."
    pass


class ResourceJSONEncoder(simplejson.JSONEncoder):
    """A JSON encoder for JSON-exposable resources like entry resources.

    This class works with simplejson to encode objects as JSON if they
    implement IJSONPublishable. All EntryResource subclasses, for
    instance, should implement IJSONPublishable.
    """

    def default(self, obj):
        """Convert the given object to a simple data structure."""
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        if isProxy(obj):
            # We have a security-proxied version of a built-in
            # type. We create a new version of the type by copying the
            # proxied version's content. That way the container is not
            # security proxied (and simplejson will know what do do
            # with it), but the content will still be security
            # wrapped.
            underlying_object = removeSecurityProxy(obj)
            if isinstance(underlying_object, list):
                return list(obj)
            if isinstance(underlying_object, tuple):
                return tuple(obj)
            if isinstance(underlying_object, dict):
                return dict(obj)
        request = get_current_web_service_request()
        if queryMultiAdapter((obj, request), IEntry):
            obj = EntryResource(obj, request)

        return IJSONPublishable(obj).toDataForJSON()


class JSONItem:
    """JSONPublishable adapter for lazr.enum."""
    implements(IJSONPublishable)
    adapts(BaseItem)

    def __init__(self, context):
        self.context = context

    def toDataForJSON(self):
        """See `ISJONPublishable`"""
        return str(self.context.title)


class RedirectResource:
    """A resource that redirects to another URL."""
    implements(IHTTPResource)

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def __call__(self):
        url = self.url
        self.request.response.setStatus(301)
        self.request.response.setHeader("Location", url)


class HTTPResource:
    """See `IHTTPResource`."""
    implements(IHTTPResource)

    # Some interesting media types.
    WADL_TYPE = 'application/vnd.sun.wadl+xml'
    JSON_TYPE = 'application/json'
    XHTML_TYPE = 'application/xhtml+xml'

    # This misspelling of the WADL media type was used for a while,
    # and lazr.restful still supports it to avoid breaking clients
    # that depend on it.
    DEPRECATED_WADL_TYPE = 'application/vd.sun.wadl+xml'

    # A preparsed template file for WADL representations of resources.
    WADL_TEMPLATE = LazrPageTemplateFile('templates/wadl-resource.pt')

    HTTP_METHOD_OVERRIDE_ERROR = ("X-HTTP-Method-Override can only be used "
                                  "with a POST request.")

    # All resources serve WADL and JSON representations. Only entry
    # resources serve XHTML representations.
    SUPPORTED_CONTENT_TYPES = [WADL_TYPE, DEPRECATED_WADL_TYPE, JSON_TYPE]

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.etags_by_media_type = {}

    def __call__(self):
        """See `IHTTPResource`."""
        pass

    def getRequestMethod(self, request=None):
        """Return the HTTP method of the provided (or current) request.

        This is usually the actual HTTP method, but it might be
        overridden by a value for X-HTTP-Method-Override.

        :return: None if the valid for X-HTTP-Method-Override is invalid.
        Otherwise, the HTTP method to use.
        """
        if request == None:
            request = self.request
        override = request.headers.get('X-HTTP-Method-Override')
        if override is not None:
            if request.method == 'POST':
                return override
            else:
                # XHMO should not be used unless the underlying method
                # is POST.
                self.request.response.setStatus(400)
                return None
        return request.method

    def handleConditionalGET(self):
        """Handle a possible conditional GET request.

        This method has side effects. If the resource provides a
        generated ETag, it sets this value as the "ETag" response
        header. If the "ETag" request header matches the generated
        ETag, it sets the response code to 304 ("Not Modified").

        :return: The media type to serve. If this value is None, the
            incoming ETag matched the generated ETag and there is no
            need to serve anything else.
        """
        incoming_etags = self._parseETags('If-None-Match')

        media_type = self.getPreferredSupportedContentType()
        existing_etag = self.getETag(media_type)
        if existing_etag is not None:
            self.request.response.setHeader('ETag', existing_etag)
            if existing_etag in incoming_etags:
                # The client already has this representation.
                # No need to send it again.
                self.request.response.setStatus(304) # Not Modified
                media_type = None
        return media_type

    def handleConditionalWrite(self):
        """Handle a possible conditional PUT or PATCH request.

        This method has side effects. If the write operation should
        not continue, because the incoming ETag doesn't match the
        generated ETag, it sets the response code to 412 ("Precondition
        Failed"). Whether or not the two ETags 'match' depends on the
        resource-specific implementation, but by default two ETags
        only 'match' if they are identical.

        If the PUT or PATCH request is being tunneled through POST
        with X-HTTP-Method-Override, the media type of the incoming
        representation will be obtained from X-Content-Type-Override
        instead of Content-Type, should X-C-T-O be provided.

        :return: The media type of the incoming representation. If
            this value is None, the incoming ETag didn't match the
            generated ETag and the incoming representation should be
            ignored.
        """
        media_type = self.request.headers.get('X-Content-Type-Override')
        if media_type is not None:
            if self.request.method != 'POST':
                # X-C-T-O should not be used unless the underlying
                # method is POST. Set response code 400 ("Bad
                # Request").
                self.request.response.setStatus(400)
                return None
        else:
            media_type = self.request.headers.get(
                'Content-Type', self.JSON_TYPE)

        incoming_etags = self._parseETags('If-Match')
        if len(incoming_etags) == 0:
            # This is not a conditional write.
            return media_type
        existing_etag = self.getETag(media_type)
        if self._etagMatchesForWrite(existing_etag, incoming_etags):
            # The conditional write can continue.
            return media_type
        # The resource has changed since the client requested it.
        # Don't let the write go through. Set response code 412
        # ("Precondition Failed")
        self.request.response.setStatus(412)
        return None

    def _etagMatchesForWrite(self, existing_etag, incoming_etags):
        """Perform an ETag match to see if conditional write is OK.

        By default, we match the full ETag strings against each other.
        """
        return existing_etag in incoming_etags

    def _getETagCores(self, cache=None):
        """Calculate the core ETag for a representation.

        :return: a list of strings that will be used to calculate the
            full ETag. If None is returned, no ETag at all will be
            calculated for the given resource and media type.
        """
        return None

    def getETag(self, media_type, cache=None):
        """Calculate the ETag for an entry.

        An ETag is derived from a 'core' string conveying information
        about the representation itself, plus information about the
        content type and the current Launchpad revision number. The
        resulting string is hashed, and there's your ETag.

        :arg unmarshalled_field_values: A dict mapping field names to
            unmarshalled values, obtained during some other operation
            such as the construction of a representation.
        """
        # Try to find a cached value.
        etag = self.etags_by_media_type.get(media_type)
        if etag is not None:
            return etag

        if media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            # The WADL representation of a resource only changes when
            # the software itself changes. Thus, we don't need any
            # special information for its ETag core.
            etag_cores = ['']
        else:
            # For other media types, we calculate the ETag core by
            # delegating to the subclass.
            etag_cores = self._getETagCores(cache)

        if etag_cores is None:
            return None

        core_hashes = []
        for core in etag_cores:
            hash_object = sha_constructor()
            hash_object.update(core)
            core_hashes.append(hash_object)

        # Append the media type, so that web browsers won't treat
        # different representations of a resource interchangeably.
        core_hashes[-1].update("\0" + media_type)

        # Append the revision number, because the algorithm for
        # generating the representation might itself change across
        # versions.
        revno = getUtility(IWebServiceConfiguration).code_revision
        core_hashes[-1].update("\0" + revno)

        etag = '"%s"' % "-".join([core.hexdigest() for core in core_hashes])
        self.etags_by_media_type[media_type] = etag
        return etag

    def implementsPOST(self):
        """Returns True if this resource will respond to POST.

        Right now this means the resource has defined one or more
        custom POST operations.
        """
        adapters = list(
            getAdapters((self.context, self.request), IResourcePOSTOperation))
        return len(adapters) > 0

    def implementsDELETE(self):
        """Returns True if this resource will respond to DELETE."""
        adapters = list(
            getAdapters(
                (self.context, self.request), IResourceDELETEOperation))
        assert len(adapters) < 2, ("%s has more than one registered DELETE "
                                   "handler." % self.context.__class__)
        return len(adapters) > 0

    def toWADL(self):
        """Represent this resource as a WADL application.

        The WADL document describes the capabilities of this resource.
        """
        namespace = self.WADL_TEMPLATE.pt_getContext()
        namespace['context'] = self
        return self.WADL_TEMPLATE.pt_render(namespace)

    def getPreferredSupportedContentType(self):
        """Of the content types we serve, which would the client prefer?

        The web service supports WADL, XHTML, and JSON
        representations. If no supported media type is requested, JSON
        is the default. This method determines whether the client
        would rather have WADL, XHTML, or JSON.
        """
        content_types = self.getPreferredContentTypes()
        preferences = []
        winner = None
        for media_type in self.SUPPORTED_CONTENT_TYPES:
            try:
                pos = content_types.index(media_type)
                if winner is None or pos < winner[1]:
                    winner = (media_type, pos)
            except ValueError:
                pass
        if winner is None:
            return self.JSON_TYPE
        else:
            return winner[0]

    def getPreferredContentTypes(self):
        """Find which content types the client prefers to receive."""
        accept_header = (self.request.form.pop('ws.accept', None)
            or self.request.get('HTTP_ACCEPT'))
        return self._parseAcceptStyleHeader(accept_header)

    def _parseETags(self, header_name):
        """Extract a list of ETags from a header and parse the list.

        RFC2616 allows multiple comma-separated ETags.

        If the compensate_for_mod_compress_etag_modification value is set,
        ETags like '"foo"-gzip' and '"foo-gzip"' will be transformed into
        '"foo"'.
        """
        header = self.request.getHeader(header_name)
        if header is None:
            return []
        utility = getUtility(IWebServiceConfiguration)
        strip_gzip_from_etag = (
            utility.compensate_for_mod_compress_etag_modification)
        etags = []
        # We're kind of cheating, because entity tags can technically
        # have commas in them, but none of our tags contain commas, so
        # this will work.
        for etag in header.split(','):
            etag = etag.strip()
            if strip_gzip_from_etag:
                if etag.endswith('-gzip'):
                    etag = etag[:-5]
                elif etag.endswith('-gzip"'):
                    etag = etag[:-6] + '"'
            etags.append(etag)
        return etags

    def _fieldValueIsObject(self, field):
        """Does the given field expect a data model object as its value?

        Obviously an IObject field is expected to have a data model
        object as its value. But an IChoice field might also have a
        vocabulary drawn from the set of data model objects.
        """
        return (IObject.providedBy(field)
                or IReferenceChoice.providedBy(field))

    def _parseContentDispositionHeader(self, value):
        """Parse a Content-Disposition header.

        :return: a 2-tuple (disposition-type, disposition-params).
        disposition-params is a dict mapping parameter names to values.
        """
        disposition = None
        params = {}
        if value is None:
            return (disposition, params)
        pieces = value.split(';')
        if len(pieces) > 1:
            disposition = pieces[0].strip()
        for name_value in pieces[1:]:
            name_and_value = name_value.split('=', 2)
            if len(name_and_value) == 2:
                name = name_and_value[0].strip()
                value = name_and_value[1].strip()
                # Strip quotation marks if present. RFC2183 gives
                # guidelines for when to quote these values, but it's
                # very likely that a client will quote even short
                # filenames, and unlikely that a filename will
                # actually begin and end with quotes.
                if (value[0] == '"' and value[-1] == '"'):
                    value = value[1:-1]
            else:
                name = name_and_value
                value = None
            params[name] = value
        return (disposition, params)

    def _parseAcceptStyleHeader(self, value):
        """Parse an HTTP header from the Accept-* family.

        These headers contain a list of possible values, each with an
        optional priority.

        This code is modified from Zope's
        BrowserLanguages#getPreferredLanguages.

        :return: All values, in descending order of priority.
        """
        if value is None:
            return []

        values = value.split(',')
        # In the original getPreferredLanguages there was some language
        # code normalization here, which I removed.
        values = [v for v in values if v != ""]

        accepts = []
        for index, value in enumerate(values):
            l = value.split(';', 2)

            # If not supplied, quality defaults to 1...
            quality = 1.0

            if len(l) == 2:
                q = l[1]
                if q.startswith('q='):
                    q = q.split('=', 2)[1]
                    quality = float(q)

            if quality == 1.0:
                # ... but we use 1.9 - 0.001 * position to
                # keep the ordering between all items with
                # 1.0 quality, which may include items with no quality
                # defined, and items with quality defined as 1.
                quality = 1.9 - (0.001 * index)

            accepts.append((quality, l[0].strip()))

        accepts = [acc for acc in accepts if acc[0] > 0]
        accepts.sort()
        accepts.reverse()
        return [value for quality, value in accepts]


class WebServiceBatchNavigator(BatchNavigator):
    """A batch navigator that speaks to web service clients.

    This batch navigator differs from others in the names of the query
    variables it expects. This class expects the starting point to be
    contained in the query variable "ws.start" and the size of the
    batch to be contained in the query variable "ws.size". When this
    navigator serves links, it includes query variables by those
    names.
    """

    start_variable_name = "ws.start"
    batch_variable_name = "ws.size"

    @property
    def default_batch_size(self):
        return getUtility(IWebServiceConfiguration).default_batch_size

    @property
    def max_batch_size(self):
        return getUtility(IWebServiceConfiguration).max_batch_size


class BatchingResourceMixin:

    """A mixin for resources that need to batch lists of entries."""

    def __init__(self, context, request):
        """A basic constructor."""
        # Like all mixin classes, this class is designed to be used
        # with multiple inheritance. That requires defining __init__
        # to call the next constructor in the chain, which means using
        # super() even though this class itself has no superclass.
        super(BatchingResourceMixin, self).__init__(context, request)

    def batch(self, entries, request):
        """Prepare a batch from a (possibly huge) list of entries.

        :return: A hash:
        'entries' contains a list of EntryResource objects for the
          entries that actually made it into this batch
        'total_size' contains the total size of the list.
        'next_url', if present, contains a URL to get the next batch
         in the list.
        'prev_url', if present, contains a URL to get the previous batch
         in the list.
        'start' contains the starting index of this batch
        """
        if not hasattr(entries, '__len__'):
            entries = IFiniteSequence(entries)
        navigator = WebServiceBatchNavigator(entries, request)

        view_permission = getUtility(IWebServiceConfiguration).view_permission
        resources = [EntryResource(entry, request)
                     for entry in navigator.batch
                     if checkPermission(view_permission, entry)]
        batch = { 'entries' : resources,
                  'total_size' : navigator.batch.listlength,
                  'start' : navigator.batch.start }
        if navigator.batch.start < 0:
            batch['start'] = None
        next_url = navigator.nextBatchURL()
        if next_url != "":
            batch['next_collection_link'] = next_url
        prev_url = navigator.prevBatchURL()
        if prev_url != "":
            batch['prev_collection_link'] = prev_url
        return batch


class CustomOperationResourceMixin:

    """A mixin for resources that implement a collection-entry pattern."""

    def __init__(self, context, request):
        """A basic constructor."""
        # Like all mixin classes, this class is designed to be used
        # with multiple inheritance. That requires defining __init__
        # to call the next constructor in the chain, which means using
        # super() even though this class itself has no superclass.
        super(CustomOperationResourceMixin, self).__init__(context, request)

    def handleCustomGET(self, operation_name):
        """Execute a custom search-type operation triggered through GET.

        This is used by both EntryResource and CollectionResource.

        :param operation_name: The name of the operation to invoke.
        :return: The result of the operation: either a string or an
        object that needs to be serialized to JSON.
        """
        try:
            operation = getMultiAdapter((self.context, self.request),
                                        IResourceGETOperation,
                                        name=operation_name)
        except ComponentLookupError:
            self.request.response.setStatus(400)
            return "No such operation: " + operation_name
        return operation()

    def handleCustomPOST(self, operation_name):
        """Execute a custom write-type operation triggered through POST.

        This is used by both EntryResource and CollectionResource.

        :param operation_name: The name of the operation to invoke.
        :return: The result of the operation: either a string or an
        object that needs to be serialized to JSON.
        """
        try:
            operation = getMultiAdapter((self.context, self.request),
                                        IResourcePOSTOperation,
                                        name=operation_name)
        except ComponentLookupError:
            self.request.response.setStatus(400)
            return "No such operation: " + operation_name
        return operation()

    def do_POST(self):
        """Invoke a custom operation.

        XXX leonardr 2008-04-01 bug=210265:
        The standard meaning of POST (ie. when no custom operation is
        specified) is "create a new subordinate resource."  Code
        should eventually go into CollectionResource that implements
        POST to create a new entry inside the collection.
        """
        operation_name = self.request.form.get('ws.op')
        if operation_name is None:
            self.request.response.setStatus(400)
            return "No operation name given."
        del self.request.form['ws.op']
        return self.handleCustomPOST(operation_name)

    def do_DELETE(self):
        """Invoke a destructor operation."""
        try:
            operation = getMultiAdapter((self.context, self.request),
                                        IResourceDELETEOperation)
        except ComponentLookupError:
            # This should never happen because implementsDELETE()
            # makes sure there is a registered
            # IResourceDELETEOperation.
            self.request.response.setStatus(405)
            return "DELETE not supported."
        return operation()

        return operation()


class FieldUnmarshallerMixin:

    """A class that needs to unmarshall field values."""

    # The representation value used when the client doesn't have
    # authorization to see the real value.
    REDACTED_VALUE = 'tag:launchpad.net:2008:redacted'

    def __init__(self, context, request):
        """A basic constructor."""
        # Like all mixin classes, this class is designed to be used
        # with multiple inheritance. That requires defining __init__
        # to call the next constructor in the chain, which means using
        # super() even though this class itself has no superclass.
        super(FieldUnmarshallerMixin, self).__init__(context, request)
        self._unmarshalled_field_cache = {}

    def _unmarshallField(self, field_name, field, detail=NORMAL_DETAIL):
        """See what a field would look like in a generic representation.

        :return: a 2-tuple (representation_name, representation_value).
        """
        missing = object()
        cached_value = missing
        if detail is NORMAL_DETAIL:
            cached_value = self._unmarshalled_field_cache.get(
                field_name, missing)
        if cached_value is not missing:
            return cached_value

        field = field.bind(self.context)
        marshaller = getMultiAdapter((field, self.request), IFieldMarshaller)
        try:
            if IUnmarshallingDoesntNeedValue.providedBy(marshaller):
                value = None
            else:
                value = getattr(self.entry, field.__name__)
            if detail is NORMAL_DETAIL:
                repr_value = marshaller.unmarshall(self.entry, value)
            elif detail is CLOSEUP_DETAIL:
                repr_value = marshaller.unmarshall_to_closeup(
                    self.entry, value)
            else:
                raise AssertionError("Invalid level of detail specified")
        except Unauthorized:
            # Either the client doesn't have permission to see
            # this field, or it doesn't have permission to read
            # its current value. Rather than denying the client
            # access to the resource altogether, use our special
            # 'redacted' tag: URI for the field's value.
            repr_value = self.REDACTED_VALUE

        unmarshalled = (marshaller.representation_name, repr_value)

        if detail is NORMAL_DETAIL:
            self._unmarshalled_field_cache[field_name] = unmarshalled
        return unmarshalled

    def unmarshallFieldToHTML(self, field_name, field):
        """See what a field would look like in an HTML representation.

        This is usually similar to the value of _unmarshallField(),
        but it might contain some custom HTML weirdness.

        :return: a 2-tuple (representation_name, representation_value).
        """
        name, value = self._unmarshallField(field_name, field)
        try:
            # Try to get a renderer for this particular field.
            renderer = getMultiAdapter(
                (self.entry.context, field, self.request),
                IFieldHTMLRenderer, name=field.__name__)
        except ComponentLookupError:
            # There's no field-specific renderer. Look up an
            # IFieldHTMLRenderer for this _type_ of field.
            field = field.bind(self.entry.context)
            renderer = getMultiAdapter(
                (self.entry.context, field, self.request),
                IFieldHTMLRenderer)
        return name, renderer(value)


@component.adapter(Interface, IField, IWebServiceClientRequest)
@implementer(IFieldHTMLRenderer)
def render_field_to_html(object, field, request):
    """Turn a field's current value into an XHTML snippet.

    This is the default adapter for IFieldHTMLRenderer.
    """
    def unmarshall(value):
        return cgi.escape(unicode(value).encode("utf-8"))
    return unmarshall


class ReadOnlyResource(HTTPResource):
    """A resource that serves a string in response to GET."""

    def __init__(self, context, request):
        """A basic constructor."""
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super(ReadOnlyResource, self).__init__(context, request)

    def __call__(self):
        """Handle a GET or (if implemented) POST request."""
        result = ""
        method = self.getRequestMethod()
        if method is None:
            result = self.HTTP_METHOD_OVERRIDE_ERROR
        elif method == "GET":
            result = self.do_GET()
        elif method == "POST" and self.implementsPOST():
            result = self.do_POST()
        else:
            allow_string = "GET"
            if self.implementsPOST():
                allow_string += " POST"
            self.request.response.setStatus(405)
            self.request.response.setHeader("Allow", allow_string)
        return result


class ReadWriteResource(HTTPResource):
    """A resource that responds to GET, PUT, and PATCH."""

    def __init__(self, context, request):
        """A basic constructor."""
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super(ReadWriteResource, self).__init__(context, request)

    def __call__(self):
        """Handle a GET, PUT, or PATCH request."""
        result = ""
        method = self.getRequestMethod()
        if method is None:
            result = self.HTTP_METHOD_OVERRIDE_ERROR
        elif method == "GET":
            result = self.do_GET()
        elif method in ["PUT", "PATCH"]:
            media_type = self.handleConditionalWrite()
            if media_type is not None:
                stream = self.request.bodyStream
                representation = stream.getCacheStream().read()
                if method == "PUT":
                    result = self.do_PUT(media_type, representation)
                else:
                    result = self.do_PATCH(media_type, representation)
        elif method == "POST" and self.implementsPOST():
            result = self.do_POST()
        elif method == "DELETE" and self.implementsDELETE():
            result = self.do_DELETE()
        else:
            allow_string = "GET PUT PATCH"
            if self.implementsPOST():
                allow_string += " POST"
            if self.implementsDELETE():
                allow_string += " DELETE"
            self.request.response.setStatus(405)
            self.request.response.setHeader("Allow", allow_string)
        return result


class EntryHTMLView:
    """An HTML view of an entry."""

    # A preparsed template file for HTML representations of the resource.
    HTML_TEMPLATE = LazrPageTemplateFile('templates/html-resource.pt')

    def __init__(self, context, request):
        """Initialize with respect to a data object and request."""
        self.context = context
        self.request = request
        self.resource = EntryResource(context, request)

    def __call__(self):
        """Send the entry data through an HTML template."""
        namespace = self.HTML_TEMPLATE.pt_getContext()
        names_and_values = self.resource.toDataStructure(
            HTTPResource.XHTML_TYPE).items()
        data = [{'name' : name, 'value': decode_value(value)}
                for name, value in names_and_values]
        namespace['context'] = sorted(data)
        return self.HTML_TEMPLATE.pt_render(namespace)


class EntryManipulatingResource(ReadWriteResource):
    """A resource that manipulates some aspect of an entry."""

    def __init__(self, context, request):
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super(EntryManipulatingResource, self).__init__(context, request)

    def processAsJSONDocument(self, media_type, representation):
        """Process an incoming representation as a JSON document."""
        if not media_type.startswith(self.JSON_TYPE):
            self.request.response.setStatus(415)
            return None, 'Expected a media type of %s.' % self.JSON_TYPE
        try:
            h = simplejson.loads(representation.decode('utf-8'))
        except ValueError:
            self.request.response.setStatus(400)
            return None, "Entity-body was not a well-formed JSON document."
        return h, None

    def applyChanges(self, changeset):
        """Apply a dictionary of key-value pairs as changes to an entry.

        :param changeset: A dictionary. Should come from an incoming
        representation.

        :return: If there was an error, a string error message to be
        propagated to the client.
        """
        changeset = copy.copy(changeset)
        validated_changeset = []
        errors = []

        # The self link and resource type link aren't part of the
        # schema, so they're handled separately.
        modified_read_only_attribute = ("%s: You tried to modify a "
                                        "read-only attribute.")
        if 'self_link' in changeset:
            if changeset['self_link'] != absoluteURL(self.entry.context,
                                                     self.request):
                errors.append(modified_read_only_attribute % 'self_link')
            del changeset['self_link']

        if 'resource_type_link' in changeset:
            if changeset['resource_type_link'] != self.type_url:
                errors.append(modified_read_only_attribute %
                              'resource_type_link')
            del changeset['resource_type_link']

        if 'http_etag' in changeset:
            if changeset['http_etag'] != self.getETag(self.JSON_TYPE):
                errors.append(modified_read_only_attribute %
                              'http_etag')
            del changeset['http_etag']

        # For every field in the schema, see if there's a corresponding
        # field in the changeset.
        for name, field in get_entry_fields_in_write_order(self.entry):
            field = field.bind(self.entry.context)
            marshaller = getMultiAdapter((field, self.request),
                                         IFieldMarshaller)
            repr_name = marshaller.representation_name
            if not repr_name in changeset:
                # The client didn't try to set a value for this field.
                continue

            # Obtain the current value of the field, as it would be
            # shown in an outgoing representation. This gives us an easy
            # way to see if the client changed the value.
            try:
                current_value = marshaller.unmarshall(
                    self.entry, getattr(self.entry, name))
            except Unauthorized:
                # The client doesn't have permission to see the old
                # value. That doesn't necessarily mean they can't set
                # it to a new value, but it does mean we have to
                # assume they're changing it rather than see for sure
                # by comparing the old value to the new.
                current_value = self.REDACTED_VALUE

            # The client tried to set a value for this field. Marshall
            # it, validate it, and (if it's different from the current
            # value) move it from the client changeset to the
            # validated changeset.
            original_value = changeset.pop(repr_name)
            if original_value == current_value == self.REDACTED_VALUE:
                # The client can't see the field's current value, and
                # isn't trying to change it. Skip to the next field.
                continue

            try:
                value = marshaller.marshall_from_json_data(original_value)
            except (ValueError, ValidationError), e:
                errors.append("%s: %s" % (repr_name, e))
                continue

            if ICollectionField.providedBy(field):
                # This is a collection field, so the most we can do is set an
                # error message if the new value is not identical to the
                # current one.
                if value != current_value:
                    errors.append("%s: You tried to modify a collection "
                                  "attribute." % repr_name)
                continue

            if IBytes.providedBy(field):
                # We don't modify Bytes fields from the Entry that contains
                # them, but we may tell users how to do so if they attempt to
                # change them.
                if value != current_value:
                    if field.readonly:
                        errors.append(modified_read_only_attribute
                                      % repr_name)
                    else:
                        errors.append(
                            "%s: To modify this field you need to send a PUT "
                            "request to its URI (%s)."
                            % (repr_name, current_value))
                continue

            # If the new value is an object, make sure it provides the correct
            # interface.
            if value is not None and IObject.providedBy(field):
                # XXX leonardr 2008-04-12 spec=api-wadl-description:
                # This should be moved into the
                # ObjectLookupFieldMarshaller, once we make it
                # possible for Vocabulary fields to specify a schema
                # class the way IObject fields can.
                if value != None and not field.schema.providedBy(value):
                    errors.append("%s: Your value points to the "
                                  "wrong kind of object" % repr_name)
                    continue

            # Obtain the current value of the field.  This gives us an easy
            # way to see if the client changed the value.
            current_value = getattr(self.entry, name)

            change_this_field = True
            # Read-only attributes can't be modified. It's okay to specify a
            # value for an attribute that can't be modified, but the new value
            # must be the same as the current value.  This makes it possible
            # to GET a document, modify one field, and send it back.
            if field.readonly:
                change_this_field = False
                if value != current_value:
                    errors.append(modified_read_only_attribute
                                  % repr_name)
                    continue

            if change_this_field is True and value != current_value:
                if not IObject.providedBy(field):
                    # We don't validate IObject values because that
                    # can lead to infinite recursion. We don't _need_
                    # to validate IObject values because a client
                    # isn't changing anything about the IObject; it's
                    # just associating one IObject or another with an
                    # entry. We're already checking the type of the
                    # new IObject, and that's the only error the
                    # client can cause.
                    try:
                        # Do any field-specific validation.
                        field.validate(value)
                    except ConstraintNotSatisfied, e:
                        # Try to get a string error message out of
                        # the exception; otherwise use a generic message
                        # instead of whatever object the raise site
                        # thought would be a good idea.
                        if (len(e.args) > 0 and
                            isinstance(e.args[0], basestring)):
                            error = e.args[0]
                        else:
                            error = "Constraint not satisfied."
                        errors.append("%s: %s" % (repr_name, error))
                        continue
                    except RequiredMissing, e:
                        error = "Missing required value."
                        errors.append("%s: %s" % (repr_name, error))
                    except (ValueError, ValidationError), e:
                        error = str(e)
                        if error == "":
                            error = "Validation error"
                        errors.append("%s: %s" % (repr_name, error))
                        continue
                validated_changeset.append((field, value))
        # If there are any fields left in the changeset, they're
        # fields that don't correspond to some field in the
        # schema. They're all errors.
        for invalid_field in changeset.keys():
            errors.append("%s: You tried to modify a nonexistent "
                          "attribute." % invalid_field)

        # If there were errors, display them and send a status of 400.
        if len(errors) > 0:
            self.request.response.setStatus(400)
            self.request.response.setHeader('Content-type', 'text/plain')
            return "\n".join(errors)

        # Make a snapshot of the entry to use in a notification event.
        entry_before_modification = Snapshot(
            self.entry.context, providing=providedBy(self.entry.context))

        # Store the entry's current URL so we can see if it changes.
        original_url = absoluteURL(self.entry.context, self.request)

        # Make the changes, in the same order obtained from
        # get_entry_fields_in_write_order.
        for field, value in validated_changeset:
            field.set(self.entry, value)
        # The representation has changed, and etags will need to be
        # recalculated.
        self.etags_by_media_type = {}

        # Send a notification event.
        event = ObjectModifiedEvent(
            object=self.entry.context,
            object_before_modification=entry_before_modification,
            edited_fields=[field for field, value in validated_changeset])
        notify(event)

        # The changeset contained new values for some of this object's
        # fields, and the notification event may have changed others.
        # Clear out any fields that changed.
        for name, ignored in self._unmarshalled_field_cache.items():
            force_clear = False
            try:
                old_value = getattr(entry_before_modification, name, None)
                new_value = getattr(self.entry.context, name, None)
            except Unauthorized:
                # Clear the cache, just to be safe.
                force_clear = True
            if force_clear or new_value != old_value:
                del(self._unmarshalled_field_cache[name])

        new_url = absoluteURL(self.entry.context, self.request)
        if new_url == original_url:
            # The resource did not move. Serve a new representation of
            # it. This might not necessarily be a representation of
            # the whole entry!
            self.request.response.setStatus(209)
            media_type = self.getPreferredSupportedContentType()
            self.request.response.setHeader('Content-type', media_type)
            return self._representation(media_type)
        else:
            # The object moved. Serve a redirect to its new location.
            # This might not necessarily be the location of the entry!
            self.request.response.setStatus(301)
            self.request.response.setHeader(
                'Location', absoluteURL(self.context, self.request))
            # RFC 2616 says the body of a 301 response, if present,
            # SHOULD be a note linking to the new object.
            return ''


class EntryFieldResource(FieldUnmarshallerMixin, EntryManipulatingResource):
    """An individual field of an entry."""
    implements(IEntryFieldResource, IJSONPublishable)

    SUPPORTED_CONTENT_TYPES = [HTTPResource.JSON_TYPE,
                               HTTPResource.XHTML_TYPE]

    def __init__(self, context, request):
        """Initialize with respect to a context and request."""
        super(EntryFieldResource, self).__init__(context, request)
        self.entry = self.context.entry

    def do_GET(self):
        """Create a representation of a single field."""
        media_type = self.handleConditionalGET()
        if media_type is None:
            # The conditional GET succeeded. Serve nothing.
            return ""
        else:
            self.request.response.setHeader('Content-Type', media_type)
            return self._representation(media_type)

    def do_PUT(self, media_type, representation):
        """Overwrite the field's existing value with a new value."""
        value, error = self.processAsJSONDocument(media_type, representation)
        if value is None:
            return value, error
        changeset = {self.context.name : value}
        return self.applyChanges(changeset)

    do_PATCH = do_PUT

    def _getETagCores(self, unmarshalled_field_values=None):
        """Calculate the ETag for an entry field.

        The core of the ETag is the field value itself.
        """
        name, value = self._unmarshallField(
            self.context.name, self.context.field)
        return [str(value)]

    def _representation(self, media_type):
        """Create a representation of the field value."""
        if media_type == self.JSON_TYPE:
            name, value = self._unmarshallField(
                self.context.name, self.context.field, CLOSEUP_DETAIL)
            return simplejson.dumps(value)
        elif media_type == self.XHTML_TYPE:
            name, value = self.unmarshallFieldToHTML(
                self.context.name, self.context.field)
            return value
        else:
            raise AssertionError(
                    "No representation implementation for media type %s"
                    % media_type)


class EntryField:
    """A schema field bound by name to a particular entry."""
    implements(IEntryField, ILocation)

    def __init__(self, entry, field, name):
        """Initialize with respect to a named field of an entry."""
        self.entry = entry
        self.field = field.bind(entry)
        self.name = name

        # ILocation implementation
        self.__parent__ = self.entry.context
        self.__name__ = self.name


class EntryFieldURL(AbsoluteURL):
    """An IAbsoluteURL adapter for EntryField objects."""
    component.adapts(EntryField, IHTTPRequest)
    implements(IAbsoluteURL)

    def __init__(self, entryfield, request):
        self.context = entryfield
        self.request = request


class EntryResource(CustomOperationResourceMixin,
                    FieldUnmarshallerMixin, EntryManipulatingResource):
    """An individual object, published to the web."""
    implements(IEntryResource, IJSONPublishable)

    SUPPORTED_CONTENT_TYPES = [HTTPResource.WADL_TYPE,
                               HTTPResource.DEPRECATED_WADL_TYPE,
                               HTTPResource.XHTML_TYPE,
                               HTTPResource.JSON_TYPE]

    def __init__(self, context, request):
        """Associate this resource with a specific object and request."""
        super(EntryResource, self).__init__(context, request)
        self.entry = getMultiAdapter((context, request), IEntry)

    def _getETagCores(self, unmarshalled_field_values=None):
        """Calculate the ETag for an entry.

        :arg unmarshalled_field_values: A dict mapping field names to
        unmarshalled values, obtained during some other operation such
        as the construction of a representation.
        """
        unwritable_values = []
        writable_values = []
        for name, field in getFieldsInOrder(self.entry.schema):
            if self.isModifiableField(field, True):
                # The client can write to this value.
                bucket = writable_values
            elif self.isModifiableField(field, False):
                # The client can't write this value, but it still
                # might change.
                bucket = unwritable_values
            else:
                # This value can never change, and as such does not
                # need to be included in the ETag.
                continue
            if (unmarshalled_field_values is not None
                and unmarshalled_field_values.get(name)):
                value = unmarshalled_field_values[name]
            else:
                ignored, value = self._unmarshallField(name, field)
            bucket.append(decode_value(value))

        unwritable = "\0".join(unwritable_values).encode("utf-8")
        writable = "\0".join(writable_values).encode("utf-8")
        return [unwritable, writable]


    def _etagMatchesForWrite(self, existing_etag, incoming_etags):
        """Make sure no other client has modified this resource.

        For a conditional read to succeed, the entire ETag must
        match. But for a conditional write to succeed, only the second
        half of the ETag must match. This prevents spurious 412 errors
        on conditional writes where the only fields that changed are
        read-only fields that can't possibly cause a conflict.
        """
        existing_write_portion = existing_etag.split('-', 1)[-1]
        for etag in incoming_etags:
            if '-' in etag:
                incoming_write_portion = etag.rsplit('-', 1)[-1]
            else:
                incoming_write_portion = etag
            if existing_write_portion == incoming_write_portion:
                return True
        return False


    def toDataForJSON(self):
        """Turn the object into a simple data structure."""
        return self.toDataStructure(self.JSON_TYPE)

    def toDataStructure(self, media_type):
        """Turn the object into a simple data structure.

        In this case, a dictionary containing all fields defined by
        the resource interface.

        The values in the dictionary may differ depending on the value
        of media_type.
        """
        data = {}
        data['self_link'] = absoluteURL(self.context, self.request)
        data['resource_type_link'] = self.type_url
        unmarshalled_field_values = {}
        for name, field in getFieldsInOrder(self.entry.schema):
            if media_type == self.JSON_TYPE:
                repr_name, repr_value = self._unmarshallField(name, field)
            elif media_type == self.XHTML_TYPE:
                repr_name, repr_value = self.unmarshallFieldToHTML(
                    name, field)
            else:
                raise AssertionError(
                        "Cannot create data structure for media type %s"
                        % media_type)
            data[repr_name] = repr_value
            unmarshalled_field_values[name] =  repr_value

        etag = self.getETag(media_type, unmarshalled_field_values)
        data['http_etag'] = etag
        return data

    def toXHTML(self):
        """Represent this resource as an XHTML document."""
        view = getMultiAdapter(
            (self.context, self.request),
            name="lazr.restful.EntryResource")
        return view()

    def processAsJSONHash(self, media_type, representation):
        """Process an incoming representation as a JSON hash.

        :param media_type: The specified media type of the incoming
        representation.

        :representation: The incoming representation:

        :return: A tuple (dictionary, error). 'dictionary' is a Python
        dictionary corresponding to the incoming JSON hash. 'error' is
        an error message if the incoming representation could not be
        processed. If there is an error, this method will set an
        appropriate HTTP response code.
        """

        value, error = self.processAsJSONDocument(media_type, representation)
        if value is None:
            return value, error
        if not isinstance(value, dict):
            self.request.response.setStatus(400)
            return None, 'Expected a JSON hash.'
        return value, None

    def do_GET(self):
        """Render an appropriate representation of the entry."""
        # Handle a custom operation, probably a search.
        operation_name = self.request.form.pop('ws.op', None)
        if operation_name is not None:
            result = self.handleCustomGET(operation_name)
            if isinstance(result, basestring):
                # The custom operation took care of everything and
                # just needs this string served to the client.
                return result
        else:
            # No custom operation was specified. Implement a standard
            # GET, which serves a JSON or WADL representation of the
            # entry.
            media_type = self.handleConditionalGET()
            if media_type is None:
                # The conditional GET succeeded. Serve nothing.
                return ""
            else:
                self.request.response.setHeader('Content-Type', media_type)
                return self._representation(media_type)

    def do_PUT(self, media_type, representation):
        """Modify the entry's state to match the given representation.

        A PUT is just like a PATCH, except the given representation
        must be a complete representation of the entry.
        """
        changeset, error = self.processAsJSONHash(media_type, representation)
        if error is not None:
            return error

        # Make sure the representation includes values for all
        # writable attributes.
        #
        # Get the fields ordered by schema order so that we always
        # evaluate them in the same order. This is needed to predict
        # errors when testing.
        for name, field in getFieldsInOrder(self.entry.schema):
            if not self.isModifiableField(field, True):
                continue
            field = field.bind(self.context)
            marshaller = getMultiAdapter((field, self.request),
                                         IFieldMarshaller)
            repr_name = marshaller.representation_name
            if (changeset.get(repr_name) is None
                and getattr(self.entry, name) is not None):
                # This entry has a value for the attribute, but the
                # entity-body of the PUT request didn't make any assertion
                # about the attribute. The resource's behavior under HTTP
                # is undefined; we choose to send an error.
                self.request.response.setStatus(400)
                return ("You didn't specify a value for the attribute '%s'."
                        % repr_name)

        return self.applyChanges(changeset)


    def do_PATCH(self, media_type, representation):
        """Apply a JSON patch to the entry."""
        changeset, error = self.processAsJSONHash(media_type, representation)
        if error is not None:
            return error
        return self.applyChanges(changeset)

    @property
    def type_url(self):
        "The URL to the resource type for this resource."
        adapter = EntryAdapterUtility(self.entry.__class__)

        return "%s#%s" % (
            absoluteURL(self.request.publication.getApplication(
                    self.request), self.request),
            adapter.singular_type)

    def isModifiableField(self, field, is_external_client):
        """Returns true if this field's value can be changed.

        Collection fields, and fields that are not part of the web
        service interface, are never modifiable. Read-only fields are
        not modifiable by external clients.

        :param is_external_client: Whether the code trying to modify
        the field is an external client. Read-only fields cannot be
        directly modified from external clients, but they might change
        as side effects of other changes.
        """
        if (ICollectionField.providedBy(field)
            or field.__name__.startswith('_')):
            return False
        if field.readonly:
            return not is_external_client
        return True

    def _representation(self, media_type):
        """Return a representation of this entry, of the given media type."""
        if media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            return self.toWADL().encode("utf-8")
        elif media_type == self.JSON_TYPE:
            return simplejson.dumps(self, cls=ResourceJSONEncoder)
        elif media_type == self.XHTML_TYPE:
            return self.toXHTML().encode("utf-8")
        else:
            raise AssertionError(
                    "No representation implementation for media type %s"
                    % media_type)


class CollectionResource(BatchingResourceMixin,
                         CustomOperationResourceMixin,
                         ReadOnlyResource):
    """A resource that serves a list of entry resources."""
    implements(ICollectionResource)

    def __init__(self, context, request):
        """Associate this resource with a specific object and request."""
        super(CollectionResource, self).__init__(context, request)
        if ICollection.providedBy(context):
            self.collection = context
        else:
            self.collection = getMultiAdapter((context, request), ICollection)

    def do_GET(self):
        """Fetch a collection and render it as JSON."""
        # Handle a custom operation, probably a search.
        operation_name = self.request.form.pop('ws.op', None)
        if operation_name is not None:
            result = self.handleCustomGET(operation_name)
            if isinstance(result, str) or isinstance(result, unicode):
                # The custom operation took care of everything and
                # just needs this string served to the client.
                return result
        else:
            # No custom operation was specified. Implement a standard
            # GET, which serves a JSON or WADL representation of the
            # collection.
            entries = self.collection.find()
            if entries is None:
                raise NotFound(self, self.collection_name)

            media_type = self.getPreferredSupportedContentType()
            if media_type in [self.DEPRECATED_WADL_TYPE, self.WADL_TYPE]:
                result = self.toWADL().encode("utf-8")
                self.request.response.setHeader('Content-Type', media_type)
                return result

            result = self.batch(entries)

        self.request.response.setHeader('Content-type', self.JSON_TYPE)
        return simplejson.dumps(result, cls=ResourceJSONEncoder)

    def batch(self, entries=None):
        """Return a JSON representation of a batch of entries.

        :param entries: (Optional) A precomputed list of entries to batch.
        """
        if entries is None:
            entries = self.collection.find()
        result = super(CollectionResource, self).batch(entries, self.request)
        result['resource_type_link'] = self.type_url
        return result

    @property
    def type_url(self):
        "The URL to the resource type for the object."

        if IScopedCollection.providedBy(self.collection):
            # Scoped collection. The type URL depends on what type of
            # entry the collection holds.
            schema = self.context.relationship.value_type.schema
            adapter = EntryAdapterUtility.forSchemaInterface(
                schema, self.request)
            return adapter.entry_page_type_link
        else:
            # Top-level collection.
            schema = self.collection.entry_schema
            adapter = EntryAdapterUtility.forEntryInterface(
                schema, self.request)
            return adapter.collection_type_link


class ServiceRootResource(HTTPResource):
    """A resource that responds to GET by describing the service."""
    implements(IServiceRootResource, IJSONPublishable)

    # A preparsed template file for WADL representations of the root.
    WADL_TEMPLATE = LazrPageTemplateFile('templates/wadl-root.pt')

    def __init__(self):
        """Initialize the resource.

        The service root constructor is different from other
        HTTPResource constructors because Zope initializes the object
        with no request or context, and then passes the request in
        when it calls the service root object.
        """
        # We're not calling the superclass constructor because
        # it assumes it's being called in the context of a particular
        # request.
        # pylint:disable-msg=W0231
        self.etags_by_media_type = {}

    @property
    def request(self):
        """Fetch the current web service request."""
        return get_current_web_service_request()

    def _getETagCores(self, cache=None):
        """Calculate an ETag for a representation of this resource.

        The service root resource changes only when the software
        itself changes. This information goes into the ETag already,
        so there's no need to provide anything.
        """
        return ['']

    def __call__(self, REQUEST=None):
        """Handle a GET request."""
        method = self.getRequestMethod(REQUEST)
        if method is None:
            result = self.HTTP_METHOD_OVERRIDE_ERROR
        elif method == "GET":
            result = self.do_GET()
        else:
            REQUEST.response.setStatus(405)
            REQUEST.response.setHeader("Allow", "GET")
            result = ""
        return result

    def setCachingHeaders(self):
        "How long should the client cache this service root?"
        user_agent = self.request.getHeader('User-Agent', '')
        if user_agent.startswith('Python-httplib2'):
            # XXX leonardr 20100412
            # bug=http://code.google.com/p/httplib2/issues/detail?id=97
            #
            # A client with a User-Agent of "Python/httplib2" (such as
            # old versions of lazr.restfulclient) gives inconsistent
            # results when a resource is served with both ETag and
            # Cache-Control. We check for that User-Agent and omit the
            # Cache-Control headers if it makes a request.
            return
        config = getUtility(IWebServiceConfiguration)
        caching_policy = config.caching_policy
        if self.request.version == config.active_versions[-1]:
            max_age = caching_policy[-1]
        else:
            max_age = caching_policy[0]
        if max_age > 0:
            self.request.response.setHeader(
                'Cache-Control', 'max-age=%d' % max_age)
            # Also set the Date header so that client-side caches will
            # have something to work from.
            self.request.response.setHeader('Date', formatdate(time.time()))

    def do_GET(self):
        """Describe the capabilities of the web service."""
        media_type = self.handleConditionalGET()
        self.setCachingHeaders()
        if media_type is None:
            # The conditional GET succeeded. Serve nothing.
            return ""
        elif media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            result = self.toWADL().encode("utf-8")
        elif media_type == self.JSON_TYPE:
            # Serve a JSON map containing links to all the top-level
            # resources.
            result = simplejson.dumps(self, cls=ResourceJSONEncoder)

        self.request.response.setHeader('Content-Type', media_type)
        return result

    def toWADL(self):
        # Find all resource types.
        site_manager = getGlobalSiteManager()
        entry_classes = []
        collection_classes = []
        singular_names = {}
        plural_names = {}

        # Determine the name of the earliest version. We'll be using this later.
        config = getUtility(IWebServiceConfiguration)
        earliest_version = config.active_versions[0]

        for registration in sorted(site_manager.registeredAdapters()):
            provided = registration.provided
            if IInterface.providedBy(provided):
                if (provided.isOrExtends(IEntry)
                    and IEntry.implementedBy(registration.factory)):
                    # The implementedBy check is necessary because
                    # some IEntry adapters aren't classes with
                    # schemas; they're functions. We can ignore these
                    # functions because their return value will be one
                    # of the classes with schemas, which we do describe.

                    # Make sure we have a registration relevant to
                    # this version. A given entry may have one
                    # registration for every web service version.
                    schema, version_marker = registration.required

                    if (version_marker is IWebServiceClientRequest
                        and self.request.version != earliest_version):
                        # We are generating WADL for some version
                        # other than the earliest version, and this is
                        # a registration for the earliest version. We
                        # can ignore it.
                        #
                        # We need this special test because the normal
                        # test (below) is useless when
                        # version_marker is
                        # IWebServiceClientRequest. Since all request
                        # objects provide IWebServiceClientRequest
                        # directly, it will always show up in
                        # providedBy(self.request).
                        continue
                    if not version_marker in providedBy(self.request):
                        continue

                    # Make sure that no other entry class is using this
                    # class's singular or plural names.
                    adapter = EntryAdapterUtility.forSchemaInterface(
                        schema, self.request)

                    singular = adapter.singular_type
                    assert not singular_names.has_key(singular), (
                        "Both %s and %s expose the singular name '%s'."
                        % (singular_names[singular].__name__,
                           schema.__name__, singular))
                    singular_names[singular] = schema

                    plural = adapter.plural_type
                    assert not plural_names.has_key(plural), (
                        "Both %s and %s expose the plural name '%s'."
                        % (plural_names[plural].__name__,
                           schema.__name__, plural))
                    plural_names[plural] = schema

                    entry_classes.append(registration.factory)
                elif (provided.isOrExtends(ICollection)
                      and ICollection.implementedBy(registration.factory)
                      and not IScopedCollection.implementedBy(
                        registration.factory)):
                    # See comment above re: implementedBy check.
                    # We omit IScopedCollection because those are handled
                    # by the entry classes.
                    collection_classes.append(registration.factory)
        namespace = self.WADL_TEMPLATE.pt_getContext()
        namespace['context'] = self
        namespace['request'] = self.request
        namespace['entries'] = entry_classes
        namespace['collections'] = collection_classes
        return self.WADL_TEMPLATE.pt_render(namespace)

    def toDataForJSON(self):
        """Return a map of links to top-level collection resources.

        A top-level resource is one that adapts a utility.  Currently
        top-level entry resources (should there be any) are not
        represented.
        """
        type_url = "%s#%s" % (
            absoluteURL(
                self.request.publication.getApplication(self.request),
                self.request),
            "service-root")
        data_for_json = {'resource_type_link' : type_url}
        publications = self.getTopLevelPublications()
        for link_name, publication in publications.items():
            data_for_json[link_name] = absoluteURL(publication,
                                                   self.request)
        return data_for_json

    def getTopLevelPublications(self):
        """Return a mapping of top-level link names to published objects."""
        top_level_resources = {}
        site_manager = getGlobalSiteManager()
        # First, collect the top-level collections.
        for registration in site_manager.registeredAdapters():
            provided = registration.provided
            if IInterface.providedBy(provided):
                # XXX sinzui 2008-09-29 bug=276079:
                # Top-level collections need a marker interface
                # so that so top-level utilities are explicit.
                if (provided.isOrExtends(ICollection)
                     and ICollection.implementedBy(registration.factory)):
                    try:
                        utility = getUtility(registration.required[0])
                    except ComponentLookupError:
                        # It's not a top-level resource.
                        continue
                    entry_schema = registration.factory.entry_schema
                    if isinstance(entry_schema, property):
                        # It's not a top-level resource.
                        continue
                    adapter = EntryAdapterUtility.forEntryInterface(
                        entry_schema, self.request)
                    link_name = ("%s_collection_link" % adapter.plural_type)
                    top_level_resources[link_name] = utility
        # Now, collect the top-level entries.
        for utility in getAllUtilitiesRegisteredFor(ITopLevelEntryLink):
            link_name = ("%s_link" % utility.link_name)
            top_level_resources[link_name] = utility

        return top_level_resources

    @property
    def type_url(self):
        "The URL to the resource type for this resource."
        adapter = EntryAdapterUtility(self.entry.__class__)

        return "%s#%s" % (
            absoluteURL(self.request.publication.getApplication(
                    self.request), self.request),
            adapter.singular_type)


class Entry:
    """An individual entry."""
    implements(IEntry)

    def __init__(self, context, request):
        """Associate the entry with some database model object."""
        self.context = context
        self.request = request


class Collection:
    """A collection of entries."""
    implements(ICollection)

    def __init__(self, context, request):
        """Associate the entry with some database model object."""
        self.context = context
        self.request = request


class ScopedCollection:
    """A collection associated with some parent object."""
    implements(IScopedCollection)
    adapts(Interface, Interface, IWebServiceLayer)

    def __init__(self, context, collection, request):
        """Initialize the scoped collection.

        :param context: The object to which the collection is scoped.
        :param collection: The scoped collection.
        """
        self.context = context
        self.collection = collection
        self.request = request
        # Unknown at this time. Should be set by our call-site.
        self.relationship = None

    @property
    def entry_schema(self):
        """The schema for the entries in this collection."""
        # We are given a model schema (IFoo). Look up the
        # corresponding entry schema (IFooEntry).
        model_schema = self.relationship.value_type.schema
        request_interface = getUtility(
            IWebServiceVersion,
            name=self.request.version)
        return getGlobalSiteManager().adapters.lookup(
            (model_schema, request_interface), IEntry).schema

    def find(self):
        """See `ICollection`."""
        return self.collection


class RESTUtilityBase:

    def _service_root_url(self):
        """Return the URL to the service root."""
        request = get_current_web_service_request()
        return absoluteURL(request.publication.getApplication(request),
                           request)


class EntryAdapterUtility(RESTUtilityBase):
    """Useful information about an entry's presence in the web service.

    This includes the links to entry's WADL resource type, and the
    resource type for a page of these entries.
    """

    @classmethod
    def forSchemaInterface(cls, entry_interface, request):
        """Create an entry adapter utility, given a schema interface.

        A schema interface is one that can be annotated to produce a
        subclass of IEntry.
        """
        request_interface = getUtility(
            IWebServiceVersion, name=request.version)
        entry_class = getGlobalSiteManager().adapters.lookup(
            (entry_interface, request_interface), IEntry)
        assert entry_class is not None, (
            ("No IEntry adapter found for %s (web service version: %s)."
             % (entry_interface.__name__, request.version)))
        return EntryAdapterUtility(entry_class)

    @classmethod
    def forEntryInterface(cls, entry_interface, request):
        """Create an entry adapter utility, given a subclass of IEntry."""
        registrations = getGlobalSiteManager().registeredAdapters()
        # There should be one IEntry subclass registered for every
        # version of the web service. We'll go through the appropriate
        # IEntry registrations looking for one associated with the
        # same IWebServiceVersion interface we find on the 'request'
        # object.
        entry_classes = [
            registration.factory for registration in registrations
            if (IInterface.providedBy(registration.provided)
                and registration.provided.isOrExtends(IEntry)
                and entry_interface.implementedBy(registration.factory)
                and registration.required[1].providedBy(request))]
        assert not len(entry_classes) > 1, (
            "%s provides more than one IEntry subclass for version %s." %
            (entry_interface.__name__, request.version))
        assert not len(entry_classes) < 1, (
            "%s does not provide any IEntry subclass for version %s." %
            (entry_interface.__name__, request.version))
        return EntryAdapterUtility(entry_classes[0])

    def __init__(self, entry_class):
        """Initialize with a class that implements IEntry."""
        self.entry_class = entry_class

    @property
    def entry_interface(self):
        """The IEntry subclass implemented by this entry type."""
        interfaces = implementedBy(self.entry_class)
        entry_ifaces = [interface for interface in interfaces
                        if interface.extends(IEntry)]
        assert len(entry_ifaces) == 1, (
            "There must be one and only one IEntry implementation "
            "for %s, found %s" % (
                self.entry_class,
                ", ".join(interface.__name__ for interface in entry_ifaces)))
        return entry_ifaces[0]

    @property
    def singular_type(self):
        """Return the singular name for this object type."""
        interface = self.entry_interface
        return interface.queryTaggedValue(LAZR_WEBSERVICE_NAME)['singular']

    @property
    def plural_type(self):
        """Return the plural name for this object type."""
        interface = self.entry_interface
        return interface.queryTaggedValue(LAZR_WEBSERVICE_NAME)['plural']

    @property
    def type_link(self):
        """The URL to the type definition for this kind of entry."""
        return "%s#%s" % (
            self._service_root_url(), self.singular_type)

    @property
    def collection_type_link(self):
        """The definition of a top-level collection of this kind of object."""
        return "%s#%s" % (
            self._service_root_url(), self.plural_type)

    @property
    def entry_page_type(self):
        """The definition of a collection of this kind of object."""
        return "%s-page-resource" % self.singular_type

    @property
    def entry_page_type_link(self):
        "The URL to the definition of a collection of this kind of object."
        return "%s#%s" % (
            self._service_root_url(), self.entry_page_type)

    @property
    def entry_page_representation_id(self):
        "The name of the description of a colleciton of this kind of object."
        return "%s-page" % self.singular_type

    @property
    def entry_page_representation_link(self):
        "The URL to the description of a collection of this kind of object."
        return "%s#%s" % (
            self._service_root_url(),
            self.entry_page_representation_id)

    @property
    def full_representation_link(self):
        """The URL to the description of the object's full representation."""
        return "%s#%s-full" % (
            self._service_root_url(), self.singular_type)


def get_entry_fields_in_write_order(entry):
    """Return the entry's fields in the order they should be written to.

    The ordering is intended to 1) be deterministic for a given schema
    and 2) minimize the chance of conflicts. Fields that are just
    fields come before fields (believed to be) controlled by
    mutators. Within each group, fields are returned in the order they
    appear in the schema.

    :param entry: An object that provides IEntry.
    :return: A list of 2-tuples (field name, field object)
    """
    non_mutator_fields = []
    mutator_fields = []
    field_implementations = entry.__class__.__dict__
    for name, field in getFieldsInOrder(entry.schema):
        if name.startswith('_'):
            # This field is not part of the web service interface.
            continue

        # If this field is secretly a subclass of lazr.delegates
        # Passthrough (but not a direct instance of Passthrough), put
        # it at the end -- it's probably controlled by a mutator.
        implementation = field_implementations[name]
        if (issubclass(implementation.__class__, Passthrough)
            and not implementation.__class__ is Passthrough):
            mutator_fields.append((name, field))
        else:
            non_mutator_fields.append((name, field))
    return non_mutator_fields + mutator_fields

