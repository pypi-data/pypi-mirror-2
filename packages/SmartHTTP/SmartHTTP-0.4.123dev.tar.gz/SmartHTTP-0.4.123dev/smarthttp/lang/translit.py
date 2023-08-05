# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lang.translit
    Library for transliteration into latin symbols.
    Last changed on Wed Apr 14 14:50:37 2010 +1100 rev. 111:5efdacc70dde by Dan Kluev <orion@ssorion.info>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging
import sys, os
from smarthttp.lang import split_by_unicode_blocks
log = logging.getLogger(__name__)

translist = open(os.path.join(os.path.dirname(__file__), 'translit.txt')).read().decode('utf-8').split('\n')
transmap = {}
for r in translist:
    if r and r[0] != '#':
        row = r.strip().split()
        if len(row) > 1:
            if len(row) > 2:
                transmap[row[0]] = (row[1], row[2])
            else:
                transmap[row[0]] = (row[1], None)

def transliterate(text):
    trans = []
    parts = split_by_unicode_blocks(text)
    for part in parts:
        i = 0
        while i < len(part[0]):
            c = part[0][i]
            t = None
            if i+1 < len(part[0]):
                p = part[0][i:i+2]
                t = transmap.get(p, None)
                if t:
                    i += 1
            if not t:
                t = transmap.get(c, (c, None))
            if len(part[0]) > 1 and t[1]:
                trans.append(t[1])
            else:
                trans.append(t[0])
            i += 1
    return u''.join(trans)

if __name__ == '__main__':
    print sys.argv[1]
    txt = sys.argv[1]
    if type(txt) == str:
        txt = unicode(txt, 'utf-8')
    print transliterate(txt)
