# -*- coding: UTF-8 -*-
# Copyright (C) 2006-2007 Hervé Cauwelier <herve@itaapy.com>
# Copyright (C) 2006-2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
# Copyright (C) 2008 Nicolas Deram <nicolas@itaapy.com>
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
from re import compile

# Import from itools
from itools.core import add_type
from itools.csv import CSVFile
from itools.gettext import POFile, MSG
from itools.handlers import TextFile
from itools.html import HTMLFile
from itools.python import Python as PythonFile
from itools.uri import get_reference, Path, Reference
from itools.web import get_context
from itools.xmlfile import XMLFile

# Import from ikaaro
from file import File
from file_views import File_Edit, File_ExternalEdit_View
from registry import register_resource_class
from text_views import Text_Edit, Text_View, PO_Edit
from text_views import CSV_View, CSV_AddRow, CSV_EditRow


# FIXME Add support for thumb
css_uri_expr = compile(
        r"url\(['\"]{0,1}([a-zA-Z0-9\./\-\_]*/;download)['\"]{0,1}\);")

# FIXME This list should be built from a txt file with all the
# encodings, or better, from a Python module that tells us which
# encodings Python supports.
encodings = [
    {'value': 'utf-8', 'title': 'UTF-8', 'is_selected': True},
    {'value': 'iso-8859-1', 'title': 'ISO-8859-1', 'is_selected': False}
]


class Text(File):

    class_id = 'text'
    class_title = MSG(u'Plain Text')
    class_icon16 = 'icons/16x16/text.png'
    class_icon48 = 'icons/48x48/text.png'
    class_views = ['view', 'edit', 'externaledit', 'edit_state', 'commit_log']
    class_handler = TextFile


    def get_content_type(self):
        return '%s; charset=UTF-8' % File.get_content_type(self)


    #######################################################################
    # Views
    view = Text_View()
    edit = Text_Edit()
    externaledit = File_ExternalEdit_View(encodings=encodings)



class PO(Text):

    class_id = 'text/x-gettext-translation'
    class_title = MSG(u'Message Catalog')
    class_icon16 = 'icons/16x16/po.png'
    class_icon48 = 'icons/48x48/po.png'
    class_handler = POFile

    # Views
    edit = PO_Edit()



