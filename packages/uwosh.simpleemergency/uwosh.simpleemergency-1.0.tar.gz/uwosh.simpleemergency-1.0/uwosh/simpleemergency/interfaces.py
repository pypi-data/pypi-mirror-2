from zope.interface import Interface, Attribute
import zope.deferredimport
import zope.component.interfaces

class IUWOshSimpleEmergencyLayer(Interface):
    """
    Marker interface that defines a browser layer
    """
    
class ISimpleEmergencyModifiedEvent(zope.component.interfaces.IObjectEvent):
    """An object has been modified"""