"""Definition of the MediaPage content type."""

# zope imports
from zope.interface import implements

# plone imports
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import (ATDocument,
    finalizeATCTSchema)

# local imports
from Products.ATMediaPage import ATMediaPageMessageFactory as _
from Products.ATMediaPage.config import PROJECTNAME
from Products.ATMediaPage.interfaces import IMediaPage


mediapageSchema = ATDocument.schema.copy() + atapi.Schema((

    atapi.BooleanField(
        'AutoChangeRandom',
        default = False,
        required = False,
        storage = atapi.AnnotationStorage(migrate=True),
        widget = atapi.BooleanWidget(
            description = _(
                u"descr_mediapage_autochangerandom",
                u"Should we show images randomized in AutoChange views?",
            ),
            label = _(
                u"label_mediapage_autochangerandom",
                u"Show images randomized",
            ),
        ),
    ),

    atapi.StringField(
        'AutoChangeDelay',
        default = '10000',
        required = False,
        storage = atapi.AnnotationStorage(migrate=True),
        widget = atapi.StringWidget(
            description = _(
                u"descr_mediapage_autochangedelay",
                u"Here you can set the delaytime for views with image " \
                 "autochange enabled.",
            ),
            label = _(
                u"label_mediapage_autochangedelay",
                u"Image autochange delay (in milliseconds)",
            ),
        ),
    ),

    atapi.BooleanField(
        'UseImageZoom',
        default = True,
        index = 'FieldIndex:schema',
        required = False,
        storage = atapi.AnnotationStorage(migrate=True),
        widget = atapi.BooleanWidget(
            description = _(
                u"descr_mediapage_useimagezoom",
                u"Check to use the image-zoom feature (Javscript).",
            ),
            label = _(
                u"label_mediapage_useimagezoom",
                u"Use image-zoom feature",
            ),
        ),
    ),
), marshall = atapi.RFC822Marshaller())

mediapageSchema['text'].required = True
mediapageSchema['text'].widget.allow_file_upload = True
mediapageSchema.changeSchemataForField('presentation', 'default')
mediapageSchema.changeSchemataForField('tableContents', 'default')

schemata.finalizeATCTSchema(
    mediapageSchema,
    moveDiscussion = False,
    folderish = True,
)


class MediaPage(atapi.OrderedBaseFolder, ATDocument):
    """MediaPage is a Page which can contain ATImage objects."""
    implements(IMediaPage)

    meta_type = 'MediaPage'
    portal_type = 'MediaPage'
    schema = mediapageSchema

    schema['relatedItems'].widget.visible['edit'] = 'visible'

    schema.changeSchemataForField('presentation', 'settings')
    schema.changeSchemataForField('tableContents', 'settings')
    schema.changeSchemataForField('AutoChangeRandom', 'settings')
    schema.changeSchemataForField('AutoChangeDelay', 'settings')
    schema.changeSchemataForField('UseImageZoom', 'settings')

    _at_rename_after_creation = True
    #__implements__ = atapi.OrderedBaseFolder.__implements__ + \
    #                 ATDocument.__implements__

    def canSetDefaultPage(self):
        return False

    # enable FTP/WebDAV and friends
    PUT = ATDocument.PUT

atapi.registerType(MediaPage, PROJECTNAME)
