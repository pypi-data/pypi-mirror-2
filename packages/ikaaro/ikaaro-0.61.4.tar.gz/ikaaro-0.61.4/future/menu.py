# -*- coding: UTF-8 -*-
# Copyright (C) 2008 Henry Obein <henry@itaapy.com>
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

# Import from standard Library
from copy import deepcopy

# Import from itools
from itools.datatypes import String, Enumerate, Unicode, Integer
from itools.gettext import MSG
from itools.handlers import checkid
from itools.uri import Path, get_reference
from itools.web import get_context
from itools.xml import XMLParser

# Import from ikaaro
from ikaaro import messages
from ikaaro.buttons import Button
from ikaaro.exceptions import ConsistencyError
from ikaaro.folder import Folder
from ikaaro.folder_views import Folder_NewResource, Folder_BrowseContent
from ikaaro.folder_views import Folder_Rename, Folder_PreviewContent
from ikaaro.folder_views import Folder_Thumbnail, GoToSpecificDocument
from ikaaro.folder_views import Folder_Orphans
from ikaaro.forms import PathSelectorWidget
from ikaaro.forms import TextWidget, SelectWidget, ReadOnlyWidget
from ikaaro.resource_views import DBResource_AddLink
from ikaaro.revisions_views import DBResource_CommitLog
from ikaaro.table import OrderedTableFile, OrderedTable
from ikaaro.table_views import OrderedTable_View
from ikaaro.workflow import get_workflow_preview



def get_reference_and_path(value):
    """Return the reference associated to the path and the path
    without query/fragment.
    """
    # Be robust if the path is multilingual (Unicode multiple)
    path = value
    if type(path) is unicode:
        path = Unicode.encode(value)
    ref = get_reference(path)
    return ref, str(ref.path)


class NotAllowedError(Exception):
    pass



class Target(Enumerate):

    options = [{'name': '_blank', 'value': MSG(u'New page')},
               {'name': '_top', 'value': MSG(u'Current page')}]



class MenuFile(OrderedTableFile):

    record_properties = {
        'title': Unicode(multiple=True),
        'path': String,
        'target': Target(mandatory=True, default='_top'),
        'child': String}



class ChildButton(Button):

    access = 'is_allowed_to_edit'
    name = 'add_child'
    title = MSG(u'Add Child')
    css = 'button-add'



