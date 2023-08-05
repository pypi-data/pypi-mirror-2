#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Hervé Cauwelier <herve@itaapy.com>
# Copyright (C) 2007-2008 Juan David Ibáñez Palomar <jdavid@itaapy.com>
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

# Import from the Standard Library
from datetime import datetime
from optparse import OptionParser

# Import from itools
import itools
from itools.core import get_pipe
from itools.fs import lfs


def parse_copyright(line):
    """From a copyright line:

        Copyright (C) 2005 Toto <toto@example.com>

    Extract the email address and the years.
    """
    line = line[16:].strip()
    # Split
    for i in range(len(line)):
        c = line[i]
        if not c.isdigit() and c not in (' ', ',', '-'):
            break
    name, email = line[i:].split('<')
    line = line[:i]
    # The email
    email = email[:-1]
    # The years
    years = set()
    for year in line.split(','):
        year = year.strip()
        if '-' in year:
            start, end = year.split('-')
            years.update(range(int(start), int(end) + 1))
        else:
            years.add(int(year))

    return email, name.strip(), years




if __name__ == '__main__':
    # The command line parser
    usage = '%prog [OPTIONS] FILES'
    version = 'itools %s' % itools.__version__
    description = (
        "Modifies the copyright notice in the given FILES. Uses 'git blame'"
        " to figure out the authors.")
    parser = OptionParser(usage, version=version, description=description)
    parser.add_option('-f', '--forget', action='store_true', default=False,
        help='forget the old copyright (a more aggresive approach)')

    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error('incorrect number of arguments')

    # Load CREDITS
    credits_names = {}  # Mapping from canonical email to real full name
    credits_mails = {}  # Mapping from secondary email to canonical email
    emails = []
    if lfs.exists('CREDITS'):
        for line in lfs.open('CREDITS').readlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            if line:
                key, value = line.split(':', 1)
                value = value.lstrip()
                if key == 'N':
                    name = value
                elif key == 'E':
                    emails.append(value)
                    if len(emails) == 1:
                        credits_names[value] = name
                    else:
                        credits_mails[value] = emails[0]
            else:
                emails = []

    # Go!
    for filename in args:
        # Call "git blame"
        command = ['git', 'blame', '-p', filename]
        output = get_pipe(command)

        header = True
        authors = {}
        for line in output.splitlines():
            if line.startswith('author '):
                name = line[7:]
            elif line.startswith('author-mail '):
                email = line[13:-1]
                if email in credits_mails:
                    email = credits_mails[email]
                if email in credits_names:
                    name = credits_names[email]
            elif line.startswith('author-time '):
                year = datetime.fromtimestamp(int(line[12:])).year
            elif line.startswith('\t'):
                # Don't consider the file header (copyright, license) as code
                data = line.lstrip()
                if not data.startswith('#'):
                    header = False
                if header is False:
                    authors.setdefault(email, (name, set()))
                    authors[email][1].add(year)

        # Don't consider the email 'not.committed.yet' as a valid author email
        if 'not.committed.yet' in authors:
            del authors['not.committed.yet']

        # Keep old copyright
        if options.forget is False:
            lines = open(filename).readlines()
            n_lines = len(lines)
            i = 0
            # Skip shebang and encoding
            while i < n_lines and not lines[i].startswith('# Copyright (C) '):
                i += 1
            # Process
            while i < n_lines and lines[i].startswith('# Copyright (C) '):
                line = lines[i]
                email, name, years = parse_copyright(line)
                if email in credits_mails:
                    email = credits_mails[email]
                if email in credits_names:
                    name = credits_names[email]
                authors.setdefault(email, (name, set()))
                authors[email][1].update(years)
                i += 1

        # Format the lines
        copyright = []
        for email in authors:
            name, years = authors[email]
            years = list(years)
            years.sort()
            # Format the years ranges
            # [(year, year), year]
            aux = [years[0]]
            for year in years[1:]:
                if isinstance(aux[-1], int):
                    if aux[-1] == (year - 1):
                        aux[-1] = (aux[-1], year)
                    else:
                        aux.append(year)
                else:
                    if aux[-1][1] == (year - 1):
                        aux[-1] = (aux[-1][0], year)
                    else:
                        aux.append(year)
            # ['year-year', 'year']
            years = []
            for x in aux:
                if isinstance(x, int):
                    years.append(str(x))
                else:
                    years.append('%s-%s' % x)
            years = ', '.join(years)
            copyright.append('# Copyright (C) %s %s <%s>\n' % (years, name,
                email))
        copyright.sort()

        # Replace the old copyright by the new one
        lines = open(filename).readlines()
        n_lines = len(lines)
        i = 0
        # Skip shebang and encoding
        while i < n_lines and not lines[i].startswith('# Copyright (C) '):
            i += 1
        # No copyright found
        if i == n_lines:
            if lines[0].startswith('#!'):
                if lines[1].startswith('# -*-'):
                    # Shebang plus encoding
                    i = 2
                else:
                    # Only shebang
                    i = 1
            elif lines[0].startswith('# -*-'):
                # Only encoding
                i = 1
            else:
                # None of them
                i = 0
        # Process
        while i < n_lines and lines[i].startswith('# Copyright (C) '):
            del lines[i]
        lines = lines[:i] + copyright + lines[i:]

        # Write
        open(filename, 'w').write(''.join(lines))
