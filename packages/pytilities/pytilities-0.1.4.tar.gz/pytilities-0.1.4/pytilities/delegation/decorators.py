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
Various decorators to ease delegation
"""

__docformat__ = 'reStructuredText'

from types import UnboundMethodType
import logging

from . import Profile, DelegatorFactory

# logging stuff
_logger = logging.getLogger("pytilities.delegation")

# Note: we don't care about mangling here, there's no need to. You won't be
# delegating any private vars anyway, or at least you shouldn't.

def delegator_factory():
    """
    Makes a `DelegatorFactory` on the class and adds profiles to it.

    The factory is stored as a class attribute with name _delegator_factory.
    A Delegator method is installed on the class, it is the same as
    _delegator_factory.Delegator.
    
    `Profile`s are created based on the annotations left by `delegated`.
    """

    def _delegator_factory(cls):
        # iterate through attributes and generate profiles
        # {name: Profile}
        profiles = {"default": Profile()}  # there's always a default
        for name in cls.__dict__:
            attribute = getattr(cls, name)

            _logger.debug(name)
            if isinstance(attribute, property):
                _logger.debug("prop")
                data_holder = attribute.fget
            elif isinstance(attribute, UnboundMethodType):
                _logger.debug("unbound method!")
                data_holder = attribute.im_func
            else:
                _logger.debug("I have no clue what this is")
                data_holder = attribute

            if hasattr(data_holder, "__pytilities_delegation_profiles"):
                _logger.debug("is delegated!")
                profile_data = data_holder.__pytilities_delegation_profiles
                for profile_name, modifiers in profile_data.iteritems():
                    profiles.setdefault(profile_name, Profile())
                    profiles[profile_name].add_mappings(modifiers, name)

                del data_holder.__pytilities_delegation_profiles

        # make factory with profiles
        factory = DelegatorFactory()

        for name, profile in profiles.iteritems():
            factory.set_profile(name, profile)

        # install stuff on cls
        setattr(cls, "_delegator_factory", factory)
        cls.Delegator = factory.Delegator

        return cls

    return _delegator_factory

def delegated(profile_name="default", modifiers="rwd"):
    """
    Includes the decorated attribute in the specified delegation profile.

    Parameters:

        `profile_name` :: string
            name of the `Profile` to add the attribute to

        `modifiers` :: string
            the types of access to delegate to the target. Possible modifiers
            are combinations of:
                
                - `r`: read
                - `w`: write
                - `d`: delete
    """

    def _delegate(attribute):
        _logger.debug("%s += %s" % (profile_name, attribute))
        if not hasattr(attribute, "__pytilities_delegator_profiles"):
            if isinstance(attribute, property):
                # stick data on the getter function, can't set attribs on
                # properties
                data_holder = attribute.fget
            else:
                data_holder = attribute

            data_holder.__pytilities_delegation_profiles = {}

        data_holder.__pytilities_delegation_profiles[profile_name] = modifiers

        return attribute

    return _delegate

