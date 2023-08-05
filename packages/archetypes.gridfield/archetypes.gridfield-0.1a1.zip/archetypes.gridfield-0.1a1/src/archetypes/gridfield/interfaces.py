from zope.interface import Interface
from zope import schema

class IGridField(Interface):
    """ Grid field interface """
    
class IRowId(Interface):
    
    _id = schema.Int(title=u"Row id")