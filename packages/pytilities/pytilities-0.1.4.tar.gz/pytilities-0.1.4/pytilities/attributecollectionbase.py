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

class AttributeCollectionBase(object):
    """
    Mixin, allows extension of instance attributes with `AttributeCollection`s

    This mixin allows a class' instances' attributes and set of supported
    operators to be extended with `AttributeCollection`s.

    Note: this class provides a base for using `AttributeCollection`s, it is not
    a base class of `AttributeCollection`. This have been a misnomer.

    Methods:

        - `_append_attribute_collection`: Append a new `AttributeCollection`
        
    Class invariants:

        1. an `AttributeCollectionBase` never contains two identical
        `AttributeCollection`s
    """

    def __init__(self):
        object.__setattr__(self,
                "_AttributeCollectionBase__collections", [])

    def _append_attribute_collection(self, collection):
        """
        Append a new `AttributeCollection`.
        
        When attributes of collections overlap, the first of overlapping
        attributes found in the lookup process is used and the others are
        ignored. Lookup happens in the same order as collections were added. (It
        is probably best to avoid overlaps.)

        Parameters:

            collection :: AttributeCollection
                the collection to add
        """
        assert collection not in self.__collections, \
            "Collection can appear only once in the list of collections of" + \
            "the attribute collection base"

        self.__collections.append(collection)

    def __getattr__(self, name):
        # NOTE: if you're getting exceptions about this, you probably still
        # need to call __init__
        collections = object.__getattribute__(self,
                                              "_AttributeCollectionBase__collections")
        for collection in collections: 
            (found, value) = collection.getattr_(name)
            if found: return value

        # reaching this point means no collection contains the attrib
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (object.__getattribute__(self, "__class__").__name__, name))

    def __setattr__(self, name, value):
        try:
            for collection in self.__collections:
                found = collection.setattr_(name, value)
                if found: return
        except AttributeError:
            # caused by our init not having been called yet
            # this can happen when C inherits from A, B and B inherits from us
            # thus self.__collections doesn't exist yet
            # or we are createing __colections for the first time
            pass

        # reaching this point means no collection contains the attrib
        # let object take care of this one
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        try:
            for collection in self.__collections:
                found = collection.detattr_(name)
                if found: return
        except AttributeError:
            # see __setattr__
            pass

        # reaching this point means no collection contains the attrib
        # let object take care of this one
        object.__delattr__(self, name)


    ########################################################################
    # A big bunch of things aren't searched for on the instance, but on the
    # class Thus, they don't call __getattr__, __getattribute__, ... We'll just
    # 'fix' that by placing them on our class and routing them through to the
    # __getattr__ methods etc.

    def __str__(self):
        return self.__getattr__("__str__")()

    def __copy__(self):
        return self.__getattr__("__copy__")()

    def __eq__(self, other):
        return self.__getattr__("__eq__")(other)

    def __neq__(self, other):
        return self.__getattr__("__neq__")(other)

    def __nonzero__(self):
        try:
            return self.__getattr__("__nonzero__")()
        except AttributeError:
            return True  # the default behaviour

    def __len__(self):
        return self.__getattr__("__len__")()

    def __getitem__(self, key):
        return self.__getattr__("__getitem__")(key)

    def __setitem__(self, key, value):
        self.__getattr__("__setitem__")(key, value)

    def __iter__(self):
        return self.__getattr__("__iter__")()

    def __add__(self, other):
        return self.__getattr__("__add__")(other)

    def __iadd__(self, other):
        return self.__getattr__("__iadd__")(other)

    def __sub__(self, other):
        return self.__getattr__("__sub__")(other)

    def __mul__(self, other):
        return self.__getattr__("__mul__")(other)

    def __rmul__(self, other):
        return self.__getattr__("__rmul__")(other)

    def __imul__(self, other):
        return self.__getattr__("__imul__")(other)

    def __div__(self, other):
        return self.__getattr__("__div__")(other)

    def __rdiv__(self, other):
        return self.__getattr__("__rdiv__")(other)

    def __floordiv__(self, other):
        return self.__getattr__("__floordiv__")(other)

    def __rfloordiv__(self, other):
        return self.__getattr__("__rfloordiv__")(other)

    def __truediv__(self, other):
        return self.__getattr__("__truediv__")(other)

    def __rtruediv__(self, other):
        return self.__getattr__("__rtruediv__")(other)

    def __neg__(self):
        return self.__getattr__("__neg__")()

    def __pos__(self):
        return self.__getattr__("__pos__")()

    def __abs__(self):
        return self.__getattr__("__abs__")()

# TODO: test all ops for the expected fail, just like with an object, for
# unimplemented ops

