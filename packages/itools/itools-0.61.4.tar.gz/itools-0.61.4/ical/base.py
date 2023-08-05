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
from datetime import datetime

# Import from itools
from itools.csv import property_to_str
from itools.datatypes import Unicode



class BaseCalendar(object):
    """Base class for the different calendar formats.
    """

    def generate_uid(self, c_type='UNKNOWN'):
        """Generate a uid based on c_type and current datetime.
        """
        return ' '.join([c_type, datetime.now().isoformat()])


    def encode_inner_components(self, name, property_values, encoding='utf-8'):
        lines = []
        for property_value in property_values:
            record = self.get_record(property_value.value)
            if record is not None:
                seq = 0
                c_type = record.type
                for version in record:
                    line = 'BEGIN:%s\n' % c_type
                    lines.append(Unicode.encode(line))
                    # Properties
                    names = version.keys()
                    names.sort()
                    for name in names:
                        if name in ('id', 'ts', 'type'):
                            continue
                        elif name == 'DTSTAMP':
                            value = version['ts']
                        else:
                            value = version[name]
                        if name == 'SEQUENCE':
                            value.value += seq
                        else:
                            name = name.upper()
                            line = self.encode_property(name, value)
                        lines.extend(line)
                    line = 'END:%s\n' % c_type
                    lines.append(Unicode.encode(line))
                    seq += 1
        return lines


    def encode_property(self, name, property_values, encoding='utf-8'):
        if type(property_values) is not list:
            property_values = [property_values]

        datatype = self.get_record_datatype(name)
        return [
            property_to_str(name, x, datatype, {}, encoding)
            for x in property_values ]

