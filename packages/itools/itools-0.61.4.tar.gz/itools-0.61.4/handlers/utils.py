# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Juan David Ibáñez Palomar <jdavid@itaapy.com>
# Copyright (C) 2008 Hervé Cauwelier <herve@itaapy.com>
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


src = (ur"""ÄÅÁÀÂÃĀäåáàâãāÇçÉÈÊËĒéèêëēÍÌÎÏĪíìîïīÑñÖÓÒÔÕØŌöóòôõøōÜÚÙÛŪüúùûū"""
       ur"""ÝŸȲýÿȳŽž""")
dst = (ur"""AAAAAAAaaaaaaaCcEEEEEeeeeeIIIIIiiiiiNnOOOOOOOoooooooUUUUUuuuuu"""
       ur"""YYYyyyZz""")

transmap = {}
for i in range(len(src)):
    a, b = src[i], dst[i]
    transmap[ord(a)] = ord(b)
transmap[ord(u'æ')] = u'ae'
transmap[ord(u'Æ')] = u'AE'
transmap[ord(u'œ')] = u'oe'
transmap[ord(u'Œ')] = u'OE'
transmap[ord(u'ß')] = u'ss'


def checkid(id):
    """Turn a bytestring or unicode into an identifier only composed of
    alphanumerical characters and a limited list of signs.

    It only supports Latin-based alphabets.
    """
    if isinstance(id, str):
        id = unicode(id, 'utf8')

    # Strip diacritics
    id = id.strip().translate(transmap)

    # Check for unallowed characters
    allowed_characters = set([u'.', u'-', u'_', u'@'])
    id = [ (c.isalnum() or c in allowed_characters) and c or u'-' for c in id ]

    # Merge hyphens
    id = u''.join(id)
    id = id.split(u'-')
    id = u'-'.join([x for x in id if x])
    id = id.strip('-')

    # Check wether the id is empty
    if len(id) == 0:
        return None

    # No mixed case
    id = id.lower()
    # Most FS are limited in 255 chars per name
    # (keep space for ".metadata" extension)
    id = id[:246]
    # Return a safe ASCII bytestring
    return str(id)
