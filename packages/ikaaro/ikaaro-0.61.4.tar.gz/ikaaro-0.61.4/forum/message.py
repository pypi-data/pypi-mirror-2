# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Henry Obein <henry@itaapy.com>
# Copyright (C) 2007 Hervé Cauwelier <herve@itaapy.com>
# Copyright (C) 2007 Sylvain Taverne <sylvain@itaapy.com>
# Copyright (C) 2007-2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
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

# Import from itools
from itools.gettext import MSG
from itools.html import HTMLParser, sanitize_stream, XHTMLFile

# Import from ikaaro
from ikaaro.webpage import WebPage


def build_message(data):
    # Parse and clean the data
    new_body = HTMLParser(data)
    new_body = sanitize_stream(new_body)
    new_body = list(new_body)

    # Insert the data in a new document
    document = XHTMLFile()
    old_body = document.get_body()
    document.events = (document.events[:old_body.start+1]
                       + new_body
                       + document.events[old_body.end:])

    # Ok
    return document



class Message(WebPage):

    class_id = 'ForumMessage'
    class_title = MSG(u'Message')
    class_description = u"Message in a thread"
    class_views = ['edit', 'history_form']


    @staticmethod
    def _make_resource(cls, folder, name, data, language):
        WebPage._make_resource(cls, folder, name)
        # The message
        document = build_message(data)
        folder.set_handler('%s.xhtml.%s' % (name, language), document)


    def _get_catalog_values(self):
        # text field was already indexed at the thread level
        result = WebPage._get_catalog_values(self)
        del result['text']
        return result

