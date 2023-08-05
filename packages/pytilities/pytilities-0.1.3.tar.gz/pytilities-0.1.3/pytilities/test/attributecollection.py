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

from ..attributecollectionbase import AttributeCollectionBase

class A(object):
    def __init__(self):
        self.__x = 5

    def get(self):
        return self.__x

class B(AttributeCollectionBase, A):
    def __init__(self):
        AttributeCollectionBase.__init__(self)
        A.__init__(self)
        self.y = 4

class C(object):
    def __init__(self):
        self.z = 3

class D(C, B):
    def __init__(self):
        C.__init__(self)
        B.__init__(self)

class DisturbanceTestCase(unittest.TestCase):
    """Test whether or not basic inheritance is left unharmed by
    AttributeCollectionBase
    """

    def test_direct_subclass(self):
        """A class that inherits from attrib base and another class
        """
        b = B()
        self.assertEquals(b.get(), 5)

        b.x = 3
        self.assertEquals(b.x, 3)

    def test_derived(self):
        """A class that inherits from a class that inherits from attrib base
        and another class
        """
        d = D()

        self.assertEquals(d.z, 3)
        self.assertEquals(d.y, 4)

        self.assertEquals(d.get(), 5)

        d.x = 3
        self.assertEquals(d.x, 3)

def run():
    unittest.main(__name__)