class Menu_View(OrderedTable_View):

    access = 'is_allowed_to_edit'
    schema = {
        'ids': Integer(multiple=True, mandatory=True)}
    styles = ['/ui/future/style.css']

    table_actions = [ChildButton] + OrderedTable_View.table_actions


    def get_items(self, resource, context):
        items = resource.handler.get_records_in_order()
        return list(items)


    def get_table_columns(self, resource, context):
        columns = [
            ('checkbox', None),
            ('id', MSG(u'id'))]
        # From the schema
        for widget in self.get_widgets(resource, context):
            if widget.name == 'path':
                continue
            column = (widget.name, getattr(widget, 'title', widget.name))
            columns.append(column)
        # Add the workflow state
        columns.append(('workflow_state', MSG(u'Workflow State')))

        return columns


    def get_item_value(self, resource, context, item, column):
        get_value = resource.handler.get_record_value
        value = get_value(item, column)
        if column == 'title':
            path = get_value(item, 'path')
            # Get the reference and path
            ref, path = get_reference_and_path(path)
            if ref.scheme or path.count(';'):
                # External link or method
                return value, path
            if ref.path.is_absolute():
                site_root = context.resource.get_site_root()
                path = site_root.get_abspath().resolve2('.%s' % path)
            resource_item = resource.get_resource(path, soft=True)
            # Broken link
            if resource_item is None:
                return value
            # Build the new reference with the right path
            ref2 = deepcopy(ref)
            ref2.path = context.get_link(resource_item)
            return value, str(ref2)
        elif column == 'child':
            if not value:
                return None
            child = resource.parent.get_resource(value, soft=True)
            if child is None:
                return None
            return 'edit', context.get_link(child)
        elif column == 'workflow_state':
            path = get_value(item, 'path')
            if not path:
                # Do not display a workflow state if there is no path defined.
                return
            # Get the reference and path
            ref, path = get_reference_and_path(path)
            if ref.scheme or path.count(';'):
                # External link or method
                return None
            if ref.path.is_absolute():
                site_root = context.resource.get_site_root()
                path = site_root.get_abspath().resolve2('.%s' % path)
            item_resource = resource.get_resource(path, soft=True)
            # Broken link
            if item_resource is None:
                title = MSG(u'The resource does not exist anymore.')
                title = title.gettext().encode('utf-8')
                label = MSG(u'Broken').gettext().encode('utf-8')
                link = context.get_link(resource)
                state = ('<a href="%s/;edit_record?id=%s" class="workflow"'
                         'title="%s"><strong class="broken">%s</strong>'
                         '</a>') % (link, item.id, title, label)
                return XMLParser(state)
            # The workflow state
            return get_workflow_preview(item_resource, context)

        return OrderedTable_View.get_item_value(self, resource, context, item,
                                                column)


    #######################################################################
    # Form Actions
    #######################################################################
    def action_remove(self, resource, context, form):
        ids = form['ids']
        removed = []
        not_removed = []
        referenced = []
        for id in ids:
            try:
                resource.del_record(id)
            except ConsistencyError, e:
                referenced.append(str(id))
            except NotAllowedError:
                not_removed.append(str(id))
            else:
                removed.append(str(id))

        message = []
        if removed:
            resources = ', '.join(removed)
            msg = messages.MSG_RESOURCES_REMOVED(resources=resources)
            message.append(msg)
        if referenced:
            resources = ', '.join(referenced)
            msg = messages.MSG_RESOURCES_REFERENCED(resources=resources)
            message.append(msg)
        if not_removed:
            resources = ', '.join(not_removed)
            msg = messages.MSG_RESOURCES_NOT_REMOVED(resources=resources)
            message.append(msg)
        if not removed and not referenced and not not_removed:
            message.append(messages.MSG_NONE_REMOVED)
        context.message = message

        # Reindex the resource
        context.database.change_resource(resource)


    def action_add_child(self, resource, context, form):
        handler = resource.handler
        parent = resource.parent
        for parent_id in form['ids']:
            # generate the name of the new table
            parent_record = handler.get_record(parent_id)
            # check if the child already exists
            child_path = handler.get_record_value(parent_record, 'child')
            if child_path and parent.get_resource(child_path, soft=True):
                continue

            names = parent.get_names()
            index = len(names) / 2
            base = 'menu '
            name = checkid('%s%03d' % (base, index))

            while name in names:
                index = index + 1
                name = checkid('%s%03d' % (base, index))

            cls = resource.parent.class_menu
            object = cls.make_resource(cls, parent, name)

            # update the parent record
            handler.update_record(parent_id, **{'child': name})

        context.message = messages.MSG_NEW_RESOURCE



class Menu_AddLink(DBResource_AddLink):

    def get_start(self, resource):
        return resource.get_site_root()



