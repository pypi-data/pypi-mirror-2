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

from pytilities.overloading import overloaded, Overload, Param

def __mangle_cls(cls_name, attribute):
    assert(isinstance(attribute, basestring))

    if attribute.startswith("__") and not attribute.endswith("__"):
        return "_" + cls_name + attribute
    else:
        return attribute

def __mangle_instance(instance, attribute):
    return __mangle_cls(instance.__class__.__name__, attribute)

@overloaded((
    Overload(__mangle_cls,
        Param('cls_name', basestring),
        Param('attribute')),
    Overload(__mangle_instance,
        Param('instance'),
        Param('attribute'))),
    False)
def mangle():
    """
    Get the mangled name of an attribute
    
    Overloaded parameters:

    :a:

        `cls_name` :: string
            the name of the class to which the attribute belongs

        `attribute` :: string
            the attribute name to mangle

    :b:

        `instance`
            the instance to which the attribute belongs to. It's class name
            will be used for mangling.

        `attribute` :: string
            the attribute name to mangle
    
    Returns mangled attribute, if it starts with '__' and doesn't end with
    '__'. Otherwise, `attribute` is returned :: string
    """
