# -*- coding: UTF-8 -*-
# Copyright (C) 2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
from urllib import quote

# Import from itools
from itools.core import freeze
from itools.datatypes import String, Unicode
from itools.gettext import MSG
from itools.handlers import checkid
from itools.web import FormError

# Import from ikaaro
from forms import AutoForm, TextWidget, title_widget
import messages
from registry import get_resource_class, get_document_types
from views import ContextMenu



class AddResourceMenu(ContextMenu):

    title = MSG(u'Add Resource')

    def get_items(self, resource, context):
        base = '%s/;new_resource' % context.get_link(resource)
        document_types = resource.get_document_types()
        return [
            {'src': '/ui/' + cls.class_icon16,
             'title': cls.class_title.gettext(),
             'href': '%s?type=%s' % (base, quote(cls.class_id))}
            for cls in document_types ]



class NewInstance(AutoForm):
    """This is the base class for all ikaaro forms meant to create and
    add a new resource to the database.
    """

    access = 'is_allowed_to_add'
    query_schema = freeze({
        'type': String,
        'name': String,
        'title': Unicode})
    schema = freeze({
        'name': String,
        'title': Unicode})
    widgets = freeze([
        title_widget,
        TextWidget('name', title=MSG(u'Name'), default='')])
    submit_value = MSG(u'Add')
    context_menus = freeze([AddResourceMenu()])


    def get_title(self, context):
        if self.title is not None:
            return self.title
        type = context.query['type']
        if not type:
            return MSG(u'Add resource').gettext()
        cls = get_resource_class(type)
        class_title = cls.class_title.gettext()
        title = MSG(u'Add {class_title}')
        return title.gettext(class_title=class_title)


    def get_value(self, resource, context, name, datatype):
        if name in self.get_query_schema():
            return context.query[name]
        return AutoForm.get_value(self, resource, context, name, datatype)


    def icon(self, resource, **kw):
        type = kw.get('type')
        cls = get_resource_class(type)
        if cls is not None:
            return cls.get_class_icon()
        # Default
        return 'new.png'


    def get_new_resource_name(self, form):
        # If the name is not explicitly given, use the title
        name = form['name']
        title = form['title'].strip()
        if name is None:
            return title
        return name or title


    def _get_form(self, resource, context):
        form = AutoForm._get_form(self, resource, context)
        name = self.get_new_resource_name(form)

        # Check the name
        if not name:
            raise FormError, messages.MSG_NAME_MISSING

        try:
            name = checkid(name)
        except UnicodeEncodeError:
            name = None

        if name is None:
            raise FormError, messages.MSG_BAD_NAME

        # Check the name is free
        if resource.get_resource(name, soft=True) is not None:
            raise FormError, messages.MSG_NAME_CLASH

        # Ok
        form['name'] = name
        return form


    def action(self, resource, context, form):
        name = form['name']
        title = form['title']

        # Create the resource
        class_id = context.query['type']
        cls = get_resource_class(class_id)
        child = cls.make_resource(cls, resource, name)
        # The metadata
        metadata = child.metadata
        language = resource.get_content_language(context)
        metadata.set_property('title', title, language=language)

        goto = './%s/' % name
        return context.come_back(messages.MSG_NEW_RESOURCE, goto=goto)



class ProxyNewInstance(NewInstance):
    """This particular view allows to choose the resource to add from a
    collection of resource classes, with radio buttons.
    """

    template = '/ui/base/proxy_new_instance.xml'
    schema = {
        'name': String,
        'title': Unicode,
        'class_id': String}


    def get_namespace(self, resource, context):
        type = context.query['type']
        cls = get_resource_class(type)

        document_types = get_document_types(type)
        items = []
        if document_types:
            # Multiple types
            if len(document_types) == 1:
                items = None
            else:
                selected = context.get_form_value('class_id')
                items = [
                    {'title': x.class_title.gettext(),
                     'class_id': x.class_id,
                     'selected': x.class_id == selected,
                     'icon': '/ui/' + x.class_icon16}
                    for x in document_types ]
                if selected is None:
                    items[0]['selected'] = True
        # Ok
        return {
            'class_id': cls.class_id,
            'class_title': cls.class_title.gettext(),
            'items': items}


    def action(self, resource, context, form):
        name = form['name']
        title = form['title']

        # Create the resource
        class_id = form['class_id']
        if class_id is None:
            # Get it from the query
            class_id = context.query['type']
        cls = get_resource_class(class_id)
        child = cls.make_resource(cls, resource, name)
        # The metadata
        metadata = child.metadata
        language = resource.get_content_language(context)
        metadata.set_property('title', title, language=language)

        goto = './%s/' % name
        return context.come_back(messages.MSG_NEW_RESOURCE, goto=goto)

