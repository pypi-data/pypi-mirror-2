# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lang.translit
    Library for transliteration into latin symbols.
    Last changed on 2010-05-29 00:41:07+11:00 rev. 249:c664b92c9e32 by Dan Kluev <dan@kluev.name>

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
import sys
import os
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
