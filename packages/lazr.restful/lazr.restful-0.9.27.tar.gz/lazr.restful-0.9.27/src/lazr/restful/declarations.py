# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Declaration helpers to define a web service."""

__metaclass__ = type
__all__ = [
    'COLLECTION_TYPE',
    'ENTRY_TYPE',
    'FIELD_TYPE',
    'LAZR_WEBSERVICE_EXPORTED',
    'LAZR_WEBSERVICE_MUTATORS',
    'OPERATION_TYPES',
    'REQUEST_USER',
    'cache_for',
    'call_with',
    'collection_default_content',
    'error_status',
    'exported',
    'export_as_webservice_collection',
    'export_as_webservice_entry',
    'export_destructor_operation',
    'export_factory_operation',
    'export_operation_as',
    'export_read_operation',
    'export_write_operation',
    'generate_collection_adapter',
    'generate_entry_adapters',
    'generate_entry_interfaces',
    'generate_operation_adapter',
    'mutator_for',
    'operation_for_version',
    'operation_parameters',
    'operation_returns_entry',
    'operation_returns_collection_of',
    'rename_parameters_as',
    'webservice_error',
    ]

import copy
import sys

from zope.component import getUtility, getGlobalSiteManager
from zope.interface import classImplements
from zope.interface.advice import addClassAdvisor
from zope.interface.interface import fromFunction, InterfaceClass, TAGGED_DATA
from zope.interface.interfaces import IInterface, IMethod
from zope.schema import getFields
from zope.schema.interfaces import IField, IText
from zope.security.checker import CheckerPublic
from zope.traversing.browser import absoluteURL

from lazr.delegates import Passthrough
from lazr.restful.fields import CollectionField, Reference
from lazr.restful.interface import copy_field
from lazr.restful.interfaces import (
    ICollection, IEntry, IResourceDELETEOperation, IResourceGETOperation,
    IResourcePOSTOperation, IWebServiceConfiguration, IWebServiceVersion,
    LAZR_WEBSERVICE_NAME, LAZR_WEBSERVICE_NS)
from lazr.restful import (
    Collection, Entry, EntryAdapterUtility, ResourceOperation, ObjectLink)
from lazr.restful.security import protect_schema
from lazr.restful.utils import (
    camelcase_to_underscore_separated, get_current_web_service_request,
    make_identifier_safe, VersionedDict)

LAZR_WEBSERVICE_EXPORTED = '%s.exported' % LAZR_WEBSERVICE_NS
LAZR_WEBSERVICE_MUTATORS = '%s.exported.mutators' % LAZR_WEBSERVICE_NS
COLLECTION_TYPE = 'collection'
ENTRY_TYPE = 'entry'
FIELD_TYPE = 'field'
REMOVED_OPERATION_TYPE = 'removed_operation'
OPERATION_TYPES = (
    'destructor', 'factory', 'read_operation', 'write_operation',
    REMOVED_OPERATION_TYPE)


class REQUEST_USER:
    """Marker class standing in for the user of the current request.

    This is passed in to annotations like @call_with. This is a class
    rather than an object because it's going to be run through
    copy.deepcopy, and we want 'is REQUEST_USER' to succeed on the
    copy.
    """
    pass


def _check_called_from_interface_def(name):
    """Make sure that the declaration was used from within a class definition.
    """
    # 2 is our caller's caller.
    frame = sys._getframe(2)
    f_locals = frame.f_locals

    # Try to make sure we were called from a class def.
    if (f_locals is frame.f_globals) or ('__module__' not in f_locals):
        raise TypeError(
            "%s can only be used from within an interface definition." % name)


def _check_interface(name, interface):
    """Check that interface provides IInterface or raise a TypeError."""
    if not IInterface.providedBy(interface):
        raise TypeError("%s can only be used on an interface." % name)


def _get_interface_tags():
    """Retrieve the dictionary containing tagged values for the interface.

    This will create it, if it hasn't been defined yet.
    """
    # Our caller is contained within the interface definition.
    f_locals = sys._getframe(2).f_locals
    return f_locals.setdefault(TAGGED_DATA, {})


def export_as_webservice_entry(singular_name=None, plural_name=None):
    """Mark the content interface as exported on the web service as an entry.
    """
    _check_called_from_interface_def('export_as_webservice_entry()')
    def mark_entry(interface):
        """Class advisor that tags the interface once it is created."""
        _check_interface('export_as_webservice_entry()', interface)
        if singular_name is None:
            # By convention, interfaces are called IWord1[Word2...]. The
            # default behavior assumes this convention and yields a
            # singular name of "word1_word2".
            my_singular_name = camelcase_to_underscore_separated(
                interface.__name__[1:])
        else:
            my_singular_name = singular_name
        if plural_name is None:
            # Apply default pluralization rule.
            my_plural_name = my_singular_name + 's'
        else:
            my_plural_name = plural_name

        interface.setTaggedValue(
            LAZR_WEBSERVICE_EXPORTED, dict(
                type=ENTRY_TYPE, singular_name=my_singular_name,
                plural_name=my_plural_name))

        # Set the name of the fields that didn't specify it using the
        # 'export_as' parameter in exported(). This must be done here,
        # because the field's __name__ attribute is only set when the
        # interface is created.
        for name, field in getFields(interface).items():
            tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
            if tag_stack is None or tag_stack.is_empty:
                continue
            if tag_stack['type'] != FIELD_TYPE:
                continue
            for version, tags in tag_stack.stack:
                # Set 'as' for every version in which the field is
                # published but no 'as' is specified. Also set
                # 'original_name' for every version in which the field
                # is published--this will help with performance
                # optimizations around permission checks.
                if tags.get('exported') != False:
                    tags['original_name'] = name
                    if tags.get('as') is None:
                        tags['as'] = name



        annotate_exported_methods(interface)
        return interface
    addClassAdvisor(mark_entry)


