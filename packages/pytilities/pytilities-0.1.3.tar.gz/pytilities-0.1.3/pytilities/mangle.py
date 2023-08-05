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

def mangle(obj, attribute):
    """
    Get the mangled name of an attribute
    
    Overloaded parameters:

    :a:

        `instance`
            the instance to which the attribute belongs to. It's class name
            will be used for mangling.

        `attribute` :: string
            the attribute name to mangle

    :b:
        `cls_name` :: string
            the name of the class to which the attribute belongs
    
    Returns mangled attribute, if it starts with '__' and doesn't end with
    '__'. Otherwise, `attribute` is returned :: string
    """

    assert(isinstance(attribute, basestring))

    if attribute.startswith("__") and not attribute.endswith("__"):
        if isinstance(obj, basestring):
            class_name = obj
        else:
            class_name = obj.__class__.__name__

        return "_" + class_name + attribute
    else:
        return attribute

