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
from pytilities.delegation import Delegator
from .verbosevector import VerboseVector

@event.dispatcher("size_changed")
class VerboseRectangle(AttributeCollectionBase):

    """
    A `Rectangle` wrapper that sends out events

    It supports all attributes of `Rectangle`. For `Rectangle` specific
    documentation, see `Rectangle`.

    Events:

        size_changed
            Parameters:

                `old_size` :: Vector
                    the old size
    """

    def __init__(self, r):
        """
        Construct a `VerboseRectangle`.
        
        Parameters:
            r :: Rectangle
                the rectangle to wrap
        """
        AttributeCollectionBase.__init__(self)

        self.__r = r

        self.__top_left = VerboseVector(self.__r.top_left)
        self.__top_right = VerboseVector(self.__r.top_right)
        self.__bottom_left = VerboseVector(self.__r.bottom_left)
        self.__bottom_right = VerboseVector(self.__r.bottom_right)

        # delegate to wrapped object
        delegator = Delegator()
        delegator.target = r
        delegator.profile.add_mappings("r", *"""__copy__ copy contains overlaps move_to
                           move_by __str__ __repr__""".split())
        delegator.profile.add_mappings("rw", *"""__center_x __center_y center""".split()) 
        
        self._append_attribute_collection(delegator)

    @property
    def bounds(self):
        return self.__r.bounds

    @bounds.setter
    def bounds(self, args):
        old_size = self.size
        self.__r.bounds = args
        if old_size != self.size:
            self.__dispatch("size_changed", old_size)

    @property
    def width(self):
        return self.__r.width

    @width.setter
    def width(self, value):
        old_size = self.size
        self.__r.width = value
        if old_size != self.size:
            self.__dispatch("size_changed", old_size)

    @property
    def height(self):
        return self.__r.height

    @height.setter
    def height(self, value):
        old_size = self.size
        self.__r.height = value
        if old_size != self.size:
            self.__dispatch("size_changed", old_size)

    @property
    def size(self):
        return self.__r.size

    @size.setter
    def size(self, value):
        if self.size != value:
            old_size = self.size
            self.__r.size = value
            self.__dispatch("size_changed", old_size)

    @property
    def left(self):
        return self.__r.left

    @left.setter
    def left(self, value):
        if self.left != value:
            old_size = self.size
            self.__r.left = value
            self.__dispatch("size_changed", old_size)

    @property
    def top(self):
        return self.__r.top

    @top.setter
    def top(self, value):
        if self.top != value:
            old_size = self.size
            self.__r.top = value
            self.__dispatch("size_changed", old_size)

    @property
    def right(self):
        return self.__r.right

    @right.setter
    def right(self, value):
        if self.right != value:
            old_size = self.size
            self.__r.right = value
            self.__dispatch("size_changed", old_size)

    @property
    def bottom(self):
        return self.__r.bottom

    @bottom.setter
    def bottom(self, value):
        if self.bottom != value:
            old_size = self.size
            self.__r.bottom = value
            self.__dispatch("size_changed", old_size)

    @property
    def top_left(self):
        return self.__top_left

    @top_left.setter
    def top_left(self, value):
        self.__top_left.assign(value)

    @property
    def top_right(self):
        return self.__top_right

    @top_right.setter
    def top_right(self, value):
        self.__top_right.assign(value)

    @property
    def bottom_left(self):
        return self.__bottom_left

    @bottom_left.setter
    def bottom_left(self, value):
        self.__bottom_left.assign(value)

    @property
    def bottom_right(self):
        return self.__bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        self.__bottom_right.assign(value)

    def inflate(self, *args):
        old_size = self.size
        self.__r.inflate(*args)
        if old_size != self.size:
            self.__dispatch("size_changed", old_size)

