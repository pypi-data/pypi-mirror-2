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

import pdb
import unittest

# TODO this works! awesome, start doing this more often in test packages. Also
# do a from . in all other places where applicable. In all other cases, use
# absolute paths
from .. import dispatcher, dispatcher_switch, Dispatcher
from .helpers import Listener
from pytilities import AttributeCollectionBase

@dispatcher("a", "b")
class ADispatcher(AttributeCollectionBase):
    def __init__(self, arg):
        AttributeCollectionBase.__init__(self)
        self.inited = True
        self.arg = arg

        # just checking wheter this exists, I don't care about the event
        self.__dispatcher.has_event("a")

    def dispatch_a(self):
        self.__dispatch("a")

    def dispatch_b(self):
        self.__dispatch("b", 5)

class BDispatcher(ADispatcher):
    def __init__(self, arg):
        ADispatcher.__init__(self, arg)

class DispatcherTestCase(unittest.TestCase):
    def setUp(self):
        self.l = Listener()
        self.d = ADispatcher(2)

    def test_success(self):
        self.assert_(self.d.inited)
        self.assertEquals(self.d.arg, 2)
        self.assert_(self.d.has_event("a"))
        self.assert_(self.d.has_event("b"))

        self.d.add_handler("a", self.l.handle_noarg)
        self.d.add_handler("b", self.l.handle_1arg)
        self.d.dispatch_a()

        self.assertEquals(self.l.read(), "noarg")

        self.d.dispatch_b()
        self.assertEquals(self.l.read(), "1arg: 5")


class BDispatcherTestCase(DispatcherTestCase):
    def setUp(self):
        self.l = Listener()
        self.d = BDispatcher(2)


@dispatcher_switch
class Switch(AttributeCollectionBase):
    def __init__(self, arg):
        AttributeCollectionBase.__init__(self)

        self.inited = True
        self.arg = arg

        # just checking wheter this exists, I don't care about the event
        self.__dispatcher_switch.has_event("a")

        d = Dispatcher()
        d.register_events("a", "b")
        self.__dispatcher_switch.append_dispatchers(d)

        self.__dispatcher = d

    def dispatch_a(self):
        self.__dispatcher.dispatch("a")

    def dispatch_b(self):
        self.__dispatcher.dispatch("b", 5)


class BSwitch(Switch):
    def __init__(self, arg):
        Switch.__init__(self, arg)


class SwitchTestCase(unittest.TestCase):
    def setUp(self):
        self.l = Listener()
        self.d = Switch(2)

    def test_success(self):
        self.assert_(self.d.inited)
        self.assertEquals(self.d.arg, 2)

        self.d.add_handler("a", self.l.handle_noarg)
        self.d.add_handler("b", self.l.handle_1arg)
        self.d.dispatch_a()

        self.assertEquals(self.l.read(), "noarg")

        self.d.dispatch_b()
        self.assertEquals(self.l.read(), "1arg: 5")


class BSwitchTestCase(unittest.TestCase):
    def setUp(self):
        self.l = Listener()
        self.d = BSwitch(2)


def run():
    unittest.main(__name__)

