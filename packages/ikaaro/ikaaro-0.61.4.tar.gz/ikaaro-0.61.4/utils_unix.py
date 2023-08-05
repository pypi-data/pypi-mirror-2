# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Juan David Ibáñez Palomar <jdavid@itaapy.com>
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
from os import getpgid
import os
from signal import SIGINT, SIGTERM


def is_pid_running(pid):
    """returns true if there is a process with the given pid working.
    """
    try:
        getpgid(pid)
    except OSError:
        return False
    return True



def kill(pid, force=False):
    if force:
        os.kill(pid, SIGTERM)
    else:
        os.kill(pid, SIGINT)