def exported(field, *versioned_annotations, **kwparams):
    """Mark the field as part of the entry data model.

    :param versioned_annotations: A list of (version, param) 2-tuples,
        with more recent web service versions earlier in the list and older
        versions later in the list. The 'param' objects can either be a
        string name for the field in the given version (None means to
        use the field's internal name), or a dictionary.

        The dictionary may contain the key 'exported', which controls
        whether or not to publish this field at all in the given
        version, and the key 'exported_as', which controls the name to
        use when publishing the field. as=None means to use the
        field's internal name.

    :param exported_as: the name under which the field is published in
        the entry in the earliest version of the web service. By
        default, the field's internal name is used. This is a simpler
        alternative to the 'versioned_annotations' parameter, for fields
        whose names don't change in different versions.

    :param exported: Whether or not the field should be published in
        the earliest version of the web service.

    :raises TypeError: if called on an object which doesn't provide IField.
    :returns: The field with an added tagged value.
    """
    if not IField.providedBy(field):
        raise TypeError("exported() can only be used on IFields.")

    # The first step is to turn the arguments into a
    # VersionedDict. We'll start by collecting annotations for the
    # earliest version, which we refer to as None because we don't
    # know any of the real version strings yet.
    annotation_stack = VersionedDict()
    annotation_stack.push(None)
    annotation_stack['type'] = FIELD_TYPE

    annotation_key_for_argument_key = {'exported_as' : 'as',
                                       'exported' : 'exported'}

    # The only valid keyword parameters are 'exported' and
    # 'exported_as', which manage the behavior in the first
    # version. If these keywords are present, incorporate them into
    # the VersionedDict.
    for key in ('exported_as', 'exported'):
        annotation_key = annotation_key_for_argument_key[key]
        if key in kwparams:
            annotation_stack[annotation_key] = kwparams.pop(key)
    # If any keywords are left over, raise an exception.
    if len(kwparams) > 0:
        raise TypeError("exported got an unexpected keyword "
                        "argument '%s'" % kwparams.keys()[0])

    # Now incorporate the list of named dicts into the VersionedDict.
    for version, annotations in reversed(versioned_annotations):
        # Push it onto the stack.
        annotation_stack.push(version)
        # Make sure that the 'annotations' dict contains only
        # recognized annotations.
        for key in annotations:
            if key not in annotation_key_for_argument_key:
                raise ValueError('Unrecognized annotation for version "%s": '
                                 '"%s"' % (version, key))
            annotation_stack[annotation_key_for_argument_key[key]] = (
                annotations[key])

    # Now we can annotate the field object with the VersionedDict.
    field.setTaggedValue(LAZR_WEBSERVICE_EXPORTED, annotation_stack)

    # We track the field's mutator information separately because it's
    # defined in the named operations, not in the fields. The last
    # thing we want to do is try to insert a foreign value into an
    # already create annotation stack.
    field.setTaggedValue(LAZR_WEBSERVICE_MUTATORS, {})

    return field


def export_as_webservice_collection(entry_schema):
    """Mark the interface as exported on the web service as a collection.

    :raises TypeError: if the interface doesn't have a method decorated with
        @collection_default_content.
    """
    _check_called_from_interface_def('export_as_webservice_collection()')

    if not IInterface.providedBy(entry_schema):
        raise TypeError("entry_schema must be an interface.")

    # Set the tags at this point, so that future declarations can
    # check it.
    tags = _get_interface_tags()
    tags[LAZR_WEBSERVICE_EXPORTED] = dict(
        type=COLLECTION_TYPE, collection_entry_schema=entry_schema)

    def mark_collection(interface):
        """Class advisor that tags the interface once it is created."""
        _check_interface('export_as_webservice_collection()', interface)

        tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if 'collection_default_content' not in tag:
            raise TypeError(
                "export_as_webservice_collection() is missing a method "
                "tagged with @collection_default_content.")

        annotate_exported_methods(interface)
        return interface

    addClassAdvisor(mark_collection)


class collection_default_content:
    """Decorates the method that provides the default values of a collection.

    :raises TypeError: if not called from within an interface exported as a
        collection, or if used more than once in the same interface.
    """

    def __init__(self, version=None, **params):
        """Create the decorator marking the default collection method.

        :param version: The first web service version that should use this
            method as the collection's default content.
        :param params: Optional parameter values to use when calling the
            method. This is to be used when the method has required
            parameters.
        """
        _check_called_from_interface_def('@collection_default_content')

        tags = _get_interface_tags()
        tag = tags.get(LAZR_WEBSERVICE_EXPORTED)
        if tag is None or tag['type'] != COLLECTION_TYPE:
            raise TypeError(
                "@collection_default_content can only be used from within an "
                "interface exported as a collection.")

        default_content_methods = tag.setdefault(
            'collection_default_content', {})

        if version in default_content_methods:
            raise TypeError(
                "Only one method can be marked with "
                "@collection_default_content for version '%s'." % (
                    _version_name(version)))
        self.version = version
        self.params = params

    def __call__(self, f):
        """Annotates the collection with the name of the method to call."""
        tag = _get_interface_tags()[LAZR_WEBSERVICE_EXPORTED]
        tag['collection_default_content'][self.version] = (
            f.__name__, self.params)
        return f


