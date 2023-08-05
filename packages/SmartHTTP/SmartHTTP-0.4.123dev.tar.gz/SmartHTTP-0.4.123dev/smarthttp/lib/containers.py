# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lib.containers
    Custom container implementations.
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
log = logging.getLogger(__name__)

class SmartDictException(Exception):
    pass

class SmartDict(dict):
    _internal = ['_internal', '_default', '_dict', '_join', '_clean_false', '_merge', '__getitem__', '__setitem__', '__getattribute__', '__setattr__', 'keys']
    _default = None
    _dict    = None
    def __init__(self, value=None, default=None):
        if type(value) == dict:
            self._dict = value
        else:
            self._dict = {}
        self._default = default

    def _join(self, d):
        """
        Overwrite local dict with provided dict on matches
        """
        _dict = self._dict
        for key in d:
            _dict[key] = d[key]
        return self

    def _merge(self, d):
        """
        For all keys present in both dicts, try to join values together
        """
        _dict = self._dict
        if type(d) == SmartDict:
            d = d._dict
        if type(d) != dict:
            raise SmartDictException('It is possible to merge dicts only, got {0}.'.format(type(d)))
        for k in d:
            if k in _dict:
                merger = MergeMatrix[type(_dict[k])][type(d[k])]
                if not merger:
                    raise SmartDictException('Cannot merge {0} and {1} for key {2}'.format(type(_dict[k]), type(d[k]), k))
                else:
                    _dict[k] = merger(_dict[k], d[k])
            else:
                _dict[k] = d[k]
        return self

    def _clean_false(self):
        """
        Delete all elements which evaluate as False
        """
        _dict = self._dict
        for key in _dict.keys():
            if bool(_dict[key]) == False:
                del _dict[key]

    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        _dict = self._dict
        if not item in _dict:
            _default = self._default
            if type(_default) == type:
                _dict[item] = _default()
            else:
                _dict[item] = _default
        return _dict[item]
    def __setitem__(self, item, value):
        self._dict.__setitem__(item, value)
        
    def __getattribute__(self, item):
        _internal = object.__getattribute__(self, '_internal')
        if item in _internal or (item.startswith('__') and item.endswith('__')):
            return object.__getattribute__(self, item)
        else:
            return self[item]
    def __setattr__(self, item, value):
        _internal = object.__getattribute__(self, '_internal')
        if item in _internal:
            return object.__setattr__(self, item, value)
        else:
            return self.__setitem__(item, value)
    def __add__(self, b):
        if b:
            return self._join(b)
        else:
            return self
    
    def __bool__(self):
        return bool(self._dict)
    
    def __nonzero__(self):
        return bool(self._dict)
        
    def __repr__(self):
        return self._dict.__repr__()

def join_dicts(d1, d2):
    for k in d2:
        d1[k] = d2[k]
    return d1

MergeMatrix = SmartDict({
    list:SmartDict({
        list:lambda x,y: x+y,
        set:lambda x,y: y.union(x)
        }),
    set:SmartDict({
        list:lambda x,y: x.union(y),
        set:lambda x,y: x.union(y)
        }),
    dict:SmartDict({
        dict: join_dicts,
        SmartDict: lambda x,y: y._merge(x)
        }),
    SmartDict:SmartDict({
        dict: lambda x,y: x._merge(y),
        SmartDict: lambda x,y: x._merge(y)
    })}, SmartDict)

def strdict(d):
    """
    Turn all keys into str
    >>> set(strdict({u'uni':0, 'str':0, 1:0}).keys()) == set(['uni', 'str', '1'])
    True
    """
    nd = {}
    for k in d:
        v = d[k]
        nd[str(k)] = v
    return nd
