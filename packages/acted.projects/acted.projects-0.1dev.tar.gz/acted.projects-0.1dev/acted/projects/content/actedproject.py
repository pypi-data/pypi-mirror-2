"""Definition of the ACTED Project content type
"""


from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from acted.projects import projectsMessageFactory as _
from acted.projects.interfaces import IACTEDProject
from acted.projects.config import PROJECTNAME
#from archetypes.multifile.MultiFileField import MultiFileField
#from archetypes.multifile.MultiFileWidget import MultiFileWidget
#from iw.fss.FileSystemStorage import FileSystemStorage
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime.DateTime import *
from Products.Archetypes.public import FloatField, DecimalWidget
from acted.projects.config import ACTED_COUNTRIES
from acted.projects.config import ACTED_SECTORS
from acted.projects.config import ACTED_DONORS



ACTEDProjectSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        name='description',
        widget=atapi.TextAreaWidget(
        label=_(u'Project Description')
      ),
      required=False,
      searchable=True
    ),


    atapi.StringField(
        name='projectCode',
        widget=atapi.StringWidget(
        label=_(u'Project Code'),
        maxlength=20,
        size=20
      ),
      required=True,
      searchable=True
    ),

    atapi.StringField(
        name='projectDonor',
        widget=atapi.SelectionWidget(
        label=_(u'Donor'),
        format='select'
      ),
      vocabulary=ACTED_DONORS,
      enforceVocabulary=True,
      required=True,
      searchable=True
    ),



    atapi.StringField(
        name='projectCountry',
        widget=atapi.SelectionWidget(
        label=_(u'Country'),
        format='select'
      ),
      vocabulary=ACTED_COUNTRIES,
      enforceVocabulary=True,
      required=True,
      searchable=True
    ),

    atapi.StringField(
        name='projectSectors',
        widget=atapi.MultiSelectionWidget(
        label=_(u'Sectors'),
        format='select'
      ),
      vocabulary=ACTED_SECTORS,
      required=False,
      searchable=True
    ),

    atapi.IntegerField(
        name='projectYear',
        widget=atapi.SelectionWidget(
        label=_(u'Year of Contract Signature'),
        format='select'
      ),
      vocabulary=['2000','2001','2002'],
      enforceVocabulary=True,
      required=True,
      searchable=False
    ),

    atapi.FloatField(
        name='projectBudget',
        widget=DecimalWidget(
            label=_(u'Budget (Euros)'),
      ),
      required=False,
      searchable=False
    ),

    atapi.ReferenceField(
        name='projectReferences',
        widget=ReferenceBrowserWidget(
            label=_(u'Reference Files'),
      ),
      required=False,
      searchable=False,
      multiValued=True,
      allow_sorting=True,
      relationship='WorksWith',
      allowed_types=('Document','File','Image','Folder')
    )



))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ACTEDProjectSchema['title'].storage = atapi.AnnotationStorage()
ACTEDProjectSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ACTEDProjectSchema, moveDiscussion=False)

class ACTEDProject(base.ATCTContent):
    """Details about a particular ACTED Project"""
    implements(IACTEDProject)

    meta_type = "ACTED Project"
    schema = ACTEDProjectSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-


atapi.registerType(ACTEDProject, PROJECTNAME)
