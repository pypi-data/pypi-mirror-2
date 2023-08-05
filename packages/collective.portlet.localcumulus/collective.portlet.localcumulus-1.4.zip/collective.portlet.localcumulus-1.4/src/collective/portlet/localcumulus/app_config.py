#-*- coding: utf-8 -*-
"""Specific project configuration."""
GLOBALS = globals()




################################################################################
# Products that have entries in quickinstaller, here are their 'id' (not the translated name)
################################################################################

PRODUCT_DEPENDENCIES = (\
    'quintagroup.portlet.cumulus',
)

EXTENSION_PROFILES = ('collective.portlet.localcumulus:default',)

SKIN = 'collective.portlet.skin'

from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles

class HiddenProducts(object):
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return [ u'plone.app.openid', u'NuPlone', ]

class HiddenProfiles(object):
    implements(INonInstallableProfiles)

    def getNonInstallableProfiles(self):
        return [ u'plone.app.openid', u'NuPlone', ]