WEBSERVICE_ERROR = '__lazr_webservice_error__'

def webservice_error(status):
    """Mark the exception with the HTTP status code to use.

    That status code will be used by the view used to handle that kind of
    exceptions on the web service.

    This is only effective when the exception is raised from within a
    published method.  For example, if the exception is raised by the field's
    validation its specified status won't propagate to the response.
    """
    frame = sys._getframe(1)
    f_locals = frame.f_locals

    # Try to make sure we were called from a class def.
    if (f_locals is frame.f_globals) or ('__module__' not in f_locals):
        raise TypeError(
            "webservice_error() can only be used from within an exception "
            "definition.")

    f_locals[WEBSERVICE_ERROR] = int(status)

def error_status(status):
    """Make a Python 2.6 class decorator for the given status.

    Usage 1:
        @error_status(400)
        class FooBreakage(Exception):
            pass

    Usage 2 (legacy):
        class FooBreakage(Exception):
            pass
        error_status(400)(FooBreakage)

    That status code will be used by the view used to handle that kind of
    exceptions on the web service.

    This is only effective when the exception is raised from within a
    published method.  For example, if the exception is raised by the field's
    validation, its specified status won't propagate to the response.
    """
    status = int(status)
    def func(value):
        if not issubclass(value, Exception):
            raise TypeError('Annotated value must be an exception class.')
        old = getattr(value, WEBSERVICE_ERROR, None)
        if old is not None and old != status:
            raise ValueError('Exception already has an error status', old)
        setattr(value, WEBSERVICE_ERROR, status)
        return value
    return func


class _method_annotator:
    """Base class for decorators annotating a method.

    The actual method will be wrapped in an IMethod specification once the
    Interface is complete. So we save the annotations in an attribute of the
    method, and the class advisor invoked by export_as_webservice_entry() and
    export_as_webservice_collection() will do the final tagging.
    """

    def __call__(self, method):
        """Annotates the function with the fixed arguments."""
        # Everything in the function dictionary ends up as tagged value
        # in the interface method specification.
        annotations = method.__dict__.get(LAZR_WEBSERVICE_EXPORTED, None)
        if annotations is None:
            # Create a new versioned dict which associates
            # annotation data with the earliest active version of the
            # web service. Future @webservice_version annotations will
            # push later versions onto the VersionedDict, allowing
            # new versions to specify annotation data that conflicts
            # with old versions.
            #
            # Because we don't know the name of the earliest version
            # published by the web service (we won't know this until
            # runtime), we'll use None as the name of the earliest
            # version.
            annotations = VersionedDict()
            annotations.push(None)

            # The initial presumption is that an operation is not
            # published in the earliest version of the web service. An
            # @export_*_operation declaration will modify
            # annotations['type'] in place to signal that it is in
            # fact being published.
            annotations['type'] = REMOVED_OPERATION_TYPE
            method.__dict__[LAZR_WEBSERVICE_EXPORTED] = annotations
        self.annotate_method(method, annotations)
        return method

    def annotate_method(self, method, annotations):
        """Add annotations for method.

        This method must be implemented by subclasses.

        :param f: the method being annotated.
        :param annotations: the dict containing the method annotations.

        The annotations will copied to the lazr.webservice.exported tag
        by a class advisor.
        """
        raise NotImplemented


def annotate_exported_methods(interface):
    """Sets the 'lazr.webservice.exported' tag on exported method."""

    for name, method in interface.namesAndDescriptions(True):
        if not IMethod.providedBy(method):
            continue
        annotation_stack = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if annotation_stack is None:
            continue
        if annotation_stack.get('type') is None:
            continue

        # Make sure that each version of the web service defines
        # a self-consistent view of this method.
        for version, annotations in annotation_stack.stack:
            if annotations['type'] == REMOVED_OPERATION_TYPE:
                # The method is published in other versions of the web
                # service, but not in this one. Don't try to validate this
                # version's annotations.
                continue

            # Method is exported under its own name by default.
            if 'as' not in annotations:
                annotations['as'] = method.__name__

            # It's possible that call_with, operation_parameters, and/or
            # operation_returns_* weren't used.
            annotations.setdefault('call_with', {})
            annotations.setdefault('params', {})
            annotations.setdefault('return_type', None)

            # Make sure that all parameters exist and that we miss none.
            info = method.getSignatureInfo()
            defined_params = set(info['optional'])
            defined_params.update(info['required'])
            exported_params = set(annotations['params'])
            exported_params.update(annotations['call_with'])
            undefined_params = exported_params.difference(defined_params)
            if undefined_params and info['kwargs'] is None:
                raise TypeError(
                    'method "%s" doesn\'t have the following exported '
                    'parameters in version "%s": %s.' % (
                        method.__name__, _version_name(version),
                        ", ".join(sorted(undefined_params))))
            missing_params = set(
                info['required']).difference(exported_params)
            if missing_params:
                raise TypeError(
                    'method "%s" is missing definitions for parameter(s) '
                    'exported in version "%s": %s' % (
                        method.__name__, _version_name(version),
                        ", ".join(sorted(missing_params))))

            _update_default_and_required_params(annotations['params'], info)


