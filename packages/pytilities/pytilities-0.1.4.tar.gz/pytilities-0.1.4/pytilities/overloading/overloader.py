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

from .parameter import Param

_logger = logging.getLogger("pytilities.overloading.overloader")

class Overloader(object):
    """
    A collection of `Overload`s that can process calls.

    Tool for overloading operations.
    
    Has an ordered collection of overloads which serve as rules, the operation
    of the matching overload is called. If none match, an assertion error is
    raised.

    Methods:

        - `process_call`: Process a call with given args and keyword args
    """

    def __init__(self, overloads, add_self = True):
        """
        Construct an `Overloader`.

        Parameters:

            `overloads` :: (Overload...)
                a collection of rules indicating which operation to call for
                which combination of arguments/parameters. Note: the order can
                effect which overload is matched as the first matching overload
                is used. Must specify at least one overload.

            `add_self` :: bool = True
                if True, a "self" parameter is inserted at the beginning of the
                parameter list of each overload
        """

        assert overloads, "Must specify at least one overload"

        self.__overloads = overloads

        if add_self:
            self_param = Param("self")
            for overload in overloads:
                overload.insert_params(0, self_param)

    def process_call(self, args, kwargs):
        """
        Process a call with given args and keyword args.
        
        The matching overload is called.

        Parameters:

            `args`, `kwargs'
                arguments of the call

        Returns the return value of the called operation
        """

        _logger.debug("Processing call")

        for overload in self.__overloads:
            (matched, return_value) = overload.process_call(args, kwargs)
            if matched: 
                return return_value

        assert False, "Failed to find matching overload for given"

