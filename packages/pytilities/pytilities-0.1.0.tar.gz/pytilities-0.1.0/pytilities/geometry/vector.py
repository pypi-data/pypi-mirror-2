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

import operator
import math

from pytilities.types import NumberType
from pytilities.delegation import delegated, delegator_factory
from pytilities.overloading import overloaded, Overload, Param


class _Storage(object):
    def __init__(self, x, y):
        # Can't be a string as we must avoid nastiness. Consider for example
        # what would happen when you add vectors ('1', 0) and ('0', 0), results
        # in ('10', 0)
        assert not isinstance(x, basestring)
        assert not isinstance(y, basestring)
        self.x = x
        self.y = y


# NOTE: be careful with the awesome ways python int vs float math works
# As with statically typed languages, even here 5 / 2 == 2. As values do still
# have types. So, try not to mix ints and floats.
# If you'd rather not bother casting and keeping that sort of stuff in your
# mind, I recommend adding another Vector that wraps round this one and casts
# or asserts (if you are a bit of a performance freak ^^) all input.
@delegator_factory()
class Vector(object):

    """
    2D Point/Vector

    Class fields:

        - `INFINITY`: immutable Vector of positive infinity
        - `NULL`: immutable Vector (0, 0)

    Instance methods:

        - `move_to`: Set x, y position
        - `move_by`: Move vector by x, y
        - `assign`: Assign values of other vector to this one
        - `copy`: Shallow copy
        - `normalize`: Normalize vector
        - `normalized`: Get a normalized copy of this vector
        - `dot`: Dot product
        - `cross`:
        - `reflect`:

    Instance properties:

        - `x`: Read-write, x position
        - `y`: Read-write, y position
        - `length`: Read-write, length of vector
        - `length_squared`: Read-only, length squared

    Operators:
        
        str(s)
        s == v
        s != v
        s + v
        s += v
        s - v
        s -= v
        s * n
        s *= n
        s / n
        s /= n
        -s
            self explanatory

        len(s)
            returns 2

        iter(s)
            iterates over its x and y value

        abs(s)
            returns length of vector
    """

    @staticmethod
    def __init_delegation_profiles(profiles):
        profiles['default'] |= profiles['immutable']

    def __init_xy(self, x, y):
        self.__storage = _Storage(x, y)

    def __init_storage(self, storage):
        self.__storage = storage

    @overloaded((
        Overload(__init_xy,
            Param("x", NumberType, default=0),
            Param("y", NumberType, default=0)),
        Overload(__init_storage,
            Param("storage"))))
    def __init__(self):
        """
        Constructs a 2D Vector

        Overloaded, parameters:

        :a:
            x :: float | int = 0
            y :: float | int = 0

        :b:
            storage :: object(x, y)
                an object that provides storage for the x and y values
        """
        pass

    @delegated()
    @delegated("immutable", modifiers="r")
    @property
    def x(self):
        """Read-write, x position ::float | int"""
        return self.__storage.x

    @x.setter
    def x(self, value):
        self.__storage.x = value

    @delegated()
    @delegated("immutable", modifiers="r")
    @property
    def y(self):
        """Read-write, y position ::float | int"""
        return self.__storage.y

    @y.setter
    def y(self, value):
        self.__storage.y = value

    @delegated()
    def move_to(self, x, y):
        """
        Set x, y coords

        Parameters:

            `x` :: float | int
                x position

            `y` :: float | int
                y position
        """
        self.x, self.y = x, y

    @delegated()
    def move_by(self, x, y):
        """
        Move vector by (x, y)

        Parameters:

            `x` :: float | int
                x position

            `y` :: float | int
                y position
        """
        self.x += x
        self.y += y

    @delegated()
    def assign(self, v):
        """
        Assigns the values of another vector to this vector

        v :: Vector -- the other vector
        """
        self.x = v.x
        self.y = v.y

    @delegated("immutable")
    def __str__( self ):
        return "<%s (%s,%s)>" % (self.__class__.__name__,
                                 self.x, self.y)

    @delegated("immutable")
    def __copy__(self):
        return Vector(self.x, self.y)

    @delegated("immutable")
    def copy(self):
        """Returns shallow copy :: Vector"""
        return self.__copy__()

    @delegated("immutable")
    def __eq__(self, other):
        """other :: Vector"""
        return self.x == other.x and \
               self.y == other.y

    @delegated("immutable")
    def __neq__(self, other):
        """other :: Vector"""
        return not self.__eq__(other)

    @delegated("immutable")
    def __len__(self):
        return 2

    @delegated("immutable")
    def __getitem__(self, key):
        return (self.x, self.y)[key]

    @delegated()
    def __setitem__(self, key, value):
        (self.x, self.y)[key] = value

    @delegated("immutable")
    def __iter__(self):
        """Iterates over its x and y value"""
        return iter((self.x, self.y))

    @delegated("immutable")
    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y)['xy'.index(c)] \
                          for c in name])
        except ValueError:
            raise AttributeError, name

    @delegated("immutable")
    def __add__(self, other):
        """other :: Vector"""
        v = self.copy()
        v += other
        return v

    @delegated()
    def __iadd__(self, other):
        """other :: Vector"""
        self.x += other.x
        self.y += other.y
        return self

    @delegated("immutable")
    def __sub__(self, other):
        return self + (-other)

    @delegated("immutable")
    def __mul__(self, other):
        """other :: number"""
        v = self.copy()
        v *= other
        return v

    @delegated("immutable")
    def __rmul__(self, other):
        """other :: number"""
        return self * other

    @delegated()
    def __imul__(self, other):
        """other :: number"""
        self.x *= other
        self.y *= other
        return self

    @delegated("immutable")
    def __div__(self, other):
        """other :: number"""
        return Vector(operator.div(self.x, other),
                       operator.div(self.y, other))

    @delegated("immutable")
    def __rdiv__(self, other):
        """other :: number"""
        return Vector(operator.div(other, self.x),
                       operator.div(other, self.y))

    @delegated("immutable")
    def __floordiv__(self, other):
        """other :: number"""
        return Vector(operator.floordiv(self.x, other),
                       operator.floordiv(self.y, other))

    @delegated("immutable")
    def __rfloordiv__(self, other):
        """other :: number"""
        return Vector(operator.floordiv(other, self.x),
                       operator.floordiv(other, self.y))

    @delegated("immutable")
    def __truediv__(self, other):
        """other :: number"""
        return Vector(operator.truediv(self.x, other),
                       operator.truediv(self.y, other))


    @delegated("immutable")
    def __rtruediv__(self, other):
        """other :: number"""
        return Vector(operator.truediv(other, self.x),
                       operator.truediv(other, self.y))
    
    @delegated("immutable")
    def __neg__(self):
        return Vector(-self.x, -self.y)

    @delegated("immutable")
    def __pos__(self):
        return self.copy()
    
    @delegated("immutable")
    def __abs__(self):
        return math.sqrt(self.x ** 2 + \
                         self.y ** 2)

    @delegated()
    @property
    def length(self):
        """
        Read-write, length of vector

        Returns :: float | int

        Set parameters:

            value :: number
                new length
        """
        return abs(self)

    @length.setter
    def length(self, value):
        d = self.length * value
        self *= value

    @delegated("immutable")
    @property
    def length_squared(self):
        """Read-only, length squared :: float | int"""
        return self.x ** 2 + \
               self.y ** 2

    @delegated()
    def normalize(self):
        """
        Normalize vector
        
        Returns :: Vector
        """
        d = self.length

        if d:
            self /= d

        return self

    @delegated("immutable")
    def normalized(self):
        """
        Get a normalized copy of this vector

        Returns :: Vector
        """
        v = self.copy()
        return v.normalize()

    @delegated("immutable")
    def dot(self, other):
        """
        Get the dot product of this vector with `other`

        Parameters:

            `other` :: Vector
                the other vector

        Returns :: float | int
        """
        return self.x * other.x + \
               self.y * other.y

    @delegated("immutable")
    def cross(self):
        # TODO: doc this ya lazy git
        return Vector(self.y, -self.x)

    @delegated("immutable")
    def reflect(self, normal):
        # TODO: doc this ya lazy git
        # assume normal is normalized
        d = 2 * (self.x * normal.x + self.y * normal.y)
        return Vector(self.x - d * normal.x,
                       self.y - d * normal.y)



from .immutablevector import ImmutableVector

Vector.INFINITY = ImmutableVector(Vector(float("inf"), float("inf")))
Vector.NULL = ImmutableVector(Vector(0, 0)) # saves us some vector spawning

