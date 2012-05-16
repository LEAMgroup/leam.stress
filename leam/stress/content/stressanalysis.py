"""Definition of the Stress Analysis content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from leam.stress import stressMessageFactory as _

from leam.stress.interfaces import IStressAnalysis
from leam.stress.config import PROJECTNAME

StressAnalysisSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ReferenceField(
        'layer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceWidget(
            label=_(u"GIS Layer"),
            description=_(u"A GIS layer with the environmentally sensitive areas."),
        ),
        required=True,
        relationship='stressanalysis_layer',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'scenario',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceWidget(
            label=_(u"LUC Scenario"),
            description=_(u"An existing LUC Scenario with it's associated probability maps."),
        ),
        required=True,
        relationship='stressanalysis_scenario',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.ReferenceField(
        'section',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceWidget(
            label=_(u"Section Map"),
            description=_(u"Section layer used to split the sensative layer."),
        ),
        relationship='stressanalysis_section',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

StressAnalysisSchema['title'].storage = atapi.AnnotationStorage()
StressAnalysisSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(StressAnalysisSchema, moveDiscussion=False)


class StressAnalysis(base.ATCTContent):
    """Frontend to the LEAM Stress Analysis Model"""
    implements(IStressAnalysis)

    meta_type = "StressAnalysis"
    schema = StressAnalysisSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    layer = atapi.ATReferenceFieldProperty('layer')

    scenario = atapi.ATReferenceFieldProperty('scenario')

    section = atapi.ATReferenceFieldProperty('section')


atapi.registerType(StressAnalysis, PROJECTNAME)
