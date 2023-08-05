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
from sys import platform, version_info

# Import from itools
from cache import LRUCache
from freeze import freeze, frozendict, frozenlist
from lazy import lazy
from mimetypes_ import add_type, guess_all_extensions, guess_extension
from mimetypes_ import guess_type, has_encoding, has_extension
from odict import OrderedDict
from thingy import thingy_type, thingy, thingy_property, thingy_lazy_property
from utils import get_abspath, merge_dicts, get_pipe, get_version

# Python 2.6 or 2.5
if version_info[1] == 5:
    from py25 import get_sizeof
    start_subprocess = stop_subprocess = None
    read_subprocess = send_subprocess = None
else:
    from py26 import get_sizeof
    from subprocess_ import start_subprocess, stop_subprocess
    from subprocess_ import read_subprocess, send_subprocess

# Posix or Windows
if platform[:3] == 'win':
    from _win import become_daemon, fork, get_time_spent, vmsize
else:
    from _unix import become_daemon, fork, get_time_spent, vmsize



__all__ = [
    # Thingies are cool
    'thingy_type',
    'thingy',
    'thingy_property',
    'thingy_lazy_property',
    # Frozen types
    'freeze',
    'frozendict',
    'frozenlist',
    # Lazy load
    'lazy',
    # Ordered dict and caching
    'OrderedDict',
    'LRUCache',
    # Mimetypes
    'add_type',
    'guess_all_extensions',
    'guess_extension',
    'guess_type',
    'has_encoding',
    'has_extension',
    # Subprocess
    'start_subprocess',
    'read_subprocess',
    'send_subprocess',
    'stop_subprocess',
    # Utility functions
    'get_abspath',
    'get_version',
    'merge_dicts',
    'get_sizeof',
    'get_pipe',
    # System specific functions
    'become_daemon',
    'fork',
    'get_time_spent',
    'vmsize',
   ]

