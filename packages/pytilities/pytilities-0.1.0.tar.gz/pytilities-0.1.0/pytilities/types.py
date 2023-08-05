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

"""
Various types

Classes:

    - `NumericType`: Represents any numeric type.
    - `NumberType`: Represents any number type.
    - `SequenceType`: Represents any ordered sequence.
    - all types from the standard types package
"""

# Normally from name, looks for .name first, in order to change this behaviour
# to just look for the absolute name we first import absolut_import from the
# future
from __future__ import absolute_import as _absolute_import

# now we can get types, rather than .types :/
from types import *

# TODO split into types dir with separate files
class NumericTypeMeta(type):
    def __instancecheck__(self, instance):
        try:
            float(instance)
            return True
        except (ValueError, TypeError):
            return False

    # inside meta classes, self refers to the class that has this meta as
    # metaclass
    def __subclasscheck__(self, subclass):
        """Note: returns false for a string as we can't tell whether it's
        numeric. Try to avoid subclass checks of numbers with strings.
        """
        if subclass is self:
            return True

        for type_ in (int, long, float):
            if issubclass(type_, subclass):
                return True

        return False

class NumericType(object):
    """
    Represents any numeric type.
    
    Numeric strings, ints (, longs) and floats are indirect instances of this
    class. Ints (, longs) and floats are subclasses of this class. Note that a
    string is not a subclass (some strings are numeric, but not all, and there
    is no numeric string type).
    """
    __metaclass__ = NumberTypeMeta

class NumberTypeMeta(type):
    def __instancecheck__(self, instance):
        issubclass(instance, self)

    # inside meta classes, self refers to the class that has this meta as
    # metaclass
    def __subclasscheck__(self, subclass):
        if subclass is self:
            return True

        for type_ in (int, long, float):
            if issubclass(type_, subclass):
                return True

        return False

class NumberType(object):
    """
    Represents any number type.
    
    Ints (, longs) and floats are subclasses of this class.
    """
    __metaclass__ = NumberTypeMeta


# TODO this is internal, make private (add _)
class SequenceTypeMeta(type):
    def __instancecheck__(self, instance):
        return issubclass(instance.__class__, self)

    # inside meta classes, self refers to the class that has this meta as
    # metaclass
    def __subclasscheck__(self, subclass):
        if subclass is self:
            return True

        for type_ in (tuple, list):
            if issubclass(type_, subclass):
                return True

        return False

class SequenceType(object):
    """
    Represents any ordered sequence.

    A sequence supports indexed access (i.e., [] access, __getitem__, ...).

    Lists and tuples are subtypes of this type.
    """
    __metaclass__ = SequenceTypeMeta

