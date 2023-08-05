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

from .profile import Profile
from .delegator import Delegator

class DelegatorFactory(object):
    """
    Allows easy creation of delegators with `Profile`s.
    
    It also supports a form of inheritance. By specifying base
    factories, a factory extends its bases' profiles (it takes the union of all
    base profiles and its own). Using the inheritance you can add new profiles
    and add attributes to existing profiles; you cannot, however, override
    attributes.

    Instance methods:

        - `add_delegator_profile`: Add a `Profile`
        - `Delegator`: Construct a `Delegator` from a stored profile
        - `has_profile`: See if we have a particular profile
        - `get_profile`: Get profile by name

    Class invariants:

        - Every profile has a unique name
    """

    def __init__(self, bases=()):
        """
        Construct a `DelegatorFactory`, optionally with bases to inherit from.
        
        Parameters:

            `bases` :: (::DelegatorFactory...)
                base factories for the created factory
        """
        self.__bases = bases
        self.__profiles = {}

    def add_delegator_profile(self, name, profile):
        """
        Add a new delegator factory `Profile` to the factory.

        Parameters:

            `name` :: string
                name of the profile

            `profile` :: Profile
                the profile to add
        """
        assert name not in self.__profiles, \
                "Tried to add profile that's already added to this list." + \
                " A DelegatorFactory cannot contain the same profile twice"

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
        for base in self.__bases:
            if base.has_profile(name):
                return True

        return name in self.__profiles

    def get_profile(self, name):
        """
        Get profile by name.

        Parameters:

            `name` :: string
                name of the profile

        Returns profile by name, taking into account base factories' profiles 
        :: Profile

        Raises:
            - `ValueError` when profile isn't found
        """
        profile = Profile()
        found = False  # whether we have found the profile, anywhere

        if name in self.__profiles:
            profile |= self.__profiles[name]
            found = True

        for base in self.__bases:
            if base.has_profile(name):
                profile |= base.get_profile(name)
                found = True

        if not found:
            raise ValueError("Failed to find profile: %s" % name)

        return profile

