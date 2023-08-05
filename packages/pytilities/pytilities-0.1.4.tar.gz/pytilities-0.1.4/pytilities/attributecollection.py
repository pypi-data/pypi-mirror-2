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

class AttributeCollection(object):
    """
    Abstract, represents a collection of attributes.

    Attribute collections can represent infinite amounts of attributes,
    generate them at request, ...

    Methods:

        - `getattr_`: Try to get the value of an attribute
        - `setattr_`: Try to set the value of an attribute
        - `delattr_`: Try to delete an attribute
    """

    # Note: we use an error code return as this is faster than spawning
    # exceptions and this may happen quite often, rather than exceptionally
    def getattr_(self, name):
        """
        Try to get the value of an attribute

        Parameters:

            `name` :: string
                name of the attribute to get

        Returns whether the attribute was found, and if so, its value
        :: (found_attribute::bool, value)
        """
        raise NotImplementedError('abstract')

    def setattr_(self, name, value):
        """
        Try to set the value of an attribute

        Parameters:

            `name` :: string
                name of the attribute to set

            `value`
                the new value
                    
        Returns True, if the attribute was found, False otherwise
        """
        raise NotImplementedError('abstract')

    def delattr_(self, name):
        """
        Try to delete an attribute

        Parameters:

            `name` :: string
                name of the attribute to delete

        Returns True, if the attribute was found, False otherwise
        """
        raise NotImplementedError('abstract')
