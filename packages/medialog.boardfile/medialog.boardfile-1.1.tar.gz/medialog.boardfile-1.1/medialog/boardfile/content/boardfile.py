"""Definition of the Boardfile content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
 
from medialog.boardfile import boardfileMessageFactory as _
from medialog.boardfile.interfaces import IBoardfile
from medialog.boardfile.config import PROJECTNAME

from Products.validation.validators.RangeValidator import RangeValidator

from Products.validation import validation
validYear = RangeValidator("validYear", 2010, 2050)
validation.register(validYear)
 
BoardfileSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-


    atapi.StringField(
        'wp',
        searchable = True,
		required = True,
		default = "",
		vocabulary = [('Please Choose', 'Not set'), ('WP1', 'WP1'), ('WP2', 'WP2'), ('WP3', 'WP3'), ('WP4', 'WP4'), ('WP5', 'WP5'), ('WP6', 'WP6')],
		type = """lines""",
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u"Select WP"),            
            description=_(u"The Work Package of the publication."),          
        ),
        validators=("isUnixLikeName"),
    ),
  
  
    atapi.IntegerField(
        'publishingyear',
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(
            label=_(u"Year"),
            description=_(u"Year Published"),
        ),
        validators=("isInt", "validYear"),
        required= True,
    ),

    atapi.FileField(
        'file',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"File"),
            description=_(u"Optional File to upload"),
        ),
        required=False,
    ),

    
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BoardfileSchema['title'].storage = atapi.AnnotationStorage()
BoardfileSchema['title'].widget.label = 'Journal'
BoardfileSchema['title'].required = True
BoardfileSchema['description'].storage = atapi.AnnotationStorage()
BoardfileSchema['description'].widget.label = 'Abstract'
BoardfileSchema['description'].required = True

schemata.finalizeATCTSchema(BoardfileSchema, moveDiscussion=False)

class Boardfile(base.ATCTContent):
    """Boardfile content type"""
    implements(IBoardfile)

    meta_type = "boardfile"
    schema = BoardfileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    wp = atapi.ATFieldProperty('wp')

    publishingyear = atapi.ATFieldProperty('publishingyear')

    file = atapi.ATFieldProperty('file')
    
atapi.registerType(Boardfile, PROJECTNAME)