def _update_default_and_required_params(params, method_info):
    """Set missing default/required based on the method signature."""
    optional = method_info['optional']
    required = method_info['required']
    for name, param_def in params.items():
        # If the method parameter is optional and the param didn't have
        # a default, set it to the same as the method.
        if name in optional and param_def.default is None:
            default = optional[name]

            # This is to work around the fact that all strings in
            # zope schema are expected to be unicode, whereas it's
            # really possible that the method's default is a simple
            # string.
            if isinstance(default, str) and IText.providedBy(param_def):
                default = unicode(default)
            param_def.default = default
            param_def.required = False
        elif name in required and param_def.default is not None:
            # A default was provided, so the parameter isn't required.
            param_def.required = False
        else:
            # Nothing to do for that case.
            pass


class call_with(_method_annotator):
    """Decorator specifying fixed parameters for exported methods."""

    def __init__(self, **params):
        """Specify fixed values for parameters."""
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations['call_with'] = self.params


class mutator_for(_method_annotator):
    """Decorator indicating that an exported method mutates a field.

    The method can be invoked through POST, or by setting a value for
    the given field as part of a PUT or PATCH request.
    """
    def __init__(self, field):
        """Specify the field for which this method is a mutator."""
        self.field = field

    def annotate_method(self, method, annotations):
        """See `_method_annotator`.

        Store information about the mutator method with the field.
        """

        if not self.field.readonly:
            raise TypeError("Only a read-only field can have a mutator "
                            "method.")

        # The mutator method must take only one argument, not counting
        # arguments with values fixed by call_with().
        free_params = _free_parameters(method, annotations)
        if len(free_params) != 1:
            raise TypeError("A mutator method must take one and only one "
                            "non-fixed argument. %s takes %d." %
                            (method.__name__, len(free_params)))

        # We need to keep mutator annotations in a separate dictionary
        # from the field's main annotations because we're not
        # processing the field.  We're processing a named operation,
        # and we have no idea where the named operation's current
        # version fits into the field's annotations.
        version, method_annotations = annotations.stack[-1]
        mutator_annotations = self.field.queryTaggedValue(
            LAZR_WEBSERVICE_MUTATORS)
        if version in mutator_annotations:
            raise TypeError(
                "A field can only have one mutator method for version %s; "
                "%s makes two." % (_version_name(version), method.__name__ ))
        mutator_annotations[version] = (method, dict(method_annotations))
        method_annotations['is_mutator'] = True


def _free_parameters(method, annotations):
    """Figure out which of a method's parameters are free.

    Parameters that have values fixed by call_with() are not free.
    """
    signature = fromFunction(method).getSignatureInfo()
    return (set(signature['required']) -
               set(annotations.get('call_with', {}).keys()))


class operation_for_version(_method_annotator):
    """Decorator specifying which version of the webservice is defined.

    Decorators processed after this one will decorate the given web
    service version and, by default, subsequent versions will inherit
    their values. Subsequent versions may provide conflicting values,
    but those values will not affect this version.
    """
    def __init__(self, version):
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.version = version

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # The annotations dict is a VersionedDict. Push a new dict
        # onto its stack, labeled with the version number, and copy in
        # the old version's annotations so that this version can
        # modify those annotations without destroying them.
        annotations.push(self.version)


class operation_removed_in_version(operation_for_version):
    """Decoration removing this operation from the web service.

    This operation will not be present in the given version of the web
    service, or any subsequent version, unless it's re-published with
    an export_*_operation method.
    """
    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # The annotations dict is a VersionedDict. Push a new dict
        # onto its stack, labeled with the version number. Make sure the
        # new dict is empty rather than copying the old annotations
        annotations.push(self.version, True)

        # We need to set a special 'type' so that lazr.restful can
        # easily distinguish a method that's not present in the latest
        # version from a method that was incompletely annotated.
        annotations['type'] = REMOVED_OPERATION_TYPE

class export_operation_as(_method_annotator):
    """Decorator specifying the name to export the method as."""

    def __init__(self, name):
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.name = name

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations['as'] = self.name


class rename_parameters_as(_method_annotator):
    """Decorator specifying the name to export the method parameters as."""

    def __init__(self, **params):
        """params is of the form method_parameter_name=webservice_name."""
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        param_defs = annotations.get('params')
        if param_defs is None:
            raise TypeError(
                '"%s" isn\'t exported on the webservice.' % method.__name__)
        for name, export_as in self.params.items():
            if name not in param_defs:
                raise TypeError(
                    'rename_parameters_as(): no "%s" parameter is exported.' %
                        name)
            param_defs[name].__name__ = export_as


class operation_parameters(_method_annotator):
    """Specify the parameters taken by the exported operation.

    The decorator takes a list of `IField` describing the parameters. The name
    of the underlying method parameter is taken from the argument name.
    """
    def __init__(self, **params):
        """params is of the form method_parameter_name=Field()."""
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # It's possible that another decorator already created the params
        # annotation.
        params = annotations.setdefault('params', {})
        for name, param in self.params.items():
            if not IField.providedBy(param):
                raise TypeError(
                    'export definition of "%s" in method "%s" must '
                    'provide IField: %r' % (name, method.__name__, param))
            if name in params:
                raise TypeError(
                    "'%s' parameter is already defined." % name)

            # By default, parameters are exported under their own name.
            param.__name__ = name

            params[name] = param


