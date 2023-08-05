from collective.amberjack.core.interfaces import ITourDefinition,\
    IStepDefinition
from zope.interface import implements
from zope import schema

class Tour(object):
    implements(ITourDefinition)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'steps': 
                self._addSteps(v)
            else:
                setattr(self, k, v)
        self._validateFields()

    def _addSteps(self, steps):
        if not steps:
            raise AttributeError, 'Tour need to have steps.'
        self.steps = ()
        for step in steps:
            if not isinstance(step, dict):
                raise TypeError, 'Step should be a dictionary.'
            self.steps += (Step(**step),)
        
    def _validateFields(self):         
        for field in schema.getFields(ITourDefinition).values():
            bound = field.bind(self)
            bound.validate(bound.get(self))

class Step(dict):
    implements(IStepDefinition)
    
    validators = ()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setitem__(k, v)
            setattr(self, k, v)
        self._validateFields()
        
    def _validateFields(self):         
        for field in schema.getFields(IStepDefinition).values():
            bound = field.bind(self)
            bound.validate(bound.get(self))
            
    def validate(self, context, request):
        errors = []
        for validator in self.validators:
            message = validator(context, request)
            if message:
                errors.append(message)
        return errors
            
