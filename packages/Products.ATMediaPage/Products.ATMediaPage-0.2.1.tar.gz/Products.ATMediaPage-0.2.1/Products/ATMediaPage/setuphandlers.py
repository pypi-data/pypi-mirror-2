from logging import getLogger
from plone.browserlayer import utils as layerutils

from Products.ATMediaPage.interfaces import IATMediaPageSpecific

logger = getLogger('Products.ATMediaPage')


def resetLayers(context):
    """Remove custom browserlayer on uninstall."""

    if context.readDataFile('Products.ATMediaPage_uninstall.txt') is None:
        return
    
    if IATMediaPageSpecific in layerutils.registered_layers():
        layerutils.unregister_layer(name='Products.ATMediaPage')
        logger.info('Browser layer "Products.ATMediaPage" uninstalled.')


