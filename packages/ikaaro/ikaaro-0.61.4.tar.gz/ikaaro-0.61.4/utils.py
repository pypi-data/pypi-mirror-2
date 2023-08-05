# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Hervé Cauwelier <herve@itaapy.com>
# Copyright (C) 2007 Nicolas Deram <nicolas@itaapy.com>
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

# Import from the Standard Library
from random import sample
from hashlib import sha1
from sys import platform

# Import from itools
from itools.web import get_context
from itools.xapian import AllQuery, PhraseQuery, NotQuery, OrQuery, StartQuery

if platform[:3] == 'win':
    from utils_win import is_pid_running, kill
else:
    from utils_unix import is_pid_running, kill


###########################################################################
# Navigation helper functions
###########################################################################
def get_parameters(prefix, **kw):
    """Gets the parameters from the request form, the keyword argument
    specifies which are the parameters to get and which are their default
    values.

    The prefix argument lets to create different namespaces for the
    parameters, so the same page web can have different sections with
    different but equivalent parameters.

    For example, call it like:

      get_parameters('resources', sortby='id', sortorder='up')
    """
    # Get the form field from the request (a zope idiom)
    get_parameter = get_context().get_form_value

    # Get the parameters
    parameters = {}
    for key, value in kw.items():
        parameters[key] = get_parameter('%s_%s' % (prefix, key),
                                        default=value)

    return parameters



###########################################################################
# Languages
###########################################################################

# Mark for translatios
u'Basque'
u'Catalan'
u'English'
u'French'
u'German'
u'Hungarian'
u'Italian'
u'Japanese'
u'Portuguese'
u'Spanish'


###########################################################################
# String format for display
###########################################################################

def reduce_string(title='', word_treshold=15, phrase_treshold=40):
    """Reduce words and string size.
    """
    ellipsis = '…'
    if isinstance(title, unicode):
        ellipsis = u'…'
    words = title.strip().split(' ')
    for i, word in enumerate(words):
        if len(word) > word_treshold:
            words.pop(i)
            word = word[:word_treshold] + ellipsis
            words.insert(i, word)
    title = ' '.join(words)
    if len(title) > phrase_treshold:
        # Remove right trailling whitespaces
        title = title[:phrase_treshold].rstrip()
        # Only add ellipsis if the last word does not already
        # end with one
        if not title.endswith(ellipsis):
            title += ellipsis
    return title


###########################################################################
# User and Authentication
###########################################################################
# ASCII letters and digits, except the characters: 0, O, 1, l
tokens = 'abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789'
def generate_password(length=6):
    return ''.join(sample(tokens, length))


def crypt_password(password):
    return sha1(password).digest()


###########################################################################
# Generate next name
###########################################################################
def generate_name(name, used, suffix='_'):
    """Generate a name which is not in list "used" based on name and suffix.
    Example:
      With name='toto.txt', used=['toto.txt', 'toto_0.txt']
      --> toto.txt and toto_0.txt are used so it returns toto_1.txt
      With name='toto.txt', used=['toto.txt', 'toto_0.txt'], suffix='_copy_'
      --> toto.txt is used so it returns toto_copy_0.txt
    """
    if name not in used:
        return name

    items = name.split('.', 1)
    basename = items[0]
    extent = ''
    if len(items) > 1:
        extent = '.%s' % items[1]

    # 1st time called
    if suffix not in basename:
        index = 0
    else:
        basename, index = basename.rsplit(suffix, 1)
        try:
            index = int(index) + 1
        except ValueError:
            basename = '%s%s%s' % (basename, suffix, index)
            index = 0

    name = ''.join([basename, suffix, str(index), extent])
    while name in used:
        index += 1
        name = ''.join([basename, suffix, str(index), extent])

    return str(name)



###########################################################################
# Index and Search
###########################################################################
def get_base_path_query(abspath, include_container=False):
    """Builds a query that will return all the objects within the given
    absolute path, like it is returned by 'resource.get_abspath()'.

    If 'include_container' is true the resource at the given path will be
    returned too.
    """
    # Case 1: everything
    if abspath == '/' and include_container is True:
        return AllQuery()

    # Case 2: everything but the root
    if abspath == '/':
        return NotQuery(PhraseQuery('abspath', '/'))

    # Case 3: some subfolder
    content = StartQuery('abspath', abspath + '/')
    if include_container is False:
        return content

    container = PhraseQuery('abspath', abspath)
    return OrQuery(container, content)

