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
All sorts of geometry trinkets

Classes:

    `Vector`
        2D Point/Vector

    `BoundVector`
        `Vector` whose x and y values are stored elsewhere.

    `ImmutableVector`
        `Vector` wrapper that makes the vector immutable.

    `VerboseVector`
        `Vector` wrapper that sends out events.

    `Rectangle`
        A rectangle identified by two points.

    `VerboseRectangle`
        `Rectangle` wrapper that sends out events
"""

__docformat__ = 'reStructuredText'

from .vector import Vector
from .verbosevector import VerboseVector
from .immutablevector import ImmutableVector
from .boundvector import BoundVector
from .rectangle import Rectangle
from .verboserectangle import VerboseRectangle

