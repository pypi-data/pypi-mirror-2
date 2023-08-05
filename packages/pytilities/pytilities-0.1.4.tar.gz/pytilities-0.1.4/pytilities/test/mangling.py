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

import unittest

from pytilities import mangle

class Testlet(object):
    pass

class MainTestCase(unittest.TestCase):
    def test_main(self):
        self.assertEquals(mangle('Name', '_nochange'), '_nochange')
        self.assertEquals(mangle('Name', '__nochange__'), '__nochange__')
        self.assertEquals(mangle('Name', 'nochange'), 'nochange')
        self.assertEquals(mangle('Name', '__change'), '_Name__change')

        t = Testlet()
        self.assertEquals(mangle(t, '_nochange'), '_nochange')
        self.assertEquals(mangle(t, '__nochange__'), '__nochange__')
        self.assertEquals(mangle(t, 'nochange'), 'nochange')
        self.assertEquals(mangle(t, '__change'), '_Testlet__change')
        