class operation_returns_entry(_method_annotator):
    """Specify that the exported operation returns an entry.

    The decorator takes a single argument: an interface that's been
    exported as an entry.
    """

    def __init__(self, schema):
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        if not IInterface.providedBy(schema):
            raise TypeError('Entry type %s does not provide IInterface.'
                            % schema)
        self.return_type = Reference(schema=schema)

    def annotate_method(self, method, annotations):
        annotations['return_type'] = self.return_type


class operation_returns_collection_of(_method_annotator):
    """Specify that the exported operation returns a collection.

    The decorator takes a single argument: an interface that's been
    exported as an entry.
    """

    def __init__(self, schema):
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        if not IInterface.providedBy(schema):
            raise TypeError('Collection value type %s does not provide '
                            'IInterface.' % schema)
        self.return_type = CollectionField(
            value_type=Reference(schema=schema))

    def annotate_method(self, method, annotations):
        annotations['return_type'] = self.return_type


class _export_operation(_method_annotator):
    """Basic implementation for the webservice operation method decorators."""

    # Should be overriden in subclasses with the string to use as 'type'.
    type = None

    def __init__(self):
        _check_called_from_interface_def('%s()' % self.__class__.__name__)

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations['type'] = self.type


class export_factory_operation(_export_operation):
    """Decorator marking a method as being a factory on the webservice."""
    type = 'factory'

    def __init__(self, interface, field_names):
        """Creates a factory decorator.

        :param interface: The interface where fields specified in field_names
            are looked-up.
        :param field_names: The names of the fields in the schema that
            are used as parameters by this factory.
        """
        # pylint: disable-msg=W0231
        _check_called_from_interface_def('%s()' % self.__class__.__name__)
        self.interface = interface
        self.params = {}
        for name in field_names:
            field = interface.get(name)
            if field is None:
                raise TypeError("%s doesn't define '%s'." % (
                                interface.__name__, name))
            if not IField.providedBy(field):
                raise TypeError("%s.%s doesn't provide IField." % (
                                interface.__name__, name))
            self.params[name] = copy_field(field)

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        super(export_factory_operation, self).annotate_method(
            method, annotations)
        annotations['creates'] = self.interface
        annotations['params'] = self.params
        annotations['return_type'] = ObjectLink(schema=self.interface)


class cache_for(_method_annotator):
    """Decorator specifying how long a response may be cached by a client."""

    def __init__(self, duration):
        """Specify the duration, in seconds, of the caching resource."""
        if not isinstance(duration, (int, long)):
            raise TypeError(
                'Caching duration should be int or long, not %s' %
                duration.__class__.__name__)
        if duration <= 0:
            raise ValueError(
                'Caching duration should be a positive number: %s' % duration)
        self.duration = duration

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations['cache_for'] = self.duration


class export_read_operation(_export_operation):
    """Decorator marking a method for export as a read operation."""
    type = 'read_operation'


class export_write_operation(_export_operation):
    """Decorator marking a method for export as a write operation."""
    type = "write_operation"


class export_destructor_operation(_export_operation):
    """Decorator indicating that an exported method destroys an entry.

    The method will be invoked when the client sends a DELETE request to
    the entry.
    """
    type = "destructor"

    def annotate_method(self, method, annotation_stack):
        """See `_method_annotator`.

        Store information about the mutator method with the method.

        Every version must have a self-consistent set of annotations.
        """
        super(export_destructor_operation, self).annotate_method(
              method, annotation_stack)
        # The mutator method must take no arguments, not counting
        # arguments with values fixed by call_with().
        signature = fromFunction(method).getSignatureInfo()
        for version, annotations in annotation_stack.stack:
            if annotations['type'] == REMOVED_OPERATION_TYPE:
                continue
            free_params = _free_parameters(method, annotations)
            if len(free_params) != 0:
                raise TypeError(
                    "A destructor method must take no non-fixed arguments. "
                    'In version %s, the "%s" method takes %d: "%s".' % (
                        _version_name(version), method.__name__,
                        len(free_params), '", "'.join(free_params))
                        )


def _check_tagged_interface(interface, type):
    """Make sure that the interface is exported under the proper type."""
    if not isinstance(interface, InterfaceClass):
        raise TypeError('not an interface.')

    tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    if tag is None:
        raise TypeError(
            "'%s' isn't tagged for webservice export." % interface.__name__)
    elif tag['type'] != type:
        art = 'a'
        if type == 'entry':
            art = 'an'
        raise TypeError(
            "'%s' isn't exported as %s %s." % (interface.__name__, art, type))


