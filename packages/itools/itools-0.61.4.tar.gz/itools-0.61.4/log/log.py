# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Juan David Ibáñez Palomar <jdavid@itaapy.com>
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

"""This package provides a simple programming interface for logging (in
contrast of the ridiculously complex 'logging' package of the Standard
Library).

It is inspired by the logging facilities of the Glib library, and will
eventually become just a wrapper of it (once pygobject exposes that part
of the Glib API).
"""

# Import from the Standard Library
from os import getpid
from socket import gethostname
from sys import exc_info, exit, stdout, stderr
from time import strftime
from traceback import format_exception


# Log levels
FATAL = (1 << 4)
ERROR = (1 << 3)
WARNING = (1 << 2)
INFO = (1 << 1)
DEBUG = (1 << 0)


###########################################################################
# Log functions
###########################################################################
def log(domain, level, message):
    if domain in registry:
        registry[domain].log(domain, level, message)
    else:
        registry[None].log(domain, level, message)



def log_fatal(message, domain=None):
    log(domain, FATAL, message)


def log_error(message, domain=None):
    log(domain, ERROR, message)


def log_warning(message, domain=None):
    log(domain, WARNING, message)


def log_info(message, domain=None):
    log(domain, INFO, message)


def log_debug(message, domain=None):
    log(domain, DEBUG, message)


###########################################################################
# Loggers
###########################################################################
registry = {}


def register_logger(logger, *args):
    for domain in args:
        registry[domain] = logger


class Logger(object):

    def __init__(self, log_file=None, min_level=INFO):
        self.log_file = log_file
        self.min_level = min_level


    def format_header(self, domain, level, message):
        # <date> <host> <domain>[<pid>]: <message>
        date = strftime('%Y-%m-%d %H:%M:%S')
        host = gethostname()
        domain = domain or ''
        pid = getpid()
        header = '{0} {1} {2}[{3}]: {4}\n'
        return header.format(date, host, domain, pid, message)


    def get_body(self):
        type, value, traceback = exc_info()
        if type is None:
            return []

        return format_exception(type, value, traceback)


    def format_body(self):
        body = self.get_body()
        if not body:
            return ''
        body = ''.join([ '  %s' % x for x in body ])
        body += '\n'
        return body


    def format(self, domain, level, message):
        header = self.format_header(domain, level, message)
        body = self.format_body()
        return header + body


    def log(self, domain, level, message):
        if level < self.min_level:
            return

        message = self.format(domain, level, message)

        # Case 1: log file
        if self.log_file:
            with open(self.log_file, 'a') as log_file:
                log_file.write(message)

        # Case 2: standard output & error
        elif level & (FATAL | ERROR | WARNING):
            stderr.write(message)
        else:
            stdout.write(message)

        # Exit on fatal errors
        if level & FATAL:
            exit()


register_logger(Logger(), None)

