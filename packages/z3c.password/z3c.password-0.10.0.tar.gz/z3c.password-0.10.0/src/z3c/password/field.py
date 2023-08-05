##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Password Field Implementation

$Id: field.py 101210 2009-06-22 08:25:20Z adamg $
"""
__docformat__ = "reStructuredText"
import zope.component
import zope.schema
from z3c.password import interfaces

class Password(zope.schema.Password):

    def __init__(self, checker=None, **kw):
        self._checker = checker
        super(Password, self).__init__(**kw)

    @property
    def checker(self):
        if self._checker is None:
            return None
        if not isinstance(self._checker, basestring):
            return self._checker
        return zope.component.getUtility(
            interfaces.IPasswordUtility, self._checker)

    def validate(self, value):
        super(Password, self).validate(value)
        old = None
        if self.context is not None:
            try:
                old = self.get(self.context)
            except AttributeError:
                pass
        checker = self.checker
        if checker is not None:
            self.checker.verify(value, old)

        #try to check for disallowPasswordReuse here too, to raise
        #problems ASAP
        if self.context is not None:
            try:
                self.context._checkDisallowedPreviousPassword(value)
            except AttributeError:
                #if _checkDisallowedPreviousPassword is missing
                pass