def generate_entry_interfaces(interface, *versions):
    """Create IEntry subinterfaces based on the tags in `interface`.

    :param interface: The data model interface to use as the basis
        for a number of IEntry subinterfaces.
    :param versions: The list of versions published by this service, earliest
        versions first.
    :return: A list of 2-tuples (version, interface), in the same order
        as `versions`.
    """

    _check_tagged_interface(interface, 'entry')
    versions = list(versions)

    # First off, make sure any given version defines only one
    # destructor method.
    destructor_for_version = {}
    for name, method in interface.namesAndDescriptions(True):
        if not IMethod.providedBy(method):
            continue
        method_annotations = method.queryTaggedValue(
            LAZR_WEBSERVICE_EXPORTED)
        if method_annotations is None:
            continue
        for version, annotations in method_annotations.stack:
            if annotations.get('type') == export_destructor_operation.type:
                destructor = destructor_for_version.get(version)
                if destructor is not None:
                    raise TypeError(
                        'An entry can only have one destructor method for '
                        'version %s; %s and %s make two.' % (
                            _version_name(version), method.__name__,
                            destructor.__name__))
                destructor_for_version[version] = method

    # Next, we'll normalize each published field. A normalized field
    # has a set of annotations for every version. We'll make a list of
    # the published fields, which we'll iterate over once for each
    # version.
    fields = getFields(interface).items()
    tags_for_published_fields = []
    for name, field in fields:
        tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag_stack is None:
            # This field is not published at all.
            continue
        error_message_prefix = (
            'Field "%s" in interface "%s": ' % (name, interface.__name__))
        _normalize_field_annotations(field, versions, error_message_prefix)
        tags_for_published_fields.append((name, field, tag_stack.stack))

    generated_interfaces = []
    for version in versions:
        attrs = {}
        for name, field, tag_stack in tags_for_published_fields:
            tags = [tags for tag_version, tags in tag_stack
                    if tag_version == version]
            tags = tags[0]
            if tags.get('exported') is False:
                continue
            mutated_by, mutated_by_annotations = tags.get(
                'mutator_annotations', (None, {}))
            readonly = (field.readonly and mutated_by is None)
            attrs[tags['as']] = copy_field(
                field, __name__=tags['as'], readonly=readonly)
        class_name = _versioned_class_name(
            "%sEntry" % interface.__name__, version)
        entry_interface = InterfaceClass(
            class_name, bases=(IEntry, ), attrs=attrs,
            __doc__=interface.__doc__, __module__=interface.__module__)

        tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        entry_interface.setTaggedValue(LAZR_WEBSERVICE_NAME, dict(
            singular=tag['singular_name'],
            plural=tag['plural_name']))
        generated_interfaces.append((version, entry_interface))
    return generated_interfaces


def generate_entry_adapters(content_interface, webservice_interfaces):
    """Create classes adapting from content_interface to webservice_interfaces.

    Unlike with generate_collection_adapter and
    generate_operation_adapter, the simplest implementation generates
    an entry adapter for every version at the same time.

    :param content_interface: The original data model interface being exported.

    :param webservice_interfaces: A list of 2-tuples
     (version string, webservice interface) containing the generated
     interfaces for each version of the web service.

    :param return: A list of 2-tuples (version string, adapter class)
    """
    _check_tagged_interface(content_interface, 'entry')

    # Go through the fields and build up a picture of what this entry looks
    # like for every version.
    adapters_by_version = {}
    for name, field in getFields(content_interface).items():
        tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag_stack is None:
            continue
        for tags_version, tags in tag_stack.stack:
            # Has this version been mentioned before? If not, add a
            # dictionary to adapters_by_version. This dictionary will
            # be turned into an adapter class for this version.
            adapter_dict = adapters_by_version.setdefault(tags_version, {})

            # Figure out the mutator for this version and add it to
            # this version's adapter class dictionary.
            if tags.get('exported') is False:
                continue
            mutator, annotations = tags.get(
                'mutator_annotations', (None, {}))

            if mutator is None:
                property = Passthrough(name, 'context')
            else:
                property = PropertyWithMutator(
                    name, 'context', mutator, annotations)
            adapter_dict[tags['as']] = property

    adapters = []
    for version, webservice_interface in webservice_interfaces:
        if not isinstance(webservice_interface, InterfaceClass):
            raise TypeError('webservice_interface is not an interface.')
        class_dict = adapters_by_version.get(version, {})

        class_dict['schema'] = webservice_interface
        class_dict['__doc__'] = webservice_interface.__doc__
        # The webservice interface class name already includes the version
        # string, so there's no reason to add it again to the end
        # of the class name.
        classname = "%sAdapter" % webservice_interface.__name__[1:]
        factory = type(classname, (Entry,), class_dict)
        classImplements(factory, webservice_interface)
        protect_schema(
            factory, webservice_interface, write_permission=CheckerPublic)
        adapters.append((version, factory))
    return adapters


def params_with_dereferenced_user(params):
    """Make a copy of the given parameters with REQUEST_USER dereferenced."""
    params = params.copy()
    for name, value in params.items():
        if value is REQUEST_USER:
            params[name] = getUtility(
                IWebServiceConfiguration).get_request_user()
    return params


class PropertyWithMutator(Passthrough):
    """A property with a mutator method."""

    def __init__(self, name, context, mutator, annotations):
        super(PropertyWithMutator, self).__init__(name, context)
        self.mutator = mutator.__name__
        self.annotations = annotations

    def __set__(self, obj, new_value):
        """Call the mutator method to set the value."""
        params = params_with_dereferenced_user(
            self.annotations.get('call_with', {}))
        # Error checking code in mutator_for() guarantees that there
        # is one and only one non-fixed parameter for the mutator
        # method.
        getattr(obj.context, self.mutator)(new_value, **params)


