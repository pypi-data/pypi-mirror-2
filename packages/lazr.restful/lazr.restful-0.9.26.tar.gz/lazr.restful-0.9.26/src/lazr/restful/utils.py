# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Various utility functions."""

__metaclass__ = type
__all__ = [
    'camelcase_to_underscore_separated',
    'get_current_browser_request',
    'get_current_web_service_request',
    'implement_from_dict',
    'make_identifier_safe',
    'safe_js_escape',
    'safe_hasattr',
    'smartquote',
    'simple_popen2',
    'tag_request_with_version_name',
    'VersionedDict',
    ]


import cgi
import copy
import re
import string
import subprocess

from simplejson import encoder

from zope.component import getUtility
from zope.schema import getFieldsInOrder
from zope.interface import alsoProvides, classImplements

from lazr.restful.interfaces import (
    IWebServiceClientRequest, IWebServiceVersion)


missing = object()


class VersionedDict(object):
    """A stack of named dictionaries.

    Most access to the stack actually operates on the dictionary on
    top of the stack. Dictionary access doesn't work when the stack is
    empty.

    When you push a named dictionary onto the stack, it is populated
    by a deep copy of the next highest dictionary in the stack. You
    can push an empty dictionary onto the stack by passing empty=True
    in to the push() method.
    """
    missing = object()

    def __init__(self, name=None):
        """Initialize the bleed-through dictionary."""
        self.stack = []
        if name is not None:
            self.push(name)

    def push(self, name, empty=False):
        """Pushes a dictionary onto the stack.

        :arg name: The name of the dictionary to push.
        :arg empty: If True, the dictionary will be created empty
                    rather than being populated with a deep copy of
                    the dictionary below it.
        """
        if empty or len(self.stack) == 0:
            dictionary = {}
        else:
            stack_top = self.stack[-1][1]
            dictionary = copy.deepcopy(stack_top)
        self.stack.append((name, dict(dictionary)))

    def pop(self):
        """Pop a tuple representing a dictionary from the stack.

        :return: A 2-tuple (name, dict). 'name' is the name of the
        dictionary within the VersionedDict; 'dict' is the contents
        of the dictionary.
        """
        return self.stack.pop()

    @property
    def dict_names(self):
        """Return the names of dictionaries in the stack."""
        return [item[0] for item in self.stack if item is not None]

    @property
    def is_empty(self):
        """Is the stack empty?"""
        return len(self.stack) == 0

    def setdefault(self, key, value):
        """Get a from the top of the stack, setting it if not present."""
        return self.stack[-1][1].setdefault(key, value)

    def __contains__(self, key):
        """Check whether a key is visible in the stack."""
        return self.get(key, missing) is not missing

    def __getitem__(self, key):
        """Look up an item somewhere in the stack."""
        if self.is_empty:
            raise KeyError(key)
        return self.stack[-1][1][key]

    def get(self, key, default=None):
        """Look up an item somewhere in the stack, with default fallback."""
        if self.is_empty:
            return default
        return self.stack[-1][1].get(key, default)

    def items(self):
        """Return a merged view of the items in the dictionary."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        return self.stack[-1][1].items()

    def __setitem__(self, key, value):
        """Set a value in the dict at the top of the stack."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        self.stack[-1][1][key] = value

    def __delitem__(self, key):
        """Delete a value from the dict at the top of the stack."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        del self.stack[-1][1][key]


def implement_from_dict(class_name, interface, values, superclass=object):
    """Return a class that implements an interface's attributes.

    :param interface: The interface to implement.
    :param superclass: The superclass of the class to be generated.
    :param values: A dict of values to use when generating the class.
    :return: A class that implements 'interface'. Any attributes given
             values in 'values' will have those values in the generated
             interface. Other attributes will have their default
             values as defined in the interface. Attributes with no
             default values, will not be present.
    """
    class_dict = {}
    for name, field in getFieldsInOrder(interface):
        if field.default is not None:
            class_dict[name] = field.default
    class_dict.update(values)

    if not isinstance(superclass, tuple):
        superclass = (superclass,)
    new_class = type(class_name, superclass, class_dict)
    classImplements(new_class, interface)
    return new_class


def make_identifier_safe(name):
    """Change a string so it can be used as a Python identifier.

    Changes all characters other than letters, numbers, and underscore
    into underscore. If the first character is not a letter or
    underscore, prepends an underscore.
    """
    if name is None:
        raise ValueError("Cannot make None value identifier-safe.")
    name = re.sub("[^A-Za-z0-9_]", "_", name)
    if len(name) == 0 or name[0] not in string.letters and name[0] != '_':
        name = '_' + name
    return name


def camelcase_to_underscore_separated(name):
    """Convert 'ACamelCaseString' to 'a_camel_case_string'"""
    def prepend_underscore(match):
        return '_' + match.group(1)
    return re.sub('\B([A-Z])', prepend_underscore, name).lower()


def safe_hasattr(ob, name):
    """hasattr() that doesn't hide exceptions."""
    return getattr(ob, name, missing) is not missing


def smartquote(str):
    """Return a copy of the string, with typographical quote marks applied."""
    str = unicode(str)
    str = re.compile(u'(^| )(")([^" ])').sub(u'\\1\u201c\\3', str)
    str = re.compile(u'([^ "])(")($|[\s.,;:!?])').sub(u'\\1\u201d\\3', str)
    return str


def safe_js_escape(text):
    """Return the given text escaped for use in Javascript code.

    This will also perform a cgi.escape() on the given text.
    """
    return encoder.encode_basestring(cgi.escape(text, True))


def get_current_browser_request():
    """Return the current browser request, looked up from the interaction.

    If there is no suitable request, then return None.

    Returns only requests that provide IHTTPApplicationRequest.
    """
    from zope.security.management import queryInteraction
    from zope.publisher.interfaces.http import IHTTPApplicationRequest
    interaction = queryInteraction()
    if interaction is None:
        return None
    requests = [
        participation
        for participation in interaction.participations
        if IHTTPApplicationRequest.providedBy(participation)
        ]
    if not requests:
        return None
    assert len(requests) == 1, (
        "We expect only one IHTTPApplicationRequest in the interaction."
        " Got %s." % len(requests))
    return requests[0]


def get_current_web_service_request():
    """Return the current web service request.

    This may be a new request object based on the browser request (if
    the client is a web browser that might make AJAX calls to a
    separate web service) or it may be the same as the browser request
    (if the client is a web service client accessing the service
    directly).

    :return: An object providing IWebserviceClientRequest.
    """
    request = get_current_browser_request()
    if request is None:
        return None
    return IWebServiceClientRequest(request)


def tag_request_with_version_name(request, version):
    """Tag a request with a version name and marker interface."""
    request.annotations[request.VERSION_ANNOTATION] = version
    # Find the version-specific marker interface this request should
    # provide, and provide it.
    to_provide = getUtility(IWebServiceVersion, name=version)
    alsoProvides(request, to_provide)
    request.version = version


def simple_popen2(command, input, env=None, in_bufsize=1024, out_bufsize=128):
    """Run a command, give it input on its standard input, and capture its
    standard output.

    Returns the data from standard output.

    This function is needed to avoid certain deadlock situations. For example,
    if you popen2() a command, write its standard input, then read its
    standard output, this can deadlock due to the parent process blocking on
    writing to the child, while the child process is simultaneously blocking
    on writing to its parent. This function avoids that problem by using
    subprocess.Popen.communicate().
    """

    p = subprocess.Popen(
            command, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
    (output, nothing) = p.communicate(input)
    return output
