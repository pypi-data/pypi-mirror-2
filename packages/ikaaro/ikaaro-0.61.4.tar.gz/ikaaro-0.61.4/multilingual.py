# -*- coding: UTF-8 -*-
# Copyright (C) 2007-2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
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

# Import from itools
from itools.fs import FileName
from itools.web import get_context

# Import from ikaaro
from resource_ import DBResource


class Multilingual(DBResource):

    def __init__(self, metadata):
        self.metadata = metadata
        self.handlers = {}
        # The tree
        self.name = ''
        self.parent = None


    @staticmethod
    def _make_resource(cls, folder, name, body=None, filename=None,
                       language=None, **kw):
        DBResource._make_resource(cls, folder, name, filename=filename, **kw)
        # Add the body
        if body is not None:
            cls = cls.class_handler
            handler = cls(string=body)
            name = FileName.encode((name, cls.class_extension, language))
            folder.set_handler(name, handler)


    def get_handler(self, language=None):
        # Content language
        if language is None:
            site_root = self.get_site_root()
            ws_languages = site_root.get_property('website_languages')
            handlers = [
                (x, self.get_handler(language=x)) for x in ws_languages ]
            languages = [ x for (x, y) in handlers if not y.is_empty() ]
            language = self.get_content_language(get_context(), languages)
            # Default
            if language is None:
                language = ws_languages[0]
        # Hit
        if language in self.handlers:
            return self.handlers[language]
        # Miss
        cls = self.class_handler
        metadata = self.metadata
        database = metadata.database
        fs = database.fs
        name = FileName.encode((self.name, cls.class_extension, language))
        key = fs.resolve(metadata.key, name)
        if database.has_handler(key):
            handler = database.get_handler(key, cls=cls)
        else:
            handler = cls()
            database.push_phantom(key, handler)

        self.handlers[language] = handler
        return handler

    handler = property(get_handler, None, None, '')


    def get_handlers(self):
        languages = self.get_site_root().get_property('website_languages')
        return [ self.get_handler(language=x) for x in languages ]


    def rename_handlers(self, new_name):
        old_name = self.name
        extension = self.class_handler.class_extension
        langs = self.get_site_root().get_property('website_languages')

        return [ (FileName.encode((old_name, extension, x)),
                  FileName.encode((new_name, extension, x)))
                 for x in langs ]

