from z3c.form import form,field,button
from z3c.form.interfaces import INPUT_MODE, HIDDEN_MODE

from plone.app.z3cform.layout import wrap_form, FormWrapper

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from zope.interface import Interface
from zope import schema
from Products.Five import BrowserView
import Acquisition
from archetypes.gridfield.interfaces import IRowId

class AcquisitionDict(dict, Acquisition.Implicit):
    pass

class AddForm(form.AddForm):

    label = "Add row"

    def __init__(self, context, request):
        row_interface = context.row_interface
        self.fields = field.Fields(row_interface)
        return super(AddForm, self).__init__(context, request)

    def createAndAdd(self, data):
        obj = self.context.aq_parent
        self.context.add_row(obj, data)
        obj.processForm()
        
        return data # to make addform happy

    def nextURL(self):
        return "%s/dummy" % self.context.absolute_url()

class AddFormWrapper(FormWrapper):
    
    def __init__(self, context, request):
        self.form = context.add_form
        self.context = context
        self.request = request
        super(AddFormWrapper, self).__init__(context, request)
        self.request.set("disable_border", True)

class EditForm(form.Form):
    _finishedUpdate = False
    label = "Edit row"
    
    def __init__(self, context, request):
        row_interface = context.row_interface
        
        self.fields = field.Fields(row_interface, IRowId)
        super(EditForm, self).__init__(context, request)
    
    def updateWidgets(self):
         super(EditForm, self).updateWidgets()
         self.widgets['_id'].mode = HIDDEN_MODE
         
    def getContent(self):
        obj = self.context.aq_parent
        result = {}
        row_id = self.request.get('row_id')
        if row_id:
            row = self.context.get_row(obj,row_id)
            if row:
                result = row
            
        return AcquisitionDict(result).__of__(self.context)

    @button.buttonAndHandler(u'Update')
    def handleUpdate(self, action):
        data, errors = self.extractData()
        if errors:
            self.errors = errors
            self.status = self.formErrorsMessage
            return

        if data:
            obj = self.context.aq_parent
            self.context.set_row(obj, data)
            obj.processForm()
            self._finishedUpdate = True
        return

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        self._finishedUpdate = True
        return
    
    def nextURL(self):
        return "%s/dummy" % self.context.aq_parent.absolute_url()
        
    def render(self):
        if self._finishedUpdate:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(EditForm, self).render()



class EditFormWrapper(FormWrapper):

    def __init__(self, context, request):
        self.form = context.edit_form
        self.context = context
        self.request = request
        super(EditFormWrapper, self).__init__(context, request)
        self.request.set("disable_border", True)


class DisplayForm(form.DisplayForm):
    template = ViewPageTemplateFile('display_form.pt')
    
    def __init__(self, context, request, data):
        self.data = data
        row_interface = context.row_interface
        self.fields = field.Fields(row_interface)
        return super(DisplayForm, self).__init__(context, request)
    
    def getContent(self):
        data = AcquisitionDict(self.data)
        return data.__of__(self.context)
        
    def __call__(self):
        self.update()
        return self.render()
        
class DisplayFormWrapper(FormWrapper):

    def __init__(self, context, request):
        self.form = DisplayForm
        self.context = context
        self.request = request
        row = self.request.get('row')
        if self.form is not None:
            self.form_instance = self.form(self.context.aq_inner, self.request, row)
            self.form_instance.__name__ = self.__name__

        self.request.set("disable_border", True)

class DeleteRow(BrowserView):
    
    def __call__(self):
        row_id = self.request.get('row_id')
        obj = self.context.aq_inner.aq_parent
        if row_id:
            self.context.del_row(obj, row_id)
            obj.processForm()
            
        self.request.response.redirect(obj.absolute_url())

class DummyView(BrowserView):

    def __call__(self):
        return ""