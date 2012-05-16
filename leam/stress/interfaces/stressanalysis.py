from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from leam.stress import stressMessageFactory as _



class IStressAnalysis(Interface):
    """Frontend to the LEAM Stress Analysis Model"""

    # -*- schema definition goes here -*-
    layer = schema.Object(
        title=_(u"GIS Layer"),
        required=True,
        description=_(u"A GIS layer with the environmentally sensitive areas."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    scenario = schema.Object(
        title=_(u"LUC Scenario"),
        required=True,
        description=_(u"An existing LUC Scenario with it's associated probability maps."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    section = schema.Object(
        title=_(u"Section Map"),
        required=False,
        description=_(u"Section layer used to split the sensative layer."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
