# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lib.containers
    Custom containers
    Last changed on 2010-05-22 15:30:30+11:00 rev. 231:3ff967091986 by Dan Kluev <orion@ssorion.info>

..
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


Custom containers
=================

.. _smarthttp.lib.containers-SmartDictException:

:class:`SmartDictException`
---------------------------



.. autoclass:: SmartDictException
    :members:
    :undoc-members:

.. _smarthttp.lib.containers-SmartDict:

:class:`SmartDict`
------------------


    >>> d = SmartDict(default=3, a=1, b=2)
    >>> d.c
    3
    >>> d.a
    1
    >>> d['a']
    1
    >>> d['d']
    3
    >>> d['d'] = 4
    >>> d['d']
    4
    >>> d.e = 5
    >>> d.e
    5
    >>> SmartDict(default=set, a=1, b=2).c
    set([])
    

.. autoclass:: SmartDict
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'
from ..asserts import DictAssertMixIn
import logging
log = logging.getLogger(__name__)

class SmartDictException(Exception):
    pass

class SmartDict(dict, DictAssertMixIn):
    """
    >>> d = SmartDict(default=3, a=1, b=2)
    >>> d.c
    3
    >>> d.a
    1
    >>> d['a']
    1
    >>> d['d']
    3
    >>> d['d'] = 4
    >>> d['d']
    4
    >>> d.e = 5
    >>> d.e
    5
    >>> SmartDict(default=set, a=1, b=2).c
    set([])
    """
    _internal = frozenset(['_internal', '_hash', '_strict_check', '_propagate',\
                '_get_default', '_default', '_clean_false', '_merge',\
                '__getitem__', '__setitem__', '__getattribute__', '__setattr__',\
                'keys', 'values', 'iteritems', 'update', 'get'])
    _default = None
    _dict    = None
    _hash    = None
    _strict_check = False
    _propagate    = False
    def __init__(self, value=None, default=None, _hash=None, _strict_check=False, _propagate=False, **kw):
        """
        `_hash` - value to use for hashing
        `_strict_check` - if `True`, actually check content for `in` operator
        `_propagate` - if `True`, return dicts wrapped in `SmartDict` with same params
        """
        if isinstance(value, dict):
            dict.update(self, value)
        self._default = default
        if kw:
            dict.update(self, kw)
        if _hash:
            self._hash = _hash
            
        self._strict_check = _strict_check
        self._propagate    = _propagate

    def _get_default(self):
        _default = self._default
        if type(_default) == type:
            val = _default()
        else:
            val = _default
        return val

    def _merge(self, d, overwrite=False):
        """
        For all keys present in both dicts, try to join values together
        """
        if not isinstance(d, dict):
            raise SmartDictException('It is possible to merge dicts only, got {0}.'.format(type(d)))
        for k, v2 in d.iteritems():
            if dict.__contains__(self, k):
                v = dict.__getitem__(self, k)
                merger = MergeMatrix[type(v)][type(v2)]
                if not merger:
                    if overwrite:
                        dict.__setitem__(self, k, v2)
                    else:
                        raise SmartDictException('Cannot merge {0} and {1} for key {2}'.format(type(v), type(v2), k))
                else:
                    dict.__setitem__(self, k, merger(v, v2))
            else:
                dict.__setitem__(self, k, v2)
        return self

    def _clean_false(self):
        """
        Delete all elements which evaluate as False
        """
        for key in dict.keys(self):
            if bool(dict.__getitem__(self, key)) is False:
                dict.__delitem__(self, key)

    def __contains__(self, item):
        """
        if _strict_check is True, we should actually bother to check
        """
        if self._strict_check:
            return dict.__contains__(self, item)
        else:
            return True
        
    def __getitem__(self, item):
        if not dict.__contains__(self, item):
            dict.__setitem__(self, item, self._get_default())
        res = dict.__getitem__(self, item)
        if type(res) == dict and self._propagate:
            return SmartDict(res, default=self._default, _strict_check=self._strict_check, _propagate=True)
        else:
            return res
        
    def __getattribute__(self, item):
        _internal = object.__getattribute__(self, '_internal')
        if item in _internal or (item.startswith('__') and item.endswith('__')) or item.startswith('assert'):
            return object.__getattribute__(self, item)
        else:
            return object.__getattribute__(self, '__getitem__')(item)
        
    def __setattr__(self, item, value):
        _internal = object.__getattribute__(self, '_internal')
        if item in _internal:
            return object.__setattr__(self, item, value)
        else:
            return self.__setitem__(item, value)
        
    def __add__(self, b):
        if b:
            return self._merge(b, True)
        else:
            return self
    
    def __bool__(self):
        return bool(self._dict)
    
    def __nonzero__(self):
        return bool(self._dict)
        
    def __repr__(self):
        l = []
        for k, v in dict.iteritems(self):
            if isinstance(v, dict):
                vs = u'{...}'
            elif isinstance(v, list):
                vs = u'[...]'
            elif isinstance(v, tuple):
                vs = u'(...)'
            elif isinstance(v, set):
                vs = u'set(...)'
            else:
                vs = v.__repr__()
            l.append(u"{0}={1}".format(k, vs))
        return u"<SmartDict({1})>".format(self, u', '.join(l))

    def __hash__(self):
        if self._hash:
            return hash(self._hash)
        else:
            raise TypeError('Unnamed SmarDict is unhashable')

    def update(self, *args, **kw):
        dict.update(self, *args, **kw)
        return self
    
    def get(self, item, val=None):
        if dict.__contains__(self, item):
            return dict.__getitem__(self, item)
        elif not val is None:
            return val
        else:
            return self._get_default()

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
        SmartDict: lambda x,y: y._merge(x, True)
        }),
    SmartDict:SmartDict({
        dict: lambda x,y: x._merge(y),
        SmartDict: lambda x,y: x._merge(y, True)
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
