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

# Note: this file name isn't standard as epydoc and our testing couldn't
# understand it if we named it dispatcher.py; it would clash in __init__.py
# with the dispatcher decorator

__docformat__ = 'reStructuredText'

from pytilities.delegation import (
    delegator_factory, delegated)

class UnsupportedEventError(Exception):
    """Tried to access an unregistered event"""

    def __init__(self, event_name):
        Exception.__init__(self, "Unsupported event: %s" % event_name)

@delegator_factory()
class Dispatcher(object):

    """
    Utility class for dispatching events to handlers.

    Events have to be registered before they can be dispatched or have handlers
    added to them.

    Handlers can have an owner associated with them, usually you'll use the
    reference of the listener. This allows you to remove all the handlers of a
    specific owner, which should save you some work.

    Instance methods:

        - `add_handler`: Add handler for an event
        - `remove_handlers`: Remove all or some handlers
        - `remove_handler`: Remove a handler
        - `dispatch`: Dispatch an event
        - `register_events`: Register events
        - `has_event`: Check whether event is supported

    Instance properties:

        - `events`: Read-only, set of all supported events

    Instance decorators:

        - `event`: Register decorated as a handler

    Class invariants:

        - For every (owner, event), there can be only 0 or 1 handlers
    """

    # inspired by pyglet.event.EventDispatcher, yay pyglet

    @staticmethod
    def __init_delegation_profiles(profiles):
        profiles['default'] |= profiles['public']

    def __init__(self):
        # dict of handlers: event_name -> set((handler, owner))
        self.__handlers = {}
        self.__registered_events = set()

    @delegated("public")
    def add_handler(self, event_name, handler, owner = None):
        """
        Add handler for an event, optionally with an owner.

        Parameters:

            event_name :: string
                name of the event to add the handler to

            handler :: callable
                the handler to call when the event is dispatched

            owner = None
                owner of the handler. Use this reference to easily remove all
                your handlers from the dispatcher (e.g. remove all handlers
                with the same owner)

        Raises:

            - `UnsupportedEventError` when `event_name` doesn't exist
        """

        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        assert handler, "handler argument musn't be None"

        assert (handler, owner) not in self.__handlers, (
            "You cannot add the same handler for the same owner and event " +
            "more than once.")

        self.__handlers.setdefault(event_name, set())
        self.__handlers[event_name].add((handler, owner))

    @delegated("public")
    def remove_handlers(self, event_name=None, owner=None):
        """
        Remove all or some handlers of the dispatcher.
        
        `event_name` and `owner` act as filters of what to remove.

        If no handler matched the criterea, the method will return silently.

        Parameters:

            event_name :: string = None
                the event of which to remove the handlers. `None` means any

            owner = None
                the owner of which to remove the handlers. `None` means any
        """

        if event_name:
            self.__remove_handlers(event_name, owner)
        else:
            for event in self.__registered_events:
                self.__remove_handlers(event, owner)

    def __remove_handlers(self, event, owner):
        """Remove handlers of single event, optionally with particular owner """
        handlers = self.__handlers[event]
        handlers -= set((handler, o) for (handler, o) in handlers 
                        if o is owner)

    @delegated("public")
    def remove_handler(self, event_name, handler, owner = None):
        """
        Remove a handler from an event. It is an error to try to remove a
        handler from an event that doesn't have this handler attached to it.

        Parameters:

            event_name :: string
                name of the event to which the handler belongs

            handler :: callable
                the handler that is attached to the event

            owner = None
                owner of the handler

        Preconditions:
            1. `handler` is attached to `event_name`

        Raises:
            - `UnsupportedEventError` when `event_name` doesn't exist
        """

        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        assert handler, "handler argument musn't be None"

        self.__handlers[event_name].remove((handler, owner))

    @delegated()
    def dispatch(self, event_name, *args, **keyword_args):
        """
        Dispatch an event to its handlers. 
        
        The handlers are executed in a random order.
        
        Parameters:

            event_name :: string
                name of the event to dispatch

            args
                arguments to pass to the handlers

            keyword_args
                keyword arguments to pass to the handlers

        Raises:
            - `UnsupportedEventError` when `event_name` doesn't exist
        """

        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        for handler in self.__handlers.get(event_name, ()):
            handler[0](*args, **keyword_args)

    @delegated("public")
    def event(self, event_name, owner = None):
        """
        Register the decorated as a handler of `event_name`

        Parameters:

            event_name :: string
                name of the event

            owner = None
                owner of the handler. Use this reference to easily remove all
                your handlers from the dispatcher (e.g. remove all handlers
                with the same owner)
        """

        def decorator(handler):
            self.add_handler(event_name, handler, owner)
            return handler

        return decorator

    @delegated()
    def register_events(self, *event_names):
        """
        Register events.
        
        Parameters:

            event_names :: (string...)
                names of events to support
        """
        # this allows us to have methods like has event, which allow for better
        # duck typing (if I see something that sends out quack events, then I
        # call that a duck)
        self.__registered_events.update(event_names)

    @delegated("public")
    def has_event(self, event_name):
        """
        Checks if `event_name` is supported

        Parameters:
        
            event_name :: string
                name of the event

        Returns True if the dispatcher has the event
        """
        return event_name in self.__registered_events

    @delegated("public")
    @property
    def events(self):
        """
        Read-only, set of all supported events

        Returns ::frozenset(string...)
        """
        return frozenset(self.__registered_events)

