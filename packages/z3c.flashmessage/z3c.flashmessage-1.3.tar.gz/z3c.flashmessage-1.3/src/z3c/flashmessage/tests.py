# -*- coding: latin-1 -*-
# Copyright (c) 2007 Zope Foundation and Contributors
# See also LICENSE.txt
# $Id: tests.py 117188 2010-10-02 13:20:32Z icemac $
"""Test harness"""

import doctest
import z3c.flashmessage
import zope.app.wsgi.testlayer
import zope.publisher.browser
import zope.security.management


FlashMessageLayer = zope.app.wsgi.testlayer.BrowserLayer(z3c.flashmessage)


def setUp(test):
    request = zope.publisher.browser.TestRequest()
    zope.security.management.newInteraction()
    interaction = zope.security.management.getInteraction()
    interaction.add(request)


def test_suite():
    suite = doctest.DocFileSuite(
        'README.txt',
        optionflags=doctest.ELLIPSIS,
        setUp=setUp)
    suite.layer = FlashMessageLayer
    return suite
