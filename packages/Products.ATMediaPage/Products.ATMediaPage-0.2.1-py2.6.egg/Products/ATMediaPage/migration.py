# Migration utilities and migration steps
import transaction
from zope.component import getUtility
from plone.browserlayer import utils as layerutils

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from Products.ATMediaPage.interfaces import IATMediaPageSpecific
from Products.ATMediaPage.exportimport import configureKupu

import logging
logger  = logging.getLogger('ATMediaPage-migration')

EXTENSION_PROFILES = ('Products.ATMediaPage:default', )


def emptyMigrate(self):
    """For dummy upgrade steps."""
    pass


def migrateTo02(context):
    """Replace deprecated layouts by new default view."""
    portal_types = getToolByName(context, 'portal_types')
    portal_setup = getToolByName(context, 'portal_setup')

    mp = getattr(portal_types, 'MediaPage', None)
    if mp:
        # make sure we get the newest GS profile
        for extension_id in EXTENSION_PROFILES:
            portal_setup.runAllImportStepsFromProfile(
                'profile-%s' % extension_id, purge_old = False)
            transaction.savepoint()

        view_methods = mp.view_methods
        
        query = {}
        query['portal_type'] = 'MediaPage'
        pages = context.portal_catalog.searchResults(query)
        for page in pages:
            obj = page.getObject()
            layout = obj.getLayout()
            if not layout in view_methods:
                obj.setLayout(mp.default_view) 


def migrateTo021(context):
    """Add new custom browserlayer."""
    
    if not IATMediaPageSpecific in layerutils.registered_layers():
        layerutils.register_layer(IATMediaPageSpecific, name='Products.ATMediaPage')
        logger.info('Browser layer "Products.ATMediaPage" installed.')

    site = getUtility(IPloneSiteRoot)

    # skip kupu configuration on sites that don't have kupu installed
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        configureKupu(kupu)
        logger.info('Kupu configured for Products.ATMediaPage')
