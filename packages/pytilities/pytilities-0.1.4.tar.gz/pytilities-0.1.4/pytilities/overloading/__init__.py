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

'''
Function overloading tools.

Classes:

    `Parameter`
        A parameter of an operation.

    `Param`
        Alias for `Parameter`

    `CompositeParameter`
        `Parameter` that consists of more parameters.

    `CompositeParam`
        Alias for `CompositeParameter`

    `Overloader`
        A collection of `Overload`s that can process calls.

    `Overload`
        An operation signature with an operation to call when arguments match.


Decorators:

    `overloaded`
        Overloads an operation.
'''

__docformat__ = 'reStructuredText'

from .parameter import Parameter, Param
from .compositeparameter import CompositeParameter, CompositeParam
from .overload import Overload
from .overloader import Overloader
from .decorators import overloaded

# Implementation note: we can't use overloaded(), etc. to do overloading in this 
# package. It would cause an infinite recursive loop

