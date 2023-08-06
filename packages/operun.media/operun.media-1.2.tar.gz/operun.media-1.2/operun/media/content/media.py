from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo

from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

from Products.Archetypes.atapi import DisplayList

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.validation import V_REQUIRED

from operun.media.interfaces import IMedia
from operun.media.config import PROJECTNAME

from operun.media import MediaMessageFactory as _

SELECTION = DisplayList((
    ('internal', 'Hochgeladene Datei'),
    ('external', 'Verlinkte Datei'),
    ))


schema = Schema((

    BooleanField('showimage',
        storage = AnnotationStorage(),
        widget = BooleanWidget(label=_(u"Show Image"),
                            description=_(u"Display the Image beside the Body Text."),
                            ),
        ),     

    StringField('link',
        searchable = False,
        required = False,
        languageIndependent = True,
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u"Link"),
                              description = _(u"Please enter the URL to a file or YouTube video."),
                              ),     
        ),
        

    FileField('file',
        searchable = False,
        required = False,
        languageIndependent = True,
        storage = AnnotationStorage(),
        validators = (('isNonEmptyFile', V_REQUIRED), ('isFileType', V_REQUIRED), ('checkFileMaxSize', V_REQUIRED),),
        widget = FileWidget(label = _(u"File"),
                            description = _(u"Upload a audio or video file."),
                            ),
        ),
        

    IntegerField('width',
        searchable = False,
        required = True,
        storage = AnnotationStorage(),
        default = 320,
        widget = IntegerWidget(label=_(u"Player width"),
                            description=_(u"Enter the player width."),
                            ),     
        ),

    IntegerField('height',
        searchable = False,
        required = True,
        storage = AnnotationStorage(),
        default = 240,
        widget = IntegerWidget(label=_(u"Player height"),
                            description=_(u"Enter the player height."),
                            ),     
        ),

    BooleanField('downloadlink',
        storage = AnnotationStorage(),
        widget = BooleanWidget(label=_(u"Show download link"),
                            description=_(u"Display a link to download the file below the player."),
                            ),
        ),     

    BooleanField('audiomode',
        storage = AnnotationStorage(),
        widget = BooleanWidget(label=_(u"Audio mode"),
                            description=_(u"Check to display the palyer controls only."),
                            ),
        ),     
        
    StringField('selection',
        searchable = False,
        storage = AnnotationStorage(),
        vocabulary = SELECTION,
        widget = SelectionWidget(label=_(u"Select source"),
                            description=_(u"Please select what to display."),
                            ),     
        ),
        
    ),
)

MediaSchema = ATNewsItemSchema.copy() + schema.copy()

MediaSchema['title'].storage = AnnotationStorage()
MediaSchema['description'].storage = AnnotationStorage()
MediaSchema['text'].storage = AnnotationStorage()
MediaSchema['image'].widget.description = _(u'label_image_field', default = u'Will be shown in the folder listing, and as screenshot. Image will be scaled to a sensible size.')
MediaSchema['image'].schemata = 'Media'
MediaSchema['imageCaption'].schemata = 'Media'
MediaSchema['showimage'].schemata = 'Media'
MediaSchema['downloadlink'].schemata = 'Media'
MediaSchema['audiomode'].schemata = 'Media'
MediaSchema['link'].schemata = 'Media'
MediaSchema['file'].schemata = 'Media'
MediaSchema['width'].schemata = 'Media'
MediaSchema['height'].schemata = 'Media'
MediaSchema['selection'].schemata = 'Media'

finalizeATCTSchema(MediaSchema, folderish=False, moveDiscussion=False)

class Media(ATNewsItem):
    """Media
    """

    implements(IMedia)

    portal_type = "Media"
    _at_rename_after_creation = True

    schema = MediaSchema
    schema.moveField('showimage', before = 'link')
    
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    text = ATFieldProperty('text')
    
    showimage = ATFieldProperty('showimage')
    link = ATFieldProperty('link')
    file = ATFieldProperty('file')
    
    width = ATFieldProperty('width')
    height = ATFieldProperty('height')
    
    downloadlink = ATFieldProperty('downloadlink')
    audiomode = ATFieldProperty('audiomode')
    
    security = ClassSecurityInfo()
        
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)
    
    def __bobo_traverse__(self, REQUEST, name):

        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image

        if name.startswith('splash'):
            field = self.getField('image')
            image = None
            scalename = 'large'
            image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        
        if name.startswith(self.getFileName()) and self.isFile():
            field = self.getField('file')
            return field.download(self)
            
        return super(Media, self).__bobo_traverse__(REQUEST, name)


    def getFileName(self):
        """Returns the file name needed by flowplayer"""
        
        field = self.getField('file')
        filename = field.getFilename(self)
        return filename


    security.declareProtected(View, 'download')
    def download(self, REQUEST=None, RESPONSE=None):
        """Download the file
        """
    
        if self.isFile():
            field = self.getField('file')
            return field.download(self)
        return None
    

    def isFile(self):
        """Check if there is a File"""

        size = self.getField('file').get_size(self)
        if size: return True
        return None
        
registerType(Media, PROJECTNAME)