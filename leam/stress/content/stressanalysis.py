"""Definition of the Stress Analysis content type
"""

from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import fromstring, tostring

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.stress import stressMessageFactory as _

from leam.stress.interfaces import IStressAnalysis
from leam.luc.interfaces import IModel
from leam.stress.config import PROJECTNAME

StressAnalysisSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ReferenceField(
        'layer',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"GIS Layer"),
            description=_(u"A GIS layer with the environmentally sensitive areas."),
            startup_directory='/luc/impacts/stress-analysis/es-zones',
        ),
        required=True,
        relationship='stressanalysis_layer',
        allowed_types=('SimMap',),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'scenario',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"LUC Scenario"),
            description=_(u"An existing LUC Scenario with it's associated probability maps."),
            startup_directory='/luc/scenarios',
        ),
        required=True,
        relationship='stressanalysis_scenario',
        allowed_types=('LUC Scenario'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'section',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Section Map"),
            description=_(u"Section layer used to split the sensative layer."),
            startup_directory='/luc/drivers',
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        relationship='stressanalysis_section',
        allowed_types=('SimMap',), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.StringField(
        'runstatus',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Run Status"),
            description=_(u"Provide the current run state of the scenario."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
        default="queued",
    ),


    atapi.DateTimeField(
        'start_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Time"),
            description=_(u"When the model began execution."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),


    atapi.DateTimeField(
        'end_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"End Time"),
            description=_(u"When the model completed."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

StressAnalysisSchema['title'].storage = atapi.AnnotationStorage()
StressAnalysisSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(StressAnalysisSchema, moveDiscussion=False)


class StressAnalysis(base.ATCTContent):
    """Frontend to the LEAM Stress Analysis Model"""
    implements(IStressAnalysis,IModel)

    meta_type = "StressAnalysis"
    schema = StressAnalysisSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    layer = atapi.ATReferenceFieldProperty('layer')

    scenario = atapi.ATReferenceFieldProperty('scenario')

    section = atapi.ATReferenceFieldProperty('section')

    runstatus = atapi.ATFieldProperty('runstatus')

    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')



    def checkDependencies(self):
        """Checks that all necessary impacts are ready for use."""
        pass

    security.declarePublic('requeue')
    def requeue(self):
        """simple method to requeue the scenario"""
        self.runstatus = 'queued'
        self.reindexObject(['runstatus',])
        return "requeue"

    security.declarePublic('getConfig')
    def getConfig(self):
        """Generates a configuration file for this analysis."""
       
        model = Element('model')
        tree = SubElement(model, 'scenario')
        SubElement(tree, 'id').text = self.id
        SubElement(tree, 'title').text = self.title
        SubElement(tree, 'repository').text = \
            'http://datacenter.leamgroup.com/svn/desktop/ccrpc_sa/trunk'
        SubElement(tree, 'cmdline').text = \
            'python startup -c config.xml'

        for p in self.getLayer():
            reg = SubElement(tree, 'zonemap')
            SubElement(reg, 'title').text = p.title
            SubElement(reg, 'layer').text = p.absolute_url() + \
                    '/at_download/simImage'
        SubElement(tree, 'scenario').text = self.getScenario().absolute_url()
        SubElement(tree, 'section').text = ''

        self.REQUEST.RESPONSE.setHeader('Content-Type', 
                'application/xml; charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition',
                'attachment; filename="%s.xml"' % self.id)
        return tostring(model, encoding='UTF-8')


atapi.registerType(StressAnalysis, PROJECTNAME)
