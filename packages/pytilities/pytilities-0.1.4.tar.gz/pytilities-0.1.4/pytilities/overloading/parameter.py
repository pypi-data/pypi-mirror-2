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

import logging

from .matchers import matches_everything, matches_type

_logger = logging.getLogger("pytilities.overloading.parameter")

class Parameter(object):

    """
    A parameter of an operation.
    
    It can match arguments and provide default values for them.

    Note that an argument matches a parameter, if its matcher returns True on
    the argument value or the parameter has a default.

    Methods:

        - `read_arg`: Read/process the given arg.
        - `read_kwargs`: Look in a dict for a matching arg and process its value
        - `write`: Adds the last read argument value to a dictionary.
    """

    # support multiple types per param? Wait for a feature request first
    def __init__(self, name, matcher = matches_everything, *args, **kwargs):
        """
        Construct a `Parameter`.

        Parameters:

            `name` :: string
                name of parameter as specified in keyword arguments

            `matcher` :: 
                Either of:

                    - type of the parameter
                    - iterable of possible types of param
                    - a matcher function :: f(value) -> matched::bool
            
            `default`
                default value for the parameter. Omit if param has no default

        Preconditions:
            1. `default` must match the specified matcher
        """

        assert name, "Name param musn't be empty or None"
        assert isinstance(name, basestring), "Name must be a string"
        assert len(args) <= 1, \
            "Unexpected trailing args: %s" % args
        assert not (args and "default" in kwargs), (
            "Default specified twice: by *args(%s) and **kwargs(%s)" %
            (args[0], kwargs["default"]))

        self.__name = name

        if hasattr(matcher, "__iter__"):
            # iter of types
            self._matcher = matches_type(*matcher)
        elif isinstance(matcher, type):
            # a single type
            self._matcher = matches_type(matcher)
        else:
            # it's a matcher function
            self._matcher = matcher

        self.__has_default = True
        if args:
            self.__default = args[0]
        elif "default" in kwargs:
            self.__default = kwargs["default"]
        else:
            self.__has_default = False

        assert not self.__has_default or \
                self._matcher(self.__default), (
                "Default must match the given matcher as well. (Precondition 1) Default: %s" %
                    (self.__default))

        # whether or not last read was a match
        self.__matched = False

    # Note: the two step (read all, then write) process is necessary to allow for
    # self validating parameters in the future. This allows them to return True at
    # read when they match, and throw errors at write when the overload apparantly
    # matched and their values will actually be used. (at time of read that is not
    # yet certain)
    def read_arg(self, arg):
        """
        Read/process the given arg.
        
        Parameters:

            `arg`
                the argument value to read

        Returns True if parameter matches `arg` :: bool
        """
        self.__value = arg
        self.__matched = self._matcher(self.__value)
        return self.__matched

    def read_kwargs(self, kwargs):
        """
        Look in a dict for a matching arg and process its value.

        Parameters:
            
            `kwargs` :: {name::string : value}
                dictionary of arguments

        Returns True if a matching argument was found in `kwargs` :: bool
        """

        if self.__name in kwargs:
            return self.read_arg(kwargs[self.__name])
        elif self.__has_default:
            self.__matched = True
            self.__value = self.__default
        else:
            self.__matched = False

        return self.__matched

    def write(self, kwargs):
        """
        Adds the last read argument value to a dictionary.

        Parameters:

            `kwargs` :: {name::string : value}
                the dictionary to add the last value and the parameter name to

        Preconditions:

            1. the parameter matched on the last read
        """

        assert self.__matched, \
               "write() may only be called after a succesful read()"

        kwargs[self.__name] = self.__value

    @property
    def _matched(self):
        return self.__matched


# a shortcut
Param = Parameter

# TODO: write a validation.py or something like that, add in lots of fun stuff
# like self-validating Parameters that we can then use here! (e.g. check for
# None values etc)
# or add using Strategy pattern: Validator(s)