class Menu(OrderedTable):

    class_id = 'ikaaro-menu'
    class_title = MSG(u'iKaaro Menu')
    class_handler = MenuFile
    class_views = ['view', 'add_record']

    # Views
    add_link = Menu_AddLink()
    view = Menu_View()


    form = [TextWidget('title', title=MSG(u'Title')),
            PathSelectorWidget('path', title=MSG(u'Path')),
            SelectWidget('target', title=MSG(u'Target')),
            ReadOnlyWidget('child')]


    def del_record(self, id):
        handler = self.handler
        record = handler.get_record(id)
        record_properties = handler.record_properties

        # Delete submenu
        if 'child' in record_properties:
            child_path = handler.get_record_value(record, 'child')
            if child_path:
                container = self.parent
                child = container.get_resource(child_path, soft=True)
                if child is not None:
                    ac = child.get_access_control()
                    user = get_context().user
                    if ac.is_allowed_to_remove(user, child):
                        if child.handler.get_n_records():
                            raise NotAllowedError
                        # Remove the child table
                        # May raise a ConsistencyError
                        container.del_resource(child_path)
                    else:
                        raise NotAllowedError

        # Delete the record
        handler.del_record(id)


    def _is_allowed_to_access(self, context, uri):
        # Get the reference and path
        ref, path = get_reference_and_path(uri)
        if ref.scheme:
            # External link
            return True

        user = context.user
        site_root_abspath = context.resource.get_site_root().get_abspath()
        if ref is None or path == '':
            # Skip broken entry
            return False
        elif path.count(';'):
            path, method = path.split(';')
            if ref.path.is_absolute():
                path = site_root_abspath.resolve2('.%s' % path)
            resource = self.get_resource(path, soft=True)
            if resource is None:
                return False
            # Check ACL
            ac = resource.get_access_control()
            view = resource.get_view(method, ref.query)
            if view:
                return ac.is_access_allowed(user, resource, view)
        else:
            # Internal link
            if ref.path.is_absolute():
                path = site_root_abspath.resolve2('.%s' % path)
            resource = self.get_resource(path, soft=True)
            # Broken link
            if resource is None:
                return False

            # FIXME We should take into account the show_first_child
            # parameter
            ac = resource.get_access_control()
            return ac.is_allowed_to_view(user, resource)


    def get_menu_namespace_level(self, context, url, depth=2,
                                 use_first_child=False, flat=False):
        parent = self.parent
        handler = self.handler
        menu_abspath = self.get_abspath()
        here = context.resource
        here_abspath = here.get_canonical_path()
        site_root_abspath = here.get_site_root().get_abspath()
        items = []
        tabs = {}
        get_value = handler.get_record_value
        for record in handler.get_records_in_order():
            # Get the objects, check security
            uri = get_value(record, 'path')
            if self._is_allowed_to_access(context, uri) is False:
                continue
            title = get_value(record, 'title')
            target = get_value(record, 'target')
            # Subtabs
            subtabs = {}
            # Get the reference and path
            ref, path = get_reference_and_path(uri)
            if ref.scheme or path.count(';'):
                # Special case for external link and method
                id = 'menu_'
                css = None
                if not ref.scheme:
                    # FIXME We should check the ACL of the method
                    # Get the resource associated to the method
                    _path, method_name = path.split(';')
                    if ref.path.is_absolute():
                        real_path = site_root_abspath.resolve2('.%s' % _path)
                    else:
                        real_path = _path
                    resource = self.get_resource(real_path)
                    if here_abspath == resource.get_canonical_path():
                        if context.view_name == method_name:
                            css = 'in-path'
                    id += method_name
                    # Build the new reference with the right path
                    ref2 = deepcopy(ref)
                    ref2.path = '%s/;%s' % (context.get_link(resource),
                                            method_name)
                else:
                    id += str(record.id)
                    ref2 = ref

                items.append({'id': id,
                              'path': str(ref2),
                              'real_path': None,
                              'title': title,
                              'description': None,
                              'in_path': False,
                              'active': False,
                              'class': css,
                              'target': target})
            else:
                # Internal link
                if ref.path.is_absolute():
                    path = site_root_abspath.resolve2('.%s' % path)
                resource = self.get_resource(path, soft=True)
                # Broken link
                if resource is None:
                    continue
                name = resource.name

                # Use first child by default we use the resource itself
                resource_path = path
                # Keep the real path to avoid highlight problems
                resource_original_path = path
                if depth > 1:
                    # Check the child
                    child_path = get_value(record, 'child')
                    if child_path:
                        child = parent.get_resource(child_path, soft=True)
                        if child is not None:
                            # Sub level
                            get_menu_ns_lvl = child.get_menu_namespace_level
                            subtabs = get_menu_ns_lvl(context, url, depth - 1,
                                                      use_first_child, flat)
                            # use first child
                            if use_first_child and subtabs['items']:
                                sub_path = subtabs['items'][0]['real_path']
                                # if the first child is an external link =>
                                # skip it
                                if sub_path is not None:
                                    resource_path = sub_path

                # Set active, in_path
                active = False
                if here_abspath == resource.get_canonical_path():
                    active, in_path = True, False
                else:
                    # Use the original path for the highlight
                    res_abspath = menu_abspath.resolve2(resource_original_path)
                    common_prefix = here_abspath.get_prefix(res_abspath)
                    in_path = False
                    # Avoid to always set the site_root entree 'in_path'
                    # If common prefix equals site root abspath
                    # set in_path to False otherwise compare
                    # common_prefix and res_abspath
                    if common_prefix != site_root_abspath:
                        in_path = (common_prefix == res_abspath)

                # Set css class to 'active', 'in-path' or None
                css = 'in-path' if (active or in_path) else None

                # Build the new reference with the right path
                ref2 = deepcopy(ref)
                resource = self.get_resource(resource_path)
                ref2.path = context.get_link(resource)
                items.append({'id': 'menu_%s' % name,
                              'path': str(ref2),
                              'real_path': resource.get_abspath(),
                              'title': title,
                              'description': None, # FIXME
                              'in_path': css == 'in-path' or active,
                              'active': active,
                              'class': css,
                              'target': target})
            items[-1]['items'] = subtabs.get('items', [])
        tabs['items'] = items
        return tabs


    def get_first_level_uris(self, context):
        """Return a list of the URI of all entries in the first level
        """
        handler = self.handler
        site_root = context.resource.get_site_root()
        site_root_abspath = site_root.get_abspath()
        user = context.user
        get_value = handler.get_record_value
        uris = []
        for record in handler.get_records_in_order():
            # Get the objects, check security
            uri = get_value(record, 'path')
            # Get the reference and path
            ref, path = get_reference_and_path(uri)
            if ref.scheme:
                # External link
                uris.append(ref)
                continue
            if self._is_allowed_to_access(context, uri) is False:
                continue
            if path.count(';'):
                path, method = path.split(';')
                if ref.path.is_absolute():
                    path = site_root_abspath.resolve2('.%s' % path)
                resource = self.get_resource(path)
            else:
                path = site_root_abspath.resolve2('.%s' % path)
                resource = self.get_resource(path)
            # Build the new reference with the right path
            ref2 = deepcopy(ref)
            ref2.path = context.get_link(resource)
            uris.append(ref2)

        return uris


    def get_links(self):
        base = self.get_abspath()
        site_root_abspath = self.get_site_root().get_abspath()
        handler = self.handler
        record_properties = handler.record_properties
        links = []

        for record in handler.get_records_in_order():
            # Target resources
            path = handler.get_record_value(record, 'path')
            ref, path = get_reference_and_path(path)
            if ref.scheme:
                continue
            if path.count(';'):
                path, method = path.split(';')
            if ref.path.is_absolute():
                uri = site_root_abspath.resolve2('.%s' % path)
            else:
                uri = base.resolve2(path)
            try:
                # Use the canonical path instead of the uri stocked
                resource = self.get_resource(uri)
                link = str(resource.get_canonical_path())
            except LookupError:
                # If the resource does not exist, simply use the uri
                link = str(uri)
            links.append(link)
            # Submenu resources
            if not 'child' in record_properties:
                continue
            path = handler.get_record_value(record, 'child')
            if path:
                container = self.parent
                child = container.get_resource(path, soft=True)
                if child is not None:
                    # take into account the submenu if it is not empty
                    if child.handler.get_n_records():
                        uri = site_root_abspath.resolve(path)
                        links.append(str(uri))

        return links


    def update_links(self, source, target):
        handler = self.handler
        base = self.get_abspath()
        # FIXME The context is not available when updating the catalog.
        site_root_abspath = self.parent.parent.get_abspath()

        for record in handler.get_records_in_order():
            path = handler.get_record_value(record, 'path')
            ref, path = get_reference_and_path(path)
            if ref.scheme:
                continue
            if path.count(';'):
                path, method = path.split(';')
            if ref.path.is_absolute():
                uri = site_root_abspath.resolve2('.%s' % path)
            else:
                uri = base.resolve2(path)
            uri = str(uri)
            if uri == source:
                # Hit the old name
                new_path2 = base.get_pathto(Path(target))
                handler.update_record(record.id, **{'path': str(new_path2)})
        get_context().database.change_resource(self)



