from collective.amberjack.core.interfaces import IMicroStepsManager
from plone.registry import Registry
from zope.interface import implements 

registry = Registry()

class MicroStepsManager(object):
    implements(IMicroStepsManager)
        
    def getSteps(self, context=None):
        for microstep in registry.records['collective.amberjack.core.microsteps'].value:
            yield microstep
