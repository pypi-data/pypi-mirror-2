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

# TODO: document on the wiki, also document DiscreteRectangle

# Note: None of these support mangling. It can't know about the class it
# resides in, so it can't mangle for them, and it can't use the descriptor's
# obj param as derived classes mangle differently than their base. So mangling
# has to be done manually by the user of these descriptor classes.

from .attributedescriptor import AttributeDescriptor
from .dereferenceddescriptor import DereferencedDescriptor
from .bounddescriptor import BoundDescriptor
from .restricteddescriptor import RestrictedDescriptor

