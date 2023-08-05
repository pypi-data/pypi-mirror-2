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

class Profile(object):

    """
    States what attributes to delegate, and to which target attributes.

    Instance methods:
        
        - `has_readable`: Check for read-access mapping of attribute
        - `has_writable`: Check for read-access mapping of attribute
        - `has_deletable`: Check for read-access mapping of attribute
        - `get_readable`: Get read-access mapping for attribute
        - `get_writable`: Get read-access mapping for attribute
        - `get_deletable`: Get read-access mapping for attribute
        - `remove_mappings`: Remove attribute mappings
        - `add_mappings`: Add attribute mappings

    Operators:

        self |= b::Profile
            union of this profile and the other
    """

    def __init__(self):
        self.__readables = {}
        self.__writables = {}
        self.__deletables = {}

    def has_readable(self, attribute):
        """
        Check for read-access mapping of attribute

        Returns True if the mapping exists
        """
        return attribute in self.__readables

    def has_writable(self, attribute):
        """
        Check for write-access mapping of attribute

        Returns True if the mapping exists
        """
        return attribute in self.__writables

    def has_deletable(self, attribute):
        """
        Check for delete-access mapping of attribute

        Returns True if the mapping exists
        """
        return attribute in self.__deletables

    def get_readable(self, attribute):
        """
        Get the mapped value of a readable attribute

        Returns ::string
        """
        return self.__readables[attribute]

    def get_writable(self, attribute):
        """
        Get the mapped value of a writable attribute

        Returns ::string
        """
        return self.__writables[attribute]

    def get_deletable(self, attribute):
        """
        Get the mapped value of a deletable attribute

        Returns ::string
        """
        return self.__deletables[attribute]

    # the |= operator
    def __ior__(self, other):
        """
        union of this profile and the other

        Parameters:

            - `other` :: Profile
                the other profile
        """

        # check for conflicts: intersect keys, then see whether intersections
        # map to the same values
        # If you get an assertion failure about this, then you should check
        # your bases to see if any of them map an attribute differently
        # e.g. with profiles a, b and attribute x: a.x should map to the same
        # value as b.x
        assert reduce(lambda x, y: x and y,
                      (reduce(lambda x,y: x and y,
                              (a[key] == b[key]
                              for key 
                              in set(a.iterkeys()) & set(b.iterkeys())),
                              True)
                      for a, b
                      in zip((self.__readables, self.__writables,
                             self.__deletables),
                            (other.__readables, other.__writables,
                             other.__deletables))),
                      True), \
            "Profiles have conflicting mappings, can't take union"

        # no conflicts, go ahead and update
        self.__readables.update(other.__readables)
        self.__writables.update(other.__writables)
        self.__deletables.update(other.__deletables)
        return self

    def remove_mappings(self, modifiers, *names):
        """
        Remove attribute mappings
        
        Parameters:

            `modifiers` :: string
                the types of delegation access to the target to remove. Valid 
                modifiers are combinations of:
                    
                    - `r`: read
                    - `w`: write
                    - `d`: delete

            `names` :: (source_name::string...)
                names of source_name parts of, the mappings to remove
        """

        for name in names:
            assert isinstance(name, basestring), \
                    "Invalid arguments: names should be list of strings: %s" \
                    % (names)

        for name in names:
            if "r" in modifiers:
                self.__readables.pop(name)

            if "w" in modifiers:
                self.__writables.pop(name)

            if "d" in modifiers:
                self.__deletables.pop(name)


    def add_mappings(self, modifiers, *names, **mapped_names):
        """
        Map source to target attribute names, for delegation.
        
        Parameters:

            `modifiers` :: string
                the types of delegation access to the target. Valid modifiers
                are combinations of:
                    
                    - `r`: read
                    - `w`: write
                    - `d`: delete

            `names` :: (source_name::string...)
                names of the attribute names to delegate. The target attribute
                name is the same as `source_name`. This is the same as adding a
                {source_name : source_name} mapping, using the mapped_names
                argument.

            `mapped_names` :: {source_name::string : target_name::string ...}
                names of source and target attributes to map and delegate.

                `target_name`s will be mangled if they have a __ prefix.
                Mangling will occur every time it is delegated to, so you can
                change the target object any time.
        """
        for name in names:
            assert isinstance(name, basestring), (
                "Invalid arguments: names should be list of strings. Got: %s" %
                names)

        for key, name in mapped_names.iteritems():
            assert isinstance(key, basestring) and \
                    isinstance(name, basestring), \
                    "Invalid arguments: mapped_names should be dict of " + \
                    "string:string. Got: %s" % mapped_names

        if "r" in modifiers:
            self.__readables.update(zip(names, names), **mapped_names)

        if "w" in modifiers:
            self.__writables.update(zip(names, names), **mapped_names)

        if "d" in modifiers:
            self.__deletables.update(zip(names, names), **mapped_names)