class MenuFolder(Folder):

    class_id = 'menu-folder'
    class_title = MSG(u'iKaaro Menu')
    class_views = ['view']
    __fixed_handlers__ = Folder.__fixed_handlers__ + ['menu']
    # Your menu ressource (for overriding the record_properties and form)
    class_menu = Menu

    # Views
    view = GoToSpecificDocument(specific_document='menu',
                                title=MSG(u'View'),
                                access='is_allowed_to_edit')
    # Disable all default views
    new_resource = Folder_NewResource(access='is_admin')
    browse_content = Folder_BrowseContent(access='is_admin')
    rename = Folder_Rename(access='is_admin')
    preview_content = Folder_PreviewContent(access='is_admin')
    commit_log = DBResource_CommitLog(access='is_admin')
    orphans = Folder_Orphans(access='is_admin')
    thumb = Folder_Thumbnail(access='is_admin')


    @staticmethod
    def _make_resource(cls, folder, name, **kw):
        Folder._make_resource(cls, folder, name, **kw)
        # Menu root
        cls_menu = cls.class_menu
        cls_menu._make_resource(cls_menu, folder, '%s/menu' % name)


    def get_document_types(self):
        return []


    def get_menu_namespace_level(self, context, url, depth=2,
                                 use_first_child=False, flat=False):
        menu_root = self.get_resource('menu')
        return menu_root.get_menu_namespace_level(context, url, depth,
                                                  use_first_child, flat)


    def get_first_level_uris(self, context):
        menu_root = self.get_resource('menu')
        return menu_root.get_first_level_uris(context)



