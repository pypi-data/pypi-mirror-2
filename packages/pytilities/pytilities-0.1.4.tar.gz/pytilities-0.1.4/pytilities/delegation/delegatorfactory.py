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

from . import Profile, Delegator

class DelegatorFactory(object):
    """
    Allows easy creation of delegators with `Profile`s.

    By default already has a default profile.
    
    Instance methods:

        - `set_profile`: Add/replace a `Profile`
        - `Delegator`: Construct a `Delegator` from a stored profile
        - `has_profile`: See if we have a particular profile
        - `get_profile`: Get profile by name

    Class invariants:

        - Every profile has a unique name
        - There's always a name='default' profile
    """

    def __init__(self):
        self.__profiles = {'default': Profile()}

    def set_profile(self, name, profile):
        """
        Add/replace a delegator factory `Profile` to/on the factory.

        Parameters:

            `name` :: string
                name of the profile

            `profile` :: Profile
                the profile for addition/replacement
        """
        self.__profiles[name] = profile

    def Delegator(self, profile_name = "default", target=None):
        """
        Construct a delegator with a stored `Profile`.

        Parameters:
        
            `profile_name` :: string
                name of the `Profile` to use to set up the delegator with

            `target` = None
                target of the newly created delegator

        Returns newly created delegator :: Delegator

        Raises:

            - `ValueError` when no profile with name `profile_name` exists
        """
        return Delegator(self.get_profile(profile_name), target)

    def has_profile(self, name):
        """
        See if profile with given name exists.

        Parameters:

            `name` :: string
                name of the profile to look for
        
        Returns True if the factory can find a profile by that name, False
        otherwise
        """
        return name in self.__profiles

    def get_profile(self, name):
        """
        Get profile by name.

        Parameters:

            `name` :: string
                name of the profile

        Returns bound profile by name :: Profile

        Raises:
            - `ValueError` when profile isn't found
        """
        try:
            return self.__profiles[name]
        except KeyError:
            raise ValueError("Failed to find profile: %s" % name)

