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
from base64 import decodestring, encodestring
from marshal import dumps, loads
from urllib import quote, unquote
from zlib import compress, decompress

# Import from itools
from itools.core import freeze, guess_type
from itools.datatypes import DataType, Enumerate


"""This module defines some datatypes used in ikaaro, whose inclusion in
itools is not yet clear.
"""


class FileDataType(DataType):
    """FIXME This datatype is special in that it does not deserializes from
    a byte string, but from a tuple.  Some day we should find a correct
    solution.
    """
    @staticmethod
    def encode(value):
        """Cannot preload anything in a file input.
        """
        return None


    @staticmethod
    def decode(data):
        """Find out the resource class (the mimetype sent by the browser can be
        minimalistic).
        """
        filename, mimetype, body = data
        # Find out the mimetype
        guessed, encoding = guess_type(filename)
        if encoding is not None:
            encoding_map = {'gzip': 'application/x-gzip',
                            'bzip2': 'application/x-bzip2'}
            if encoding in encoding_map:
                mimetype = encoding_map[encoding]
        elif guessed is not None:
            mimetype = guessed

        return filename, mimetype, body



class Password(DataType):

    @staticmethod
    def decode(data):
        return decodestring(unquote(data))


    @staticmethod
    def encode(value):
        return quote(encodestring(value))



class CopyCookie(DataType):

    default = None, freeze([])

    @staticmethod
    def encode(value):
        return quote(compress(dumps(value), 9))


    @staticmethod
    def decode(str):
        return loads(decompress(unquote(str)))



class ImageWidth(Enumerate):
    options = [{'name': '640', 'value': u"small"},
               {'name': '800', 'value': u"medium"},
               {'name': '1024', 'value': u"large"},
               {'name': '1280', 'value': u"huge"},
               {'name': '', 'value': u"original"}]
