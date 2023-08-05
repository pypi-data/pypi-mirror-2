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

from . import UnsupportedEventError

class RestrictedDispatcher(object):

    """
    `Dispatcher` wrapper that filters the list of supported events.

    Filter rules (in the specified order):

        - If it matches a disallow rule, it is not let through
        - If there are no allow rules, all the rest is let through
        - If there are allow rules, it must match an allow rule

    Check `Dispatcher` for the documentation of the methods that are left
    undocumented here.
    """

    def __init__(self, dispatcher, allow = None, disallow = None):
        """
        Construct a restricted dispatcher.

        `disallow` takes precedence over `allow_events`.

        Parameters:

            dispatcher :: Dispatcher
                the dispatcher to wrap around

            allow :: (string...):
                a list of events that are allowed. If `None`, all are allowed,
                unless they are in `disallow_events`

            disallow :: (string...)
                disallowed events
        """
        assert dispatcher, "dispatcher musn't be None"
        self.__dispatcher = dispatcher
        self.__allowed_events = set(allow or ())
        self.__disallowed_events = set(disallow or ())

    def add_handler(self, event_name, handler, owner = None):
        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        self.__dispatcher.add_handler(event_name, handler, owner)

    def remove_handlers(self, event_name=None, owner=None):
        # pass on the call, making sure we don't remove handlers for events we
        # don't support
        if event_name:
            if not self.has_event(event_name):
                raise UnsupportedEventError(event_name)

            self.__dispatcher.remove_handlers(event_name, owner)
        else:
            for event in self.events:
                self.__dispatcher.remove_handlers(event, owner)

    def remove_handler(self, event_name, handler, owner = None):
        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        self.__dispatcher.remove_handler(event_name, handler, owner)

    def dispatch(self, event_name, *args, **keyword_args):
        if not self.has_event(event_name):
            raise UnsupportedEventError(event_name)

        self.__dispatcher.dispatch(event_name, *args, **keyword_args)

    def event(self, event_name, owner=None):
        def decorator(handler):
            self.add_handler(event_name, handler, owner)
            return handler

        return decorator

    @property
    def events(self):
        return (self.__dispatcher.events - self.__disallowed_events) \
                & self.__allowed_events

    def has_event(self, event_name):
        return (
            not (self.__disallowed_events and
                 event_name in self.__disallowed_events) and
            (not self.__allowed_events or
             event_name in self.__allowed_events) and 
            self.__dispatcher.has_event(event_name)
        )

