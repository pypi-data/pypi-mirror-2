##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Grok
"""

from zope.interface import implements, implementsOnly, classProvides
from zope.component import adapts

from martian import ClassGrokker, InstanceGrokker, GlobalGrokker
from grokcore.component.components import Adapter, GlobalUtility, MultiAdapter, Context

from martian import baseclass
from grokcore.component.directive import (
    context, name, title, description, provides, global_utility, global_adapter, direct)
from grokcore.component.decorators import subscribe, adapter, implementer, provider
from martian.error import GrokError, GrokImportError

# Import this module so that it's available as soon as you import the
# 'grokcore.component' package.  Useful for tests and interpreter examples.
import grokcore.component.testing

# Only export public API
from grokcore.component.interfaces import IGrokcoreComponentAPI
__all__ = list(IGrokcoreComponentAPI)
