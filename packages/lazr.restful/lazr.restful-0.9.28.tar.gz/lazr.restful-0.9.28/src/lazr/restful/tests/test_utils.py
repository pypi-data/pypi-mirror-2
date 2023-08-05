# Copyright 2010 Canonical Ltd.  All rights reserved.

"""Test for lazr.restful.utils."""

__metaclass__ = type

import unittest

from zope.publisher.browser import TestRequest
from zope.security.management import (
    endInteraction, newInteraction, queryInteraction)

from lazr.restful.utils import get_current_browser_request


class TestUtils(unittest.TestCase):

    def test_get_current_browser_request_no_interaction(self):
        # When there's no interaction setup, get_current_browser_request()
        # returns None.
        self.assertEquals(None, queryInteraction())
        self.assertEquals(None, get_current_browser_request())

    def test_get_current_browser_request(self):
        # When there is an interaction, it returns the interaction's request.
        request = TestRequest()
        newInteraction(request)
        self.assertEquals(request, get_current_browser_request())
        endInteraction()

    # For the sake of convenience, test_get_current_web_service_request()
    # and tag_request_with_version_name() are tested in test_webservice.py.

