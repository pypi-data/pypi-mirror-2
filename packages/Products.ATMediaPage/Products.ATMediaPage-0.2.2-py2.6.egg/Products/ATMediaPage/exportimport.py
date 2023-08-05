from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
from Products.CMFPlone.interfaces import IPropertiesTool

TYPES_TO_VERSION = ('MediaPage', )


def configureKupu(kupu):

    def addKupuResource(resourceType, portalType):
        resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
        if portalType not in resourceList:
            resourceList.append(portalType)
            kupu.addResourceType(resourceType,tuple(resourceList))
        
    addKupuResource('linkable', 'MediaPage')
    addKupuResource('containsanchors', 'MediaPage')        
    addKupuResource('collection', 'MediaPage')


def setVersionedTypes(context):
    portal_repository = getToolByName(context, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            # use append() to make sure we don't overwrite any
            # content-types which may already be under version control
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)


def import_various(context):
    if not context.readDataFile('Products.ATMediaPage.txt'):
        return

    site = context.getSite()

    # skip kupu configuration on sites that don't have kupu installed
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        configureKupu(kupu)

    # enable versioning
    setVersionedTypes(site)
