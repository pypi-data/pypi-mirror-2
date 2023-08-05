"""
ZCML registrations.
"""
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.interfaces import IMicroStepsManager
from collective.amberjack.core.tour import Tour
from collective.amberjack.core.micro_steps_manager import registry
from plone.registry import Record
from plone.registry import field
from zope import interface
from zope.component import provideUtility
from zope.component import getUtility
from zope.configuration.fields import GlobalObject



class ITourDirective(interface.Interface):
    """Create tour registration."""
    tourdescriptor = GlobalObject(
        title=u'Tour descriptor',
        description=u'The variable that describes the tour',
        required=True)


def tour(_context, tourdescriptor, **kwargs):
    """Tour class factory registration."""
    tour = Tour(**tourdescriptor)
    provideUtility(component=tour, 
                   provides=ITourDefinition,
                   name=tour.tourId)

class IStepDirective(interface.Interface):
    """Create a ajStep registration"""
    stepsdescriptor = GlobalObject(
        title=u'Steps set',
        description=u'The variable that identifies a set of steps',
        required=True)
    
def ajstep(_context, stepsdescriptor):
    if not 'collective.amberjack.core.microsteps' in registry:
        microsteps = field.Tuple(title=u'microstep')
        record_microstep = Record(microsteps)
        record_microstep.value = stepsdescriptor
        registry.records['collective.amberjack.core.microsteps'] = record_microstep
    else:
        registry.records['collective.amberjack.core.microsteps'].value += stepsdescriptor
