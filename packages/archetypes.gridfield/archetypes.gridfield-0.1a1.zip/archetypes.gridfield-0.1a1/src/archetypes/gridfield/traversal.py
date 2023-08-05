from zope.interface import implements
from zope.component import adapts

from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IBrowserRequest

from plone.z3cform.interfaces import IFormWrapper
from plone.z3cform import z2
from Products.Archetypes.interfaces import IBaseObject

class FieldTraversal(object):
    """Allow traversal to widgets via the ++field++ namespace. The context
    is the from layout wrapper.
    
    Note that fields may need to mixing in Acquisition.Explicit for this to
    work.
    """
    
    implements(ITraversable)
    adapts(IBaseObject, IBrowserRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        return self.context.getField(name)
