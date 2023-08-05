from zope.component import getMultiAdapter

from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

from AccessControl import ClassSecurityInfo
from zope import schema

class GridWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "gridfield",
        'helper_js': ('gridfield.js',),
        'helper_css': ('gridfield.css',),
        'visible': {'view': 'visible', 'edit': 'invisible'},
        'show_fields': None,
        'exclude_fields': None,
        'table_class': 'listing',
        })

    security = ClassSecurityInfo()

    def canModify(self, instance):
        mtool = getMultiAdapter((instance, instance.REQUEST), name=u"plone_tools").membership()
        return mtool.checkPermission('Modify portal content', instance)
        
    def fields(self, instance, field):
        row_interface = field.row_interface
        fields = schema.getFieldsInOrder(row_interface)
        if self.show_fields:
            results = [{'id': x[0], 'title': x[1].title} for x in fields if x[0] in self.show_fields]
        elif self.exclude_fields:
            results = [{'id': x[0], 'title': x[1].title} for x in fields if x[0] not in self.exclude_fields]
        else:
            results = [{'id': x[0], 'title': x[1].title} for x in fields]
        return results
    
    def render_row(self, instance, field, row):
        instance.REQUEST.set('row', row)
        view = getMultiAdapter((field, field.REQUEST), name=u"display")
        view.update()
        return view.contents
        
registerWidget(GridWidget,
               title='Grid field Widget',
               description=('Displays table.'),
               used_for=('archetypes.gridfield.field.GridField',)
               )