class CollectionEntrySchema:
    """A descriptor for converting a model schema into an entry schema.

    The entry schema class for a resource may not have been defined at
    the time the collection adapter is generated, but the data model
    class certainly will have been. This descriptor performs the lookup
    as needed, at runtime.
    """

    def __init__(self, model_schema):
        """Initialize with a model schema."""
        self.model_schema = model_schema

    def __get__(self, instance, owner):
        """Look up the entry schema that adapts the model schema."""
        if instance is None or instance.request is None:
            request = get_current_web_service_request()
        else:
            request = instance.request
        request_interface = getUtility(
            IWebServiceVersion, name=request.version)
        entry_class = getGlobalSiteManager().adapters.lookup(
            (self.model_schema, request_interface), IEntry)
        if entry_class is None:
            return None
        return EntryAdapterUtility(entry_class).entry_interface


class BaseCollectionAdapter(Collection):
    """Base for generated ICollection adapter."""

    # These attributes will be set in the generated subclass.
    method_name = None
    params = None

    def find(self):
        """See `ICollection`."""
        method = getattr(self.context, self.method_name)
        params = params_with_dereferenced_user(self.params)
        return method(**params)


def generate_collection_adapter(interface, version=None):
    """Create a class adapting from interface to ICollection."""
    _check_tagged_interface(interface, 'collection')

    tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    default_content_by_version = tag['collection_default_content']
    assert (version in default_content_by_version), (
        "'%s' isn't tagged for export to web service "
        "version '%s'." % (interface.__name__, version))
    method_name, params = default_content_by_version[version]
    entry_schema = tag['collection_entry_schema']
    class_dict = {
        'entry_schema' : CollectionEntrySchema(entry_schema),
        'method_name': method_name,
        'params': params,
        '__doc__': interface.__doc__,
        }
    classname = _versioned_class_name(
        "%sCollectionAdapter" % interface.__name__[1:],
        version)
    factory = type(classname, (BaseCollectionAdapter,), class_dict)

    protect_schema(factory, ICollection)
    return factory


class BaseResourceOperationAdapter(ResourceOperation):
    """Base class for generated operation adapters."""

    def _getMethodParameters(self, kwargs):
        """Return the method parameters.

        This takes the validated parameters list and handle any possible
        renames, and adds the parameters fixed using @call_with.

        :returns: a dictionary.
        """
        # Handle renames.
        renames = dict(
            (param_def.__name__, orig_name)
            for orig_name, param_def in self._export_info['params'].items()
            if param_def.__name__ != orig_name)
        params = {}
        for name, value in kwargs.items():
            name = renames.get(name, name)
            params[name] = value

        # Handle fixed parameters.
        params.update(params_with_dereferenced_user(
                self._export_info['call_with']))
        return params

    def call(self, **kwargs):
        """See `ResourceOperation`."""
        params = self._getMethodParameters(kwargs)

        # For responses to GET requests, tell the client to cache the
        # response.
        if (IResourceGETOperation.providedBy(self)
            and 'cache_for' in self._export_info):
            self.request.response.setHeader(
                'Cache-control', 'max-age=%i'
                % self._export_info['cache_for'])

        result = getattr(self.context, self._method_name)(**params)
        return self.encodeResult(result)


class BaseFactoryResourceOperationAdapter(BaseResourceOperationAdapter):
    """Base adapter class for factory operations."""

    def call(self, **kwargs):
        """See `ResourceOperation`.

        Factory uses the 201 status code on success and sets the Location
        header to the URL to the created object.
        """
        params = self._getMethodParameters(kwargs)
        result = getattr(self.context, self._method_name)(**params)
        response = self.request.response
        response.setStatus(201)
        response.setHeader('Location', absoluteURL(result, self.request))
        return u''


def generate_operation_adapter(method, version=None):
    """Create an IResourceOperation adapter for the exported method.

    :param version: The name of the version for which to generate an
    operation adapter. None means to generate an adapter for the earliest
    version.
    """

    if not IMethod.providedBy(method):
        raise TypeError("%r doesn't provide IMethod." % method)
    tag = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    if tag is None:
        raise TypeError(
            "'%s' isn't tagged for webservice export." % method.__name__)
    match = [annotations for version_name, annotations in tag.stack
             if version_name==version]
    if len(match) == 0:
        raise AssertionError("'%s' isn't tagged for export to web service "
                             "version '%s'" % (method.__name__, version))
    tag = match[0]
    if version is None:
        version = getUtility(IWebServiceConfiguration).active_versions[0]

    bases = (BaseResourceOperationAdapter, )
    if tag['type'] == 'read_operation':
        prefix = 'GET'
        provides = IResourceGETOperation
    elif tag['type'] in ('factory', 'write_operation'):
        provides = IResourcePOSTOperation
        prefix = 'POST'
        if tag['type'] == 'factory':
            bases = (BaseFactoryResourceOperationAdapter,)
    elif tag['type'] == 'destructor':
        provides = IResourceDELETEOperation
        prefix = 'DELETE'
    else:
        raise AssertionError('Unknown method export type: %s' % tag['type'])

    return_type = tag['return_type']
    if return_type is None:
        return_type = None

    name = _versioned_class_name(
        '%s_%s_%s' % (prefix, method.interface.__name__, tag['as']),
        version)
    class_dict = {'params' : tuple(tag['params'].values()),
             'return_type' : return_type,
             '_export_info': tag,
             '_method_name': method.__name__,
             '__doc__': method.__doc__}

    if tag['type'] == 'write_operation':
        class_dict['send_modification_event'] = True
    factory = type(name, bases, class_dict)
    classImplements(factory, provides)
    protect_schema(factory, provides)

    return factory


