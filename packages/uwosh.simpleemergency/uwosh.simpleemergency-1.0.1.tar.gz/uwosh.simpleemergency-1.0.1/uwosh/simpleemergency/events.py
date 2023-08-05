from interfaces import ISimpleEmergencyModifiedEvent
import zope.component.interfaces
from zope.interface import implements

class SimpleEmergencyModifiedEvent(zope.component.interfaces.ObjectEvent):
    """An object has been modified"""

    # for repr backward compatibility. In the next release cycle, we'll
    # provide a testing framework that addresses repr migration.
    __module__ = 'zope.app.event.objectevent'

    implements(ISimpleEmergencyModifiedEvent)

    def __init__(self, context, request) :
        super(SimpleEmergencyModifiedEvent, self).__init__(context)
        self.context = context
        self.request = request