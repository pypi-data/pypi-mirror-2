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

from pytilities import AttributeCollection, mangle
from pytilities.overloading import overloaded, Overload, Param
from pytilities.types import SequenceType
from . import Profile

class Delegator(AttributeCollection):

    """
    An AttributeCollection that delegates attributes of one object to another.

    Instance properties:

        - `target`: Write-only, target of delegation
        - `profile`: Read-write, profile to use for delegation
    """

    def __init__(self, profile=None, target=None):
        """
        Constructs a delegator.

        Parameters:
            `profile` :: Profile = None
                delegation profile. If None, an empty profile is created for
                you.

            `target` = None
                target of delegation
        """
        self.__profile = profile or Profile()
        self.__object = target
        self.__variable_name = None

    @property
    def target(self):
        """
        Write-only, target for delegation.

        Delegated attributes will be delegated to this object.

        Overloaded, setter parameters:

        :a:
            `target_object`
                the object to delegate to
        :b:
            `args` :: (object, variable_name::string)
                target object will be resolved on every get/set/del by doing
                getattr(object, variable_name)
        """
        # it really is write only, this is for internal use
        if self.__variable_name:
            return getattr(self.__object, self.__variable_name)
        else:
            return self.__object

    def __set_target_args(self, args):
        # (object, variable_name)
        self.__object = args[0]
        self.__variable_name = args[1]

        # mangle the variable_name if necessary
        self.__variable_name = mangle(self.__object, self.__variable_name)

    def __set_target_object(self, target_object):
        (self.__object, self.__variable_name) = (target_object, None)

    @target.setter
    @overloaded((
        Overload(__set_target_args,
            Param("args", SequenceType)),
        Overload(__set_target_object,
            Param("target_object"))))
    def target(self):
        pass

    @property
    def profile(self):
        """
        Read-write, the profile to use for attribute mappings.

        Returns ::Profile

        Setter parameters:

            `value` :: Profile
                the profile
        """
        return self.__profile

    @profile.setter
    def profile(self, value):
        self.__profile = value

    def getattr_(self, name):
        if self.profile.has_readable(name):
            return (True, getattr(self.target,
                                  mangle(self.target, 
                                         self.profile.get_readable(name))))
        elif self.profile.has_readable("__getattr__"): 
            # this way we don't forget to delegate __getattr__
            try:
                return (True, self.target.__getattr__(name))
            except AttributeError:
                pass

        return (False, None)

    def setattr_(self, name, value):
        if self.profile.has_writable(name):
            setattr(self.target, 
                    mangle(self.target, self.profile.get_writable(name)),
                    value)
            return True
        elif self.profile.has_readable("__setattr__"): 
            # this way we don't forget to delegate __setattr__
            try:
                return (True, self.target.__setattr__(name, value))
            except AttributeError:
                pass

        return False

    def delattr_(self, name):
        if self.profile.has_deletable(name):
            delattr(self.target,
                    mangle(self.target, self.profile.get_deletable(name)))
            return True
        elif self.profile.has_readable("__delattr__"): 
            # this way we don't forget to delegate __delattr__
            try:
                return (True, self.target.__delattr__(name))
            except AttributeError:
                pass

        return False

