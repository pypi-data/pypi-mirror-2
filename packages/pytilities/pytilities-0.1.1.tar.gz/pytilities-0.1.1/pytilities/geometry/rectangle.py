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

from pytilities.overloading import \
    overloaded, Overload, Param, CompositeParam
from pytilities.types import NumberType
from . import Vector, BoundVector

# NOTE: be careful with the awesome ways python int vs float math works
# As with statically typed languages, even here 5 / 2 == 2. As values do still
# have types. So, try not to mix ints and floats.
# If you'd like it to autoconvert or assert for ints/floats, go decorator in
# this class (and vector)
class Rectangle(object):

    """
    A rectangle identified by two points.

    The rectangle stores left, top, right, and bottom values.

    Coordinates are based on screen coordinates.

    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom

    Instance methods:

        - `copy`: Make a shallow copy
        - `contains`: Is a vector inside?
        - `overlaps`: Does a rectangle overlap?
        - `inflate`: grow (or shrink)
        - `move_to`: move entire rectangle to a spot
        - `move_by`: move entire rectangle by an amount

    Instance properties:

        - `bounds`: Read-write, all rectangle coordinates
        - `center`: Read-write, center of the rectangle
        - `width`: Read-write, width of the rectangle
        - `height`: Read-write, height of the rectangle
        - `size`: Read-write, size of the rectangle
        - `left`: Read-write, left edge of rectangle
        - `top`: Read-write, top edge of rectangle
        - `right`: Read-write, right edge of rectangle
        - `bottom`: Read-write, bottom edge of rectangle
        - `top_left`: Read-write, top-left corner
        - `top_right`: Read-write, top-right corner
        - `bottom_left`: Read-write, bottom-left corner
        - `bottom_right`: Read-write, bottom-right corner

    Operators:

        str(s)
        repr(s)
    """

    def __init__(self, *args):
        """
        Construct a rectangle.
        
        Overloaded, parameters:

        :a:
            `left` :: float | int
            `top` :: float | int
            `right` :: float | int
            `bottom` :: float | int

        :b:
            `top_left` :: Vector
            `bottom_right` :: Vector
        """

        self.bounds = args

        self.__size = BoundVector(
            self, "width", "height")

        self.__center = BoundVector(
            self, "__center_x", "__center_y")

        self.__top_left = BoundVector(
            self, "left", "top")
        
        self.__top_right = BoundVector(
            self, "right", "top")

        self.__bottom_left = BoundVector(
            self, "left", "bottom")

        self.__bottom_right = BoundVector(
            self, "right", "bottom")

    def __copy__(self):
        return Rectangle(*(self.bounds))

    def copy(self):
        """Returns shallow copy"""
        return self.__copy__

    @property
    def bounds(self):
        """Read-write, all rectangle coordinates
        
        Returns (left, top, right, bottom)

        Overloaded, set parameters:

        :a:
            `left` :: float | int
            `top` :: float | int
            `right` :: float | int
            `bottom` :: float | int

        :b:
            `top_left` :: Vector
            `bottom_right` :: Vector
        """
        return (self.left, self.top, self.right, self.bottom)

    def __set_bounds_numbers(self, left, top, right, bottom):
        (self.left, self.top, self.right, self.bottom) = \
            (left, top, right, bottom)

        assert self.left < self.right, \
            "given top_left isn't the top left corner"
        assert self.top < self.bottom, \
            "given top_left isn't the top left corner"

    def __set_bounds_points(self, top_left, bottom_right):
        (self.left, self.top) = top_left.xy
        (self.right, self.bottom) = bottom_right.xy

        assert self.left < self.right, \
            "given top_left isn't the top left corner"
        assert self.top < self.bottom, \
            "given top_left isn't the top left corner"

    @bounds.setter
    @overloaded((
        Overload(__set_bounds_numbers,
            CompositeParam("args", (
                Param("left", NumberType),
                Param("top", NumberType),
                Param("right", NumberType),
                Param("bottom", NumberType)))),
        Overload(__set_bounds_points,
            CompositeParam("args", (
                Param("top_left"),
                Param("bottom_right"))))))
    def bounds(self):
        pass

    @property
    def __center_x(self):
        return (self.left + self.right) / 2

    @__center_x.setter
    def __center_x(self, value):
        cx = self.size.x
        self.left = value - cx/2
        self.right = self.left + cx  # this way we maintain our size

    @property
    def __center_y(self):
        return (self.top + self.bottom) / 2

    @__center_y.setter
    def __center_y(self, value):
        cy = self.size.y
        self.top = value - cy/2
        self.bottom = self.top + cy  # this way we maintain our size

    @property
    def center(self):
        """
        Read-write, center of the rectangle :: bound Vector

        Changing the center does not change the size.
        """
        return self.__center

    @center.setter
    def center(self, v):
        self.__center.assign(v)

    @property
    def width(self):
        """Read-write, width of the rectangle :: float | int"""
        return self.right - self.left

    @width.setter
    def width(self, value):
        self.right = self.left + value
        
    @property
    def height(self):
        """Read-write, height of the rectangle :: float | int"""
        return self.bottom - self.top

    @height.setter
    def height(self, value):
        self.bottom = self.top + value
        
    @property
    def size(self):
        """Read-write, size of the rectangle :: bound Vector"""
        return self.__size

    @size.setter
    def size(self, value):
        self.__size.assign(value)
        
    @property
    def left(self):
        """Read-write, left edge of rectangle :: float | int"""
        return self.__left

    @left.setter
    def left(self, value):
        self.__left = value
        
    @property
    def top(self):
        """Read-write, top edge of rectangle :: float | int"""
        return self.__top

    @top.setter
    def top(self, value):
        self.__top = value
        
    @property
    def right(self):
        """Read-write, right edge of rectangle :: float | int"""
        return self.__right

    @right.setter
    def right(self, value):
        self.__right = value
        
    @property
    def bottom(self):
        """Read-write, bottom edge of rectangle :: float | int"""
        return self.__bottom

    @bottom.setter
    def bottom(self, value):
        self.__bottom = value
        
