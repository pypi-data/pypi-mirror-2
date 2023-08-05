# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lang
    Language detection utilities.
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
log = logging.getLogger(__name__)

block_lines = map(lambda x:x.split(';'), open(os.path.join(os.path.dirname(__file__), 'unicode_blocks.txt')).read().split('\n'))
blocks = []
supersets = {'basic latin':'latin',
             'latin-1 supplement':'latin',
             'latin extended-a':'latin',
             'general punctuation':'common',
             'miscellaneous symbols':'common',
             'miscellaneous technical':'common',
             'letterlike symbols':'common',
             'greek and coptic':'greek',
             'cjk unified ideographs':'cjk',
             'hiragana':'cjk',
             'katakana':'cjk',
             'cyrillic':'cyrillic',
             }
for l in block_lines:
    if l[0]:
        block = l[1].strip().lower()
        r = l[0].split('..')
        upper = int(r[1], 16)
        blocks.append((upper, block))

def find_block(c):
    i = ord(c)
    for b in blocks:
        if i <= b[0]:
            return b[1]
    return None

def find_superset(c):
    b = find_block(c)
    return supersets.get(b, b)

def get_unicode_blocks(text, full=False):
    def find_block(c):
        i = ord(c)
        for b in blocks:
            if i <= b[0]:
                return b[1]
        return None
    
    def add_block(b, c):
        block = find_block(c)
        block = supersets.get(block, block)
        if not block in b:
            b.append(block)
            
    if type(text) == str:
        text = unicode(text, 'utf-8')
    tokens = text.split()
    text_blocks = []
    for t in tokens:
        if full:
            for k in range(len(t)):
                add_block(text_blocks, t[k])
        else:
            add_block(text_blocks, t[0])
    return text_blocks

def split_by_unicode_blocks(text):
    if type(text) == str:
        text = unicode(text, 'utf-8')

    parts = []
    current = []
    prev_block = find_superset(text[0])
    for k in range(len(text)):
        block = find_superset(text[k])
        if prev_block != block:
            parts.append((''.join(current), prev_block))
            current = []
        current.append(text[k])
        prev_block = block
    if current:
        parts.append((''.join(current), prev_block))
    return parts

def is_latin(text):
    if not text:
        return True
    blocks = get_unicode_blocks(text)
    if blocks.count('latin'):
        blocks.remove('latin')
    if blocks.count('common'):
        blocks.remove('common')
    if blocks:
        return False
    else:
        return True

if __name__ == '__main__':
    print sys.argv[1]
    txt = sys.argv[1]
    print get_unicode_blocks(txt, True)
    print is_latin(txt)
    print split_by_unicode_blocks(txt)
