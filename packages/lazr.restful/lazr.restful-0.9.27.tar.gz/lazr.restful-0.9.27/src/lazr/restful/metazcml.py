# Copyright 2008 Canonical Ltd.  All rights reserved.

"""ZCML registration directives for the LAZR webservice framework."""

__metaclass__ = type
__all__ = []


import inspect

from zope.component import getUtility
from zope.component.zcml import handler
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.interface.interfaces import IInterface


from lazr.restful.declarations import (
    LAZR_WEBSERVICE_EXPORTED, OPERATION_TYPES, REMOVED_OPERATION_TYPE,
    generate_collection_adapter, generate_entry_adapters,
    generate_entry_interfaces, generate_operation_adapter)
from lazr.restful.error import WebServiceExceptionView

from lazr.restful.interfaces import (
    ICollection, IEntry, IResourceDELETEOperation, IResourceGETOperation,
    IResourceOperation, IResourcePOSTOperation, IWebServiceClientRequest,
    IWebServiceConfiguration, IWebServiceVersion)


class IRegisterDirective(Interface):
    """Directive to hook up webservice based on the declarations in a module.
    """
    module = GlobalObject(
        title=u'Module which will be inspected for webservice declarations')


def generate_and_register_entry_adapters(interface, info):
    """Generate an entry adapter for every version of the web service.

    This code generates an IEntry subinterface for every version, each
    subinterface based on the annotations in `interface` for that
    version. It then generates a set of factory classes for each
    subinterface, and registers each as an adapter for the appropriate
    version and version-specific interface.
    """
    # Get the list of versions.
    config = getUtility(IWebServiceConfiguration)
    versions = list(config.active_versions)

    # Generate an interface and an adapter for every version.
    web_interfaces = generate_entry_interfaces(interface, *versions)
    web_factories = generate_entry_adapters(interface, web_interfaces)
    provides = IEntry
    for i in range(0, len(web_interfaces)):
        interface_version, web_interface = web_interfaces[i]
        factory_version, factory = web_factories[i]
        assert factory_version==interface_version, (
            "Generated interface and factory versions don't match up! "
            '%s vs. %s' % (factory_version, interface_version))

        # If this is the earliest version, register against a generic
        # request interface rather than a version-specific one.  This
        # will make certain tests require less setup.
        if interface_version == versions[0]:
            interface_version = None
        register_adapter_for_version(factory, interface, interface_version,
                                     IEntry, '', info)


def ensure_correct_version_ordering(name, version_list):
    """Make sure that a list mentions versions from earliest to latest.

    If an earlier version shows up after a later version, this is a
    sign that a developer was confused about version names when
    annotating the web service.

    :param name: The name of the object annotated with the
        possibly mis-ordered versions.

    :param version_list: The list of versions found in the interface.

    :raise AssertionError: If the given version list is not a
        earlier-to-later ordering of a subset of the web service's
        versions.
    """
    configuration = getUtility(IWebServiceConfiguration)
    actual_versions = configuration.active_versions
    # Replace None with the actual version number of the earliest
    # version.
    try:
        earliest_version_pos = version_list.index(None)
        version_list = list(version_list)
        version_list[earliest_version_pos] = actual_versions[0]
    except ValueError:
        # The earliest version was not mentioned in the version list.
        # Do nothing.
        pass

    # Sort version_list according to the list of actual versions.
    # If the sorted list is different from the unsorted list, at
    # least one version is out of place.
    def compare(x, y):
        return cmp (actual_versions.index(x), actual_versions.index(y))
    sorted_version_list = sorted(version_list, cmp=compare)
    if sorted_version_list != version_list:
        bad_versions = '", "'.join(version_list)
        good_versions = '", "'.join(sorted_version_list)
        msg = ('Annotations on "%s" put an earlier version on top of a '
               'later version: "%s". The correct order is: "%s".')
        raise AssertionError, msg % (name, bad_versions, good_versions)


