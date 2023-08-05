from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
import Acquisition
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Registry import registerField

from AccessControl import ClassSecurityInfo

from archetypes.gridfield.forms import AddForm, EditForm
from archetypes.gridfield.interfaces import IGridField
from archetypes.gridfield.widget import GridWidget

class GridField(ObjectField, Acquisition.Implicit):
    """Stores multiple files."""
    implements(IGridField)
    template = ViewPageTemplateFile('gridfield_render.pt')
    
    _properties = ObjectField._properties.copy()
    _properties.update({
        'widget': GridWidget,
        'row_interface': None,
        'add_form': AddForm,
        'edit_form': EditForm,
        })

    security  = ClassSecurityInfo()        

    def _newid(self, instance, data = None):
        if data is None:
            data = self.getRaw(instance)
        
        return data['currid'] + 1
        
    def _maxid(self, instance):
        """ TODO - can we store the max id somewhere ?"""
        data = self.getRaw(instance)['data']
            
        maxid = 0
        for item in data:
            if maxid < item['_id']:
                maxid = item['_id']
        return maxid

    def update_currid(self, instance, new_id = None, data = None, ):
        if new_id is None:
            new_id = self._maxid(instance)
        if data is None:
            data = self.getRaw(instance)
            
        data['currid'] = new_id
        
    security.declarePrivate('add')
    def add_row(self, instance, value, **kwargs):
        alldata = self.getRaw(instance)
        data = alldata['data']

        new_id = self._newid(instance, data = alldata)
        self.update_currid(instance, new_id = new_id, data = alldata)

        value['_id'] = new_id
        data.append(value)
        self.set(instance, alldata)

    security.declarePrivate('set_row')
    def set_row(self, instance, value):
        data = self.getRaw(instance)['data']
        row = self.get_row(instance, value['_id'])

        idx = data.index(row)
        data[idx] = value
    
    security.declarePrivate('get_row')
    def get_row(self, instance, row_id):
        data = self.getRaw(instance)['data']
        if not isinstance(row_id, int):
            row_id = int(row_id)
        row = None
        for item in data:
            if item['_id'] == row_id:
                row = item
                break
                
        if not row:
            raise LookupError, "The row id has not been found"
            
        return row
        
    security.declarePrivate('del_row')
    def del_row(self, instance, row_id):
        data = self.getRaw(instance)['data']
        row = self.get_row(instance, row_id)
        data.remove(row)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        return self.getRaw(instance, **kwargs)['data']
        
    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        data = super( GridField, self).get(instance, **kwargs)
        if not data:
            return {'data':[], 'currid': 0}
        return data

    security.declareProtected('View', 'ajax_render')
    def ajax_render(self):
        """ Render field from ajax request """
        instance = Acquisition.aq_parent(self)
        self.template.context = self
        return self.template(accessor=self.getAccessor(instance))
        
registerField(GridField,
              title='Grid Field',
              description=('Used for storing grid like data. '))

