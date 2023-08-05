#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2005-2007 Juan David Ibáñez Palomar <jdavid@itaapy.com>
# Copyright (C) 2007 Sylvain Taverne <sylvain@itaapy.com>
# Copyright (C) 2008 David Versmisse <david.versmisse@itaapy.com>
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
from optparse import OptionParser

# Import from itools
import itools

# Import from ikaaro
from ikaaro.server import Server
from ikaaro.utils import kill



def stop(parser, options, target):
    # Stop the Web Server
    server = Server(target, read_only=True)
    pid = server.get_pid()
    if pid is None:
        print '[%s] Web Server not running.' % target
    else:
        kill(pid, force=options.force)
        if options.force:
            print '[%s] Web Server shutting down...' % target
        else:
            print '[%s] Web Server shutting down (gracefully)...' % target


if __name__ == '__main__':
    # The command line parser
    usage = '%prog TARGET [TARGET]*'
    version = 'itools %s' % itools.__version__
    description = ('Stops the web server that is publishing the TARGET'
                   ' ikaaro instance (if it is running). Accepts'
                   ' several TARGETs at once, to stop several servers.')
    parser = OptionParser(usage, version=version, description=description)
    parser.add_option(
        '--force', action="store_true", default=False,
        help="Emits SIGTERM instead of SIGINT signal.")

    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error('incorrect number of arguments')

    # Action!
    for target in args:
        stop(parser, options, target)
