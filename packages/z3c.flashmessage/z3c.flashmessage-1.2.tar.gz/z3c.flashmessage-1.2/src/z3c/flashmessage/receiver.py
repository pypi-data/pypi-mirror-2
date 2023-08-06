# -*- coding: latin-1 -*-
# Copyright (c) 2007 Zope Foundation and Contributors
# See also LICENSE.txt
# $Id: receiver.py 113324 2010-06-10 09:48:02Z janwijbrand $
"""A global message receiver that covers all sources."""

import zope.interface

import z3c.flashmessage.interfaces


class GlobalMessageReceiver(object):

    zope.interface.implements(z3c.flashmessage.interfaces.IMessageReceiver)

    def receive(self, type=None):
        sources = zope.component.getAllUtilitiesRegisteredFor(
            z3c.flashmessage.interfaces.IMessageSource)
        for source in sources:
            # We need to create a list here, because message.prepare might
            # modify the original source list stop the iteration before
            # all items where consumed:
            for message in list(source.list(type)):
                message.prepare(source)
                yield message