def _normalize_field_annotations(field, versions, error_prefix=''):
    """Make sure a field has annotations for every published version.

    If a field lacks annotations for a given version, it will not show
    up in that version's adapter interface. This function makes sure
    version n+1 inherits version n's behavior, by copying it that
    behavior over.

    If the earliest version has both an implicit definition (from
    keyword arguments) and an explicit definition, the two definitions
    are consolidated.

    Since we have the list of versions available, this is also a good
    time to do some error checking: make sure that version annotations
    are not duplicated or in the wrong order.

    Finally, this is a good time to integrate the mutator annotations
    into the field annotations.
    """
    versioned_dict = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    mutator_annotations = field.queryTaggedValue(LAZR_WEBSERVICE_MUTATORS)

    # If the first version is None and the second version is the
    # earliest version, consolidate the two versions.
    earliest_version = versions[0]
    stack = versioned_dict.stack

    if (len(stack) >= 2
        and stack[0][0] is None and stack[1][0] == earliest_version):

        # Make sure the implicit definition of the earliest version
        # doesn't conflict with the explicit definition. The only
        # exception is the 'as' value, which is implicitly defined
        # by the system, not explicitly by the user.
        for key, value in stack[1][1].items():
            implicit_value = stack[0][1].get(key)
            if (implicit_value != value and
                not (key == 'as' and implicit_value == field.__name__)):
                raise ValueError(
                    error_prefix + 'Annotation "%s" has conflicting values '
                    'for the earliest version: "%s" (from keyword arguments) '
                    'and "%s" (defined explicitly).' % (
                        key, implicit_value, value))
        stack[0][1].update(stack[1][1])
        stack.remove(stack[1])

    # Now that we know the name of the earliest version, get rid of
    # any None at the beginning of the stack.
    if stack[0][0] is None:
        stack[0] = (earliest_version, stack[0][1])

    # Make sure there is at most one mutator for the earliest version.
    # If there is one, move it from the mutator-specific dictionary to
    # the normal tag stack.
    implicit_earliest_mutator = mutator_annotations.get(None, None)
    explicit_earliest_mutator = mutator_annotations.get(earliest_version, None)
    if (implicit_earliest_mutator is not None
        and explicit_earliest_mutator is not None):
        raise ValueError(
            error_prefix + " Both implicit and explicit mutator definitions "
            "found for earliest version %s." % earliest_version)
    earliest_mutator = implicit_earliest_mutator or explicit_earliest_mutator
    if earliest_mutator is not None:
        stack[0][1]['mutator_annotations'] = earliest_mutator

    # Do some error checking.
    max_index = -1
    for version, tags in versioned_dict.stack:
        try:
            version_index = versions.index(version)
        except ValueError:
            raise ValueError(
                error_prefix + 'Unrecognized version "%s".' % version)
        if version_index == max_index:
            raise ValueError(
                error_prefix + 'Duplicate annotations for version '
                '"%s".' % version)
        if version_index < max_index:
            raise ValueError(
                error_prefix + 'Version "%s" defined after '
                'the later version "%s".' % (version, versions[max_index]))
        max_index = version_index

    # Fill out the stack so that there is one set of tags for each
    # version.
    if stack[0][0] == earliest_version:
        new_stack = [stack[0]]
    else:
        # The field is not initially published.
        new_stack = (earliest_version, dict(published=False))
    most_recent_tags = new_stack[0][1]
    most_recent_mutator_tags = earliest_mutator
    for version in versions[1:]:
        most_recent_mutator_tags = mutator_annotations.get(
            version, most_recent_mutator_tags)
        match = [(stack_version, stack_tags)
                 for stack_version, stack_tags in stack
                 if stack_version == version]
        if len(match) == 0:
            # This version has no tags of its own. Use a copy of the
            # most recent tags.
            new_stack.append((version, copy.deepcopy(most_recent_tags)))
        else:
            # This version has tags of its own. Use them unaltered,
            # and set them up to be used in the future.
            new_stack.append(match[0])
            most_recent_tags = match[0][1]

        # Install a (possibly inherited) mutator for this field in
        # this version.
        if most_recent_mutator_tags is not None:
            new_stack[-1][1]['mutator_annotations'] = copy.deepcopy(
                most_recent_mutator_tags)

    versioned_dict.stack = new_stack
    return field


def _version_name(version):
    """Return a human-readable version name.

    If `version` is None (indicating the as-yet-unknown earliest
    version), returns "(earliest version)". Otherwise returns the version
    name.
    """
    if version is None:
        return "(earliest version)"
    return version


def _versioned_class_name(base_name, version):
    """Create a class name incorporating the given version string."""
    if version is None:
        # We need to incorporate the version into a Python class name,
        # but we won't find out the name of the earliest version until
        # runtime. Use a generic string that won't conflict with a
        # real version string.
        version = "__Earliest"
    name = "%s_%s" % (base_name, version.encode('utf8'))
    return make_identifier_safe(name)