def get_menu_namespace(context, depth=3, show_first_child=False, flat=True,
                       src=None):
    """Return dict with the following structure:

    {'items': [item_dic01, ..., item_dic0N]}

    Where the list of items is the first level
    and item_dic = {'active': True or False,
                    'class': 'active' or 'in_path' or None,
                    'description': MSG(u'About Python'),
                    'id': 'tab_python',
                    'in_path': True or False,
                    'items': [item_dic11, ..., item_dic1N] or None,
                    'name': 'python',
                    'path': '../python',
                    'target': '_top' or '_blank' or None,
                    'title': MSG(u'Python')}

    If "flat" is true (the default), the menu is also represented with a
    flattened structure:

    {'items': [...],
     'flat': {'lvl0': [item_dic01, ..., item_dic0N],
              'lvl1': [item_dic11, ..., item_dic1N],
              [...]
              'lvlN': [item_dicN1, ..., item_dicNN]}}

    "items" contains the first level. Each item_dic contains in turn an 'items'
    with its children.
    "class" is a CSS class decorating the item when active on within the
    current path.
    "id" is a CSS id to uniquely identify the item, based on the title.
    "target" is the anchor target (opening a new window or not).

    Activate "use_first_child" to automatically point to the first child of
    each item instead of the item itself.
    """
    resource = context.resource
    url = list(context.uri.path)
    if not url or url[-1][0] != ';':
        method = resource.get_default_view_name()
        url.append(';%s' % method)

    # Get the menu
    tabs = {'items': []}
    if src is None:
        src = 'menu'
    site_root = resource.get_site_root()
    menu = site_root.get_resource(src, soft=True)
    if menu is not None:
        tabs = menu.get_menu_namespace_level(context, url, depth,
                                             show_first_child)

    if flat:
        tabs['flat'] = {}
        items = tabs['flat']['lvl0'] = tabs.get('items', None)
        # initialize the levels
        for i in range(1, depth):
            tabs['flat']['lvl%s' % i] = None
        exist_items = True
        lvl = 1
        while (items is not None) and exist_items:
            exist_items = False
            for item in items:
                if item['class'] in ['active', 'in-path']:
                    if item['items']:
                        items = exist_items = item['items']
                        if items:
                            tabs['flat']['lvl%s' % lvl] = items
                            lvl += 1
                        break
                    else:
                        items = None
                        break
    return tabs

