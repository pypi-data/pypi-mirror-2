Introduction
============

archetypes.gridfield adds support for data grids which are not inline editable.
Rows are addable/editable using overlay window.

Please note, current version requires branch of plone.app.jquerytools which is
included in the example buildout.

Additionally, gridfield widget is displayed on the base_view form only (field
is not visible on the object edit form!!). This is not a bug but a feature.

Usage
=====

Install as usuall. After that you can add additional field to you content type::

    from archetypes.gridfield import GridField
    ...

    GridField('field_name',
        row_interface = IProjectRow
    )
    
    ...

IProjectRow is a zope Interface which defines the data for one row. 
The addform and editform are generated from this one::

    class IProjectRow(Interface):
        title   = schema.TextLine(title=u'Project name', required=True)
        kind    = schema.Choice(title=u'Project type',
                                vocabulary="project.projectTypesVocabulary")
        start_date = schema.Date(title=u'Start date', required=True)
        end_date   = schema.Date(title=u'End date', required=False)
    
You may define custom add/edit forms and update widgets::

    from archetypes.gridfield.forms import AddForm, EditForm
    from collective.z3cform.datetimewidget import DateFieldWidget
    
    class ProjectAddForm(AddForm):
        def __init__(self, context, request):
            super(ProjectAddForm, self).__init__(context, request)
            self.fields['start_date'].widgetFactory = DateFieldWidget
            self.fields['end_date'].widgetFactory = DateFieldWidget

    class ProjectEditForm(EditForm):
        def __init__(self, context, request):
            super(ProjectEditForm, self).__init__(context, request)
            self.fields['start_date'].widgetFactory = DateFieldWidget
            self.fields['end_date'].widgetFactory = DateFieldWidget

Since AddForm/EditForm is redefined, we must specify the forms in the field
definition::

    GridField('projects',
        row_interface = IProjectRow,
        add_form = ProjectAddForm,
        edit_form = ProjectEditForm,
        widget = GridWidget(label="Projects")
    )

Example
=======

If you want to test archetypes.gridfield in separate buildout, checkout full
package from SVN and use example.cfg buildout configuration::

    svn co http://svn.plone.org/svn/archetypes/MoreFieldsAndWidgets/archetypes.gridfield/trunk gridfield
    cd gridfield
    python2.4 bootstrap.py
    bin/buildout -c example.cfg
    bin/instance fg
    
Finally visit base_view template of any object, eg. frontpage:

    http://127.0.0.1:8080/portal/front-page/base_view
    
Usage in custom buildout
========================

Please note, package is still in the development. Requires branch of
plone.app.jquerytools and some custom version pins. Everything is set-up in
example buildout so copy the requirements from it.