def register_adapter_for_version(factory, interface, version_name,
                                 provides, name, info):
    """A version-aware wrapper for the registerAdapter operation.

    During web service generation we often need to register an adapter
    for a particular version of the web service. The way to do this is
    to register a multi-adapter using the interface being adapted to,
    plus the marker interface for the web service version.

    These marker interfaces are not available when the web service is
    being generated, but the version strings are available. So methods
    like register_webservice_operations use this function as a handler
    for the second stage of ZCML processing.

    This function simply looks up the appropriate marker interface and
    calls Zope's handler('registerAdapter').
    """
    if version_name is None:
        # This adapter is for the earliest supported version. Register
        # it against the generic IWebServiceClientRequest interface,
        # which is the superclass of the marker interfaces for every
        # specific version.
        marker = IWebServiceClientRequest
    else:
        # Look up the marker interface for the given version. This
        # will also ensure the given version string has an
        # IWebServiceVersion utility registered for it, and is not
        # just a random string.
        marker = getUtility(IWebServiceVersion, name=version_name)

    handler('registerAdapter', factory, (interface, marker),
            provides, name, info)

def find_exported_interfaces(module):
    """Find all the interfaces in a module marked for export.

    It also includes exceptions that represents errors on the webservice.

    :return: iterator of interfaces.
    """
    for name, interface in inspect.getmembers(module, inspect.isclass):
        if issubclass(interface, Exception):
            if getattr(interface, '__lazr_webservice_error__', None) is None:
                continue
            yield interface

        if not IInterface.providedBy(interface):
            continue
        tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag is None:
            continue
        if tag['type'] in ['entry', 'collection']:
            yield interface


def register_webservice(context, module):
    """Generate and register web service adapters.

    All interfaces in the module are inspected, and appropriate interfaces and
    adapters are generated and registered for the ones marked for export on
    the web service.
    """
    if not inspect.ismodule(module):
        raise TypeError("module attribute must be a module: %s, %s" %
                        module, type(module))
    for interface in find_exported_interfaces(module):
        if issubclass(interface, Exception):
            register_exception_view(context, interface)
            continue

        tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag['type'] == 'entry':
            context.action(
                discriminator=('webservice entry interface', interface),
                    callable=generate_and_register_entry_adapters,
                    args=(interface, context.info),
                    )
        elif tag['type'] == 'collection':
            for version in tag['collection_default_content'].keys():
                factory = generate_collection_adapter(interface, version)
                provides = ICollection
                context.action(
                    discriminator=(
                        'webservice versioned adapter', interface, provides,
                        '', version),
                    callable=register_adapter_for_version,
                    args=(factory, interface, version, provides, '',
                          context.info),
                    )
        else:
            raise AssertionError('Unknown export type: %s' % tag['type'])
        context.action(
            discriminator=('webservice versioned operations', interface),
            args=(context, interface),
            callable=generate_and_register_webservice_operations)


def generate_and_register_webservice_operations(context, interface):
    """Create and register adapters for all exported methods.

    Different versions of the web service may publish the same
    operation differently or under different names.
    """
    # First of all, figure out when to stop publishing field mutators
    # as named operations.
    config = getUtility(IWebServiceConfiguration)
    if config.last_version_with_mutator_named_operations is None:
        no_mutator_operations_after = None
        block_mutator_operations_as_of_version = None
    else:
        no_mutator_operations_after = config.active_versions.index(
            config.last_version_with_mutator_named_operations)
        if len(config.active_versions) > no_mutator_operations_after+1:
            block_mutator_operations_as_of_version = config.active_versions[
                no_mutator_operations_after+1]
        else:
            block_mutator_operations_as_of_version = None

    for name, method in interface.namesAndDescriptions(True):
        tag = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag is None or tag['type'] not in OPERATION_TYPES:
            # This method is not published as a named operation.
            continue

        # First, make sure that this method was annotated with the
        # versions in the right order.
        ensure_correct_version_ordering(
            interface.__name__ + '.' + method.__name__, tag.dict_names)

        operation_name = None
        # If an operation's name does not change between version n and
        # version n+1, we want lookups for requests that come in for
        # version n+1 to find the registered adapter for version n. This
        # happens automatically. But if the operation name changes
        # (because the operation is now published under a new name, or
        # because the operation has been removed), we need to register a
        # masking adapter: something that will stop version n+1's lookups
        # from finding the adapter registered for version n. To this end
        # we keep track of what the operation looked like in the previous
        # version.
        previous_operation_name = None
        previous_operation_provides = None
        operation_registered_as_mutator = False
        for version, tag in tag.stack:
            if tag['type'] == REMOVED_OPERATION_TYPE:
                # This operation is not present in this version.
                # We'll represent this by setting the operation_name
                # to None. If the operation was not present in the
                # previous version either (or there is no previous
                # version), previous_operation_name will also be None
                # and nothing will happen. If the operation was
                # present in the previous version,
                # previous_operation_name will not be None, and the
                # code that handles name changes will install a
                # masking adapter.
                operation_name = None
                operation_provides = None
                factory = None

                # If there are any other tags besides 'type', it means
                # that the developer tried to annotate a method for a
                # version where the method isn't published. Let's warn
                # them about it.
                #
                # (We can't make this check when the annotation
                # happens, because it will reject a method that uses
                # an annotation like @export_operation_as before using
                # an annotation like @export_read_operation. That's a
                # little sloppy, but it's not bad enough to warrant an
                # exception.)
                tag_names = list(tag.keys())
                if tag_names != ['type']:
                    tag_names.remove('type')
                    raise AssertionError(
                        'Method "%s" contains annotations for version "%s", '
                        'even though it\'s not published in that version. '
                        'The bad annotations are: "%s".' % (
                            method.__name__, version, '", "'.join(tag_names)))
            else:
                if tag['type'] == 'read_operation':
                    operation_provides = IResourceGETOperation
                elif tag['type']in ['factory', 'write_operation']:
                    operation_provides = IResourcePOSTOperation
                elif tag['type'] in ['destructor']:
                    operation_provides = IResourceDELETEOperation
                else:
                    # We know it's not REMOVED_OPERATION_TYPE, because
                    # that case is handled above.
                    raise AssertionError(
                        'Unknown operation type: %s' % tag['type'])

                operation_name = tag.get('as')
                if tag['type'] in ['destructor']:
                    operation_name = ''

                if version is None:
                    this_version_index = 0
                else:
                    this_version_index = config.active_versions.index(
                        version)
                if (tag.get('is_mutator', False)
                    and (no_mutator_operations_after is None
                         or no_mutator_operations_after < this_version_index)):

                    # This is a mutator method, and in this version,
                    # mutator methods are not published as named
                    # operations at all. Block any lookup of the named
                    # operation from succeeding.
                    #
                    # This will save us from having to do another
                    # de-registration later.
                    factory = _mask_adapter_registration
                    operation_registered_as_mutator = False
                else:
                    factory = generate_operation_adapter(method, version)

            # Operations are looked up by name. If the operation's
            # name has changed from the previous version to this
            # version, or if the operation was removed in this
            # version, we need to block lookups of the previous name
            # from working.
            if (operation_name != previous_operation_name
                and previous_operation_name is not None):
                register_adapter_for_version(
                    _mask_adapter_registration, interface, version,
                    previous_operation_provides, previous_operation_name,
                    context.info)

            # If the operation exists in this version (ie. its name is
            # not None), register it using this version's name.
            if operation_name is not None:
                register_adapter_for_version(
                    factory, interface, version, operation_provides,
                    operation_name, context.info)
                if tag.get('is_mutator'):
                    operation_registered_as_mutator = True
            previous_operation_name = operation_name
            previous_operation_provides = operation_provides

        if (operation_registered_as_mutator and
            block_mutator_operations_as_of_version is not None):
            # The operation was registered as a mutator, and it never
            # got de-registered. De-register it now.
            register_adapter_for_version(
                _mask_adapter_registration, interface,
                block_mutator_operations_as_of_version,
                previous_operation_provides, previous_operation_name,
                context.info)

def _mask_adapter_registration(*args):
    """A factory function that stops an adapter lookup from succeeding.

    This function is registered when it's necessary to explicitly stop
    some part of web service version n from being visible to version n+1.
    """
    return None


def register_exception_view(context, exception):
    """Register WebServiceExceptionView to handle exception on the webservice.
    """
    context.action(
        discriminator=(
            'view', exception, 'index.html', IWebServiceClientRequest,
            IWebServiceClientRequest),
        callable=handler,
        args=('registerAdapter',
              WebServiceExceptionView, (exception, IWebServiceClientRequest),
              Interface, 'index.html', context.info),
        )


