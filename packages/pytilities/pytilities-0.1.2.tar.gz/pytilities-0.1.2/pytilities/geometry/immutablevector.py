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

from pytilities import AttributeCollectionBase
from .vector import Vector

class ImmutableVector(AttributeCollectionBase):

    """
    `Vector` wrapper that makes the vector immutable.
    
    It supports all immutable attributes of `Vector`. All tries to mutate the
    vector will result in exceptions.

    For `Vector` specific documentation, see `Vector`.
    """

    def __init__(self, v):
        """v:Vector -- the vector to wrap
        """
        AttributeCollectionBase.__init__(self)

        self.__v = v

        # delegate to wrapped object
        delegator = Vector.Delegator("immutable", v)
        self._append_attribute_collection(delegator)

    @property
    def x(self):
        return self.__v.x

    @x.setter
    def x(self, value):
        assert False, "Tried to modify an immutable vector"

    @property
    def y(self):
        return self.__v.y

    @y.setter
    def y(self, value):
        assert False, "Tried to modify an immutable vector"

    @property
    def length(self):
        return abs(self)

    @length.setter
    def length(self, value):
        assert False, "Tried to modify an immutable vector"

    def move_to(self, *args):
        assert False, "Tried to modify an immutable vector"

    def move_by(self, *args):
        assert False, "Tried to modify an immutable vector"

    def assign(self, v):
        assert False, "Tried to modify an immutable vector"

    def normalize(self):
        assert False, "Tried to modify an immutable vector"

    def __isub__(self, other):
        assert False, "Tried to modify an immutable vector"

    def __idiv__(self, other):
        assert False, "Tried to modify an immutable vector"

    def __iadd__(self, other):
        assert False, "Tried to modify an immutable vector"

    def __imul__(self, other):
        assert False, "Tried to modify an immutable vector"

