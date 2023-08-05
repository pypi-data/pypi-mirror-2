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

from pytilities import event, AttributeCollectionBase
from .vector import Vector

@event.dispatcher("changed")
class VerboseVector(AttributeCollectionBase):

    """
    `Vector` wrapper that sends out events.

    It supports all attributes of `Vector`. For `Vector` specific
    documentation, see `Vector`.

    Events:

        changed
            x and/or y value changed

            Parameters:

                `old_tuple` :: (x, y)
                    the old x and y values
    """

    def __init__(self, v):
        """
        Construct a VerboseVector.
        
        Parameters:
            
            v :: Vector
                the vector to wrap
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
        old_tuple = self.__v.xy
        self.__v.x = value
        self.__dispatch("changed", old_tuple)

    @property
    def y(self):
        return self.__v.y

    @y.setter
    def y(self, value):
        old_tuple = self.__v.xy
        self.__v.y = value
        self.__dispatch("changed", old_tuple)

    def move_to(self, *args):
        old_tuple = self.__v.xy
        self.__v.move_to(*args)
        self.__dispatch("changed", old_tuple)

    def move_by(self, *args):
        old_tuple = self.__v.xy
        self.__v.move_by(*args)
        self.__dispatch("changed", old_tuple)

    def assign(self, v):
        old_tuple = self.__v.xy
        self.__v.assign(v)
        self.__dispatch("changed", old_tuple)

    @property
    def length(self):
        return abs(self)

    @length.setter
    def length(self, value):
        old_tuple = self.__v.xy
        self.__v.length = value
        self.__dispatch("changed", old_tuple)

    def normalize(self):
        old_tuple = self.__v.xy
        self.__v.normalize()
        self.__dispatch("changed", old_tuple)
        return self

    def __iadd__(self, other):
        old_tuple = self.__v.xy
        self.__v += other
        self.__dispatch("changed", old_tuple)
        return self

    def __imul__(self, other):
        old_tuple = self.__v.xy
        self.__v *= other
        self.__dispatch("changed", old_tuple)
        return self
    
