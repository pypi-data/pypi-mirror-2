from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from Products.ATContentTypes.interface import IATDocument

from archetypes.gridfield import GridField, GridWidget
from zope.interface import Interface
from zope import schema

class ExtGridField(ExtensionField, GridField):
    pass

# from archetypes.gridfield.forms import AddForm as GFAddForm
# from archetypes.gridfield.forms import EditForm as GFEditForm
# class CustomAddForm(GFAddForm):
# 
#     def __init__(self, context, request):
#         super(CustomAddForm, self).__init__(context, request)
#         self.fields['description'].widgetFactory = CustomWidget
#
# # class CustomEditForm(GFEditForm):
# 
#     def __init__(self, context, request):
#         super(CustomEditForm, self).__init__(context, request)
#         self.fields['description'].widgetFactory = CustomWidget

class IExampleGridInterface(Interface):

    portal_type  = schema.Choice(title=u'Portal type',
                              required = False,
                              vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes')

    description  = schema.TextLine(title=u'Some description',
                                   required = True)

    value  = schema.Int(title=u'Integer value',
                               required = False)
                                   
    
                                        


class GridFieldExtender(object):
    adapts(IATDocument)
    implements(ISchemaExtender)
    
    def __init__(self, context):
        self.context = context

    fields = [
        ExtGridField('example_gridfield',
                  row_interface = IExampleGridInterface,
                  # add_form = CustomAddForm,
                  # edit_form = CustomEditForm,
                  widget = GridWidget(label=u'Example Grid Field'),
                 )
    ]

    def getFields(self):
        return self.fields
