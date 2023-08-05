# Copyright (C) 2010 Tim Diels <limyreth@users.sourceforge.net>
# 
# This file is part of pytilities.
# 
# pytilities is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# pytilities is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pytilities.  If not, see <http://www.gnu.org/licenses/>.
#

__docformat__ = 'reStructuredText'

import unittest

from pytilities.delegation import delegator_factory, delegated
from pytilities import AttributeCollectionBase

@delegator_factory()
class A(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self._f = self._xw = None
        self._g = self._xr = False

    @delegated("public")
    def f(self, a, b, c): # func with args
        self._f = (a, b , c)

    @delegated()
    def g(self): # func withot args
        self._g = True

    @delegated(modifiers='w') # only delegate write
    @property
    def x(self):
        self._xr = True

    @x.setter
    def x(self, value):
        self._xw = value

# default extends/includes public
p = A._delegator_factory.get_profile('default')
p |= A._delegator_factory.get_profile('public') 

# some beasty that delegates only public
class Public(AttributeCollectionBase):
    def __init__(self, a):
        AttributeCollectionBase.__init__(self)
        self._append_attribute_collection(A.Delegator('public', a))

# some beasty that delegates the default
class Default(AttributeCollectionBase):
    def __init__(self, a):
        AttributeCollectionBase.__init__(self)
        self._append_attribute_collection(A.Delegator(target=a))

    @property
    def x(self):
        return 666


class MainTestCase(unittest.TestCase):
    def test_public(self):
        a = A()
        p = Public(a)

        # public
        p.f(5, None, 3)
        self.assertEquals(a._f, (5, None, 3))
        a.reset()

        self.assertRaises(AttributeError, lambda: p.g)
        self.assertRaises(AttributeError, lambda: p.x)

        # default
        d = Default(a)
        d.f(5, None, 3)
        self.assertEquals(a._f, (5, None, 3))
        a.reset()

        d.g()
        self.assert_(a._g)
        a.reset()

        d.x = 2
        self.assertEquals(a._xw, 2)
        a.reset()

        self.assertEquals(d.x, 666)

