#!/usr/bin/env python
# encoding: utf-8
"""
methods.py

Created by Manabu Terada on 2010-07-08.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from DateTime import DateTime
from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import config
from Products.CMFCore.permissions import View
# from Products.CMFCore.permissions import AccessInactivePortalContent

from Products.Archetypes.Referenceable import Referenceable
from Products.CMFPlone.CatalogTool import getObjPositionInParent


from logging import getLogger
logger = getLogger(__name__)
info = logger.info

def _check_view_permission(obj):
    return getSecurityManager().checkPermission(View, obj)

def _check_effective_range_permission(obj):
    now = DateTime()
    effectiveDate = obj.getEffectiveDate()
    expirationDate = obj.getExpirationDate()
    if effectiveDate and effectiveDate > now:
        return False
    elif expirationDate and expirationDate < now:
        return False
    else:
        return True


def getSecureRefs(self, relationship=None, targetObject=None):
    """get all the referenced objects for this object"""
    tool = getToolByName(self, config.REFERENCE_CATALOG)
    refs = tool.getReferences(self, relationship, targetObject=targetObject)
    if refs:
        lst = []
        for ref in refs:
            obj = ref.getTargetObject()
            if _check_view_permission(obj) and _check_effective_range_permission(obj):
                lst.append(obj)
        return lst
    return []

def getSecureBRefs(self, relationship=None, targetObject=None):
    """get all the back referenced objects for this object"""
    tool = getToolByName(self, config.REFERENCE_CATALOG)
    refs = tool.getBackReferences(self, relationship, targetObject=targetObject)
    if refs:
        lst = []
        for ref in refs:
            obj = ref.getSourceObject()
            if _check_view_permission(obj) and _check_effective_range_permission(obj):
                lst.append(obj)
        return lst
    return []


def _get_sorted_lst(lst, sort_key, order):
    if sort_key is None:
        sort_key = "Date"
    def _get_sorted_key(obj):
        try:
            o = getattr(obj, sort_key, lambda:None)()
            if o is None and sort_key == 'getObjPositionInParent':
                return getObjPositionInParent(obj)
            else:
                return o
        except TypeError:
            return None
    sorted_lst = sorted(lst, key=_get_sorted_key)
    if order == "reverse" or order == "descending":
        return list(reversed(sorted_lst))
    return sorted_lst

def getSortedSecureRefs(self, relationship=None, targetObject=None, sort_key=None, order='ascending'):
    """sorted get all the referenced objects for this object"""
    lst = self.getSecureRefs(relationship, targetObject)
    return _get_sorted_lst(lst, sort_key, order)

def getSortedSecureBRefs(self, relationship=None, targetObject=None, sort_key=None, order='ascending'):
    """sorted get all the back referenced objects for this object"""
    lst = self.getSecureBRefs(relationship, targetObject)
    return _get_sorted_lst(lst, sort_key, order)


Referenceable.getSecureRefs = getSecureRefs
info('adding method %s', str(Referenceable.getSecureRefs))
Referenceable.getSecureBRefs = getSecureBRefs
info('adding method %s', str(Referenceable.getSecureBRefs))
Referenceable.getSortedSecureRefs = getSortedSecureRefs
info('adding method %s', str(Referenceable.getSortedSecureRefs))
Referenceable.getSortedSecureBRefs = getSortedSecureBRefs
info('adding method %s', str(Referenceable.getSortedSecureBRefs))
