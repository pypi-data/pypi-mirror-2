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

from pytilities import mangle
from . import Vector

class _DelegatedStorage(object):
    def __init__(self, target, x_attribute, y_attribute):
        self.__target = target
        self.__x_name = mangle(target, x_attribute)
        self.__y_name = mangle(target, y_attribute)

    @property
    def x(self):
        return getattr(self.__target, self.__x_name)

    @x.setter
    def x(self, value):
        return setattr(self.__target, self.__x_name, value)

    @property
    def y(self):
        return getattr(self.__target, self.__y_name)

    @y.setter
    def y(self, value):
        return setattr(self.__target, self.__y_name, value)


class BoundVector(Vector):

    """
    `Vector` whose x and y values are stored elsewhere.

    Put differently, it creates a vector view of an x and a y value.

    For `Vector` specific documentation, see `Vector`.
    """

    def __init__(self, target, x_attribute, y_attribute):
        """
        Construct a `BoundVector`

        X and y attributes will be looked up on `target` with names
        `x_attribute` and `y_attribute`.

        Parameters:

            target
                the object to bind to. The object on which the x and y
                attributes reside.

            x_attribute :: string
                name of attribute of the x value on the target

            y_attribute :: string
                name of attribute of the y value on the target
        """
        assert(isinstance(x_attribute, basestring))
        assert(isinstance(y_attribute, basestring))

        Vector.__init__(self, _DelegatedStorage(target, 
                                                x_attribute,
                                                y_attribute))

