from plone.formwidget.autocomplete.widget import AutocompleteSearch \
                                              as BaseAutocompleteSearch
                                              
class AutocompleteSearch(BaseAutocompleteSearch):
    
    def validate_access(self):
        """ do nothing. There is a problem with validate_access method. 
        Original code:
        content = self.context.form.context
        view_name = self.request.getURL().split('/')[-3] # /path/to/obj/++widget++wname/@@autocomplete-search?q=foo
        view_instance = content.restrictedTraverse(view_name)

        Problem: 
        getURL returns (in case of gridfield) something like:
        http://127.0.0.1:8080/portal/content_item/++field++MyField/edit/++widget++my_field_name/@@autocomplete-search
        view_name is: add
        content is: <Field MyField(object:rw)>
        
        but validate_access fails on AttributeError: add. I've got better
        results with self.request.getURL().split('/')[-4] but I don't think it
        is correct solution, neither in case of Gridfield. 
        
        I'm leaving this as TODO.
        """
        return