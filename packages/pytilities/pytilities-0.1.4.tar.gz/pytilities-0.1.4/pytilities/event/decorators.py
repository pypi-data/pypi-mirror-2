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
Various decorators to ease event dispatching.
"""

__docformat__ = 'reStructuredText'

from pytilities import mangle
from . import Dispatcher, DispatcherSwitch

def dispatcher(*event_names):
    """
    Installs a `Dispatcher` on an `AttributeCollectionBase`.

    This class decorator does the following:
        - create a `Dispatcher` and store it in `self.__dispatcher`
        - delegate to all methods of the dispatcher's public delegation profile
        - add a `self.__dispatch` method that delegates to
          `self.__dispatcher.dispatch`
        - register the `event_names` on the dispatcher

    Note on ctor usage: though `self.__dispatcher` already exists, the delegation
    to it is not yet installed. You can use `self.__dispatcher`, but you can't
    yet e.g. call `self.add_handler`, write `self.__dispatcher.add_handler`
    instead.

    Parameters:
        event_names :: (::string...)
            collection of events to register on the dispatcher
    """

    def _dispatcher(cls):
        # remember the original init
        true_init = cls.__init__

        def init(self, *args, **kwargs):
            # create dispatcher and register events
            dispatcher = Dispatcher()
            dispatcher.register_events(*event_names)

            # store the dispatcher on the instance
            setattr(self, mangle(cls.__name__, "__dispatcher"), dispatcher)

            # call original init
            true_init(self, *args, **kwargs)

            # delegate public + dispatch()
            delegator = Dispatcher.Delegator("public", dispatcher)
            delegator.profile.add_mappings(
                "r", **{mangle(cls.__name__, "__dispatch"): "dispatch"})

            self._append_attribute_collection(delegator)

        # replace init with our init
        cls.__init__ = init

        return cls

    return _dispatcher

def dispatcher_switch(cls):
    """
    Installs a `DispatcherSwitch` on an `AttributeCollectionBase`.

    This class decorator does the following:
        - create a `DispatcherSwitch` and store it in self.__dispatcher_switch
        - delegate to all methods of the switch's public delegation profile
        - add a `self.__dispatch` method that delegates to
          `self.__dispatcher_switch.dispatch`

    Note on ctor usage: though `self.__dispatcher_switch` already exists, the
    delegation to it is not yet installed. You can use
    `self.__dispatcher_switch`, but you can't yet e.g. call `self.add_handler`,
    write `self.__dispatcher_switch.add_handler` instead.
    """

    # remember the original init
    true_init = cls.__init__

    def init(self, *args, **kwargs):
        # create switch
        switch = DispatcherSwitch()

        # store on the instance
        setattr(self, mangle(cls.__name__, "__dispatcher_switch"), switch)

        # call original init
        true_init(self, *args, **kwargs)

        # delegate public
        delegator = Dispatcher.Delegator("public", switch)
        delegator.profile.add_mappings(
            "r", **{mangle(cls.__name__, "__dispatch"): "dispatch"})
        self._append_attribute_collection(delegator)

    # replace init with our init
    cls.__init__ = init

    return cls

