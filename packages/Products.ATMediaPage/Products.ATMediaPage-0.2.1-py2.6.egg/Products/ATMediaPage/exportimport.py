from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPropertiesTool

def configureKupu(kupu):

    def addKupuResource(resourceType, portalType):
        resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
        if portalType not in resourceList:
            resourceList.append(portalType)
            kupu.addResourceType(resourceType,tuple(resourceList))
        
    addKupuResource('linkable', 'MediaPage')
    addKupuResource('containsanchors', 'MediaPage')        
    addKupuResource('collection', 'MediaPage')


def import_various(context):
    if not context.readDataFile('Products.ATMediaPage.txt'):
        return

    site = context.getSite()

    # skip kupu configuration on sites that don't have kupu installed
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        configureKupu(kupu)