# TODO: think of way of writing bound props like size easier
# Call it @bound_property or something...

    @property
    def top_left(self):
        """Read-write, top-left corner :: bound Vector"""
        return self.__top_left

    @top_left.setter
    def top_left(self, value):
        return self.__top_left.assign(value)

    @property
    def top_right(self):
        """Read-write, top-right corner :: bound Vector"""
        return self.__top_right

    @top_right.setter
    def top_right(self, value):
        return self.__top_right.assign(value)

    @property
    def bottom_left(self):
        """Read-write, bottom-left corner :: bound Vector"""
        return self.__bottom_left

    @bottom_left.setter
    def bottom_left(self, value):
        return self.__bottom_left.assign(value)

    @property
    def bottom_right(self):
        """Read-write, bottom-right corner :: bound Vector"""
        return self.__bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        return self.__bottom_right.assign(value)

    def contains(self, v):
        """
        Returns `True` if `v` is inside the rectangle.
        
        Parameters:

            `v` :: Vector
        """
        x,y = v.xy
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def overlaps(self, rect):
        """
        Returns `True` if `rect` overlaps with this rectangle.

        Parameters:

            `rect` :: Rectangle
        """
        return (self.right > rect.left and self.left < rect.right and
                self.top < rect.bottom and self.bottom > rect.top)

    def __inflate_number(self, n):
        self.left -= n
        self.top -= n
        self.right += n
        self.bottom += n

    def __inflate_vector(self, v):
        x, y = v.xy
        self.left -= x
        self.top -= y
        self.right += x
        self.bottom += y

    @overloaded((
        Overload(__inflate_number,
                Param("n", NumberType)),
        Overload(__inflate_vector,
                Param("v"))))
    def inflate(self):
        """
        Inflate the rectangle

        Overloaded, parameters:

        :a:
            n :: number
                Extend all sides by n points
        :b:
            v :: Vector
                extend left and right sides by v.x and top and bottom sides by
                v.y
        """

    def move_to(self, v):
        """
        Move the top_left corner to `v`, without changing size

        Parameters:

            `v` :: Vector
                the spot to move to
        """
        bottom_right = v + self.size
        (self.left, self.top) = v.xy
        (self.right, self.bottom) = bottom_right.xy

    def move_by(self, v):
        """
        Move the top_left corner by `v`, without changing size

        Parameters:

            `v` :: Vector
                the amount to move by
        """
        self.left += v.x
        self.right += v.x
        self.top += v.y
        self.bottom += v.y

    def __str__( self ):
        return "<%s (%s,%s)-(%s,%s)>" % (self.__class__.__name__,
                                         self.left, self.top,
                                           self.right, self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               Vector(self.left, self.top),
                               Vector(self.right, self.bottom))

# TODO: try to write code of bound props in a more succint way (using some
# awesome lib func/decorator/class)