class CSS(Text):

    class_id = 'text/css'
    class_title = MSG(u'CSS')
    class_icon16 = 'icons/16x16/css.png'
    class_icon48 = 'icons/48x48/css.png'


    def get_links(self):
        links = Text.get_links(self)
        base = self.get_abspath()
        site_root = self.get_site_root()
        site_root_base = site_root.get_abspath()
        data = self.to_text().encode('utf-8')

        segments = css_uri_expr.findall(data)
        for segment in segments:
            reference = get_reference(segment)

            # Skip empty links, external links and links to '/ui/'
            if reference.scheme or reference.authority:
                continue
            path = reference.path
            if not path and path[0] == 'ui':
                continue

            # Strip the view
            name = path.get_name()
            if name and name[0] == ';':
                path = path[:-1]

            # Absolute path are relative to site root
            if path.is_absolute():
                # /images/xx -> images/xx
                path.startswith_slash = False
                uri = site_root_base.resolve2(path)
            else:
                uri = base.resolve2(path)

            links.append(str(uri))

        return links


    def update_links(self,  source, target):
        Text.update_links(self,  source, target)
        base = self.get_abspath()
        site_root = self.get_site_root()
        site_root_base = site_root.get_abspath()
        resources_new2old = get_context().database.resources_new2old
        base = str(base)
        old_base = resources_new2old.get(base, base)
        old_base = Path(old_base)
        old_site_root_base = resources_new2old.get(site_root_base,
                                                   site_root_base)
        old_site_root_base = Path(old_site_root_base)
        new_base = Path(base)

        def my_func(matchobj):
            uri = matchobj.group(1)
            reference = get_reference(uri)

            # Skip empty links, external links and links to '/ui/'
            if reference.scheme or reference.authority:
                return matchobj.group(0)
            path = reference.path
            if not path and path[0] == 'ui':
                return matchobj.group(0)

            # Strip the view
            name = path.get_name()
            if name and name[0] == ';':
                view = '/' + name
                path = path[:-1]
            else:
                view = ''

            # Resolve the path
            # Absolute path are relative to site root
            if path.is_absolute():
                # /images/xx -> images/xx
                path.startswith_slash = False
                path = old_site_root_base.resolve2(path)
            else:
                path = old_base.resolve2(path)

            # Match ?
            if path == source:
                new_path = str(new_base.get_pathto(target)) + view
                return "url('%s');" % new_path

            return matchobj.group(0)

        data = self.to_text().encode('utf-8')
        new_data = css_uri_expr.sub(my_func, data)
        self.handler.load_state_from_string(new_data)

        get_context().database.change_resource(self)


    def update_relative_links(self, source):
        target = self.get_abspath()
        site_root = self.get_site_root()
        site_root_base = site_root.get_abspath()
        resources_old2new = get_context().database.resources_old2new

        def my_func(matchobj):
            uri = matchobj.group(1)
            reference = get_reference(uri)

            # Skip empty links, external links and links to '/ui/'
            if reference.scheme or reference.authority:
                return matchobj.group(0)
            path = reference.path
            if not path and path[0] == 'ui':
                return matchobj.group(0)

            # Strip the view
            name = path.get_name()
            if name and name[0] == ';':
                view = '/' + name
                path = path[:-1]
            else:
                view = ''

            # Calcul the old absolute path
            # Absolute path are relative to site root
            if path.is_absolute():
                # /images/xx -> images/xx
                path.startswith_slash = False
                old_abs_path = site_root_base.resolve2(path)
            else:
                old_abs_path = source.resolve2(path)
            # Get the 'new' absolute parth
            new_abs_path = resources_old2new.get(old_abs_path, old_abs_path)

            path = str(target.get_pathto(new_abs_path)) + view
            new_value = Reference('', '', path, reference.query.copy(),
                                  reference.fragment)
            return "url('%s');" % path

        data = self.to_text().encode('utf-8')
        new_data = css_uri_expr.sub(my_func, data)
        self.handler.load_state_from_string(new_data)



class Python(Text):

    class_id = 'text/x-python'
    class_title = MSG(u'Python')
    class_icon16 = 'icons/16x16/python.png'
    class_icon48 = 'icons/48x48/python.png'
    class_handler = PythonFile



class JS(Text):

    class_id = 'application/x-javascript'
    class_title = MSG(u'Javascript')
    class_icon16 = 'icons/16x16/js.png'
    class_icon48 = 'icons/48x48/js.png'



class XML(Text):

    class_id = 'text/xml'
    class_title = MSG(u'XML File')
    class_handler = XMLFile



class HTML(Text):

    class_id = 'text/html'
    class_title = MSG(u'HTML File')
    class_handler = HTMLFile



class CSV(Text):

    class_id = 'text/comma-separated-values'
    class_title = MSG(u'Comma Separated Values')
    class_views = ['view', 'add_row', 'edit', 'externaledit', 'commit_log']
    class_handler = CSVFile


    def get_columns(self):
        """Returns a list of tuples with the name and title of every column.
        """
        handler = self.handler

        if handler.columns is None:
            row = None
            for row in handler.lines:
                if row is not None:
                    break
            if row is None:
                return []
            return [ (str(x), str(x)) for x in range(len(row)) ]

        columns = []
        for name in handler.columns:
            datatype = handler.schema[name]
            title = getattr(datatype, 'title', None)
            if title is None:
                title = name
            else:
                title = title.gettext()
            columns.append((name, title))

        return columns


    # Views
    edit = File_Edit()
    view = CSV_View()
    add_row = CSV_AddRow()
    edit_row = CSV_EditRow()



###########################################################################
# Register
###########################################################################
for js_mime in ['application/x-javascript', 'text/javascript',
                'application/javascript']:
    register_resource_class(JS, js_mime)
    add_type(js_mime, '.js')
register_resource_class(XML, format='application/xml')
register_resource_class(CSV, 'text/x-comma-separated-values')
register_resource_class(CSV, 'text/csv')

