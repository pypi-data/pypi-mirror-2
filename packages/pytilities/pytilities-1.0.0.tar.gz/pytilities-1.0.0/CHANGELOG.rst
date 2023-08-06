1.0.0 
-----

The library moved to python3, older python versions are no longer supported.
There a lot of changes, breaking quite a bit of the previous interface. All
changes are listed below.


pytilities 
''''''''''

:Added:
    - get_annotations: gets annotations of an object, allows to add new ones,
      ...
    - get_attr_name, get_attr_value, has_attr_name, has_attr_value: gets an
      attribute, bypassing regular lookup (no descriptor.__get__, ..., does
      support inheritance though)

:Removed: 
    - AttributeCollection, AttributeCollectionBase: use aop instead (see User
      Guide)

:Changed:
    - mangle: 

      - You can now pass an instance as well.
      - Small fix involving class names that start with a '_'

pytilities.aop 
''''''''''''''

This package brings aspect oriented language features to python (in a handy
format). You can apply advice on classes and instances, using aspects that can
be applied and unapplied, enabled, disabled, ...

:Added:
    - advisor: singleton that aspects use to give advice (you shouldn't use
      this directly, derive from Aspect and use its methods instead)
    - proceed, return_close, return\_, arguments, advised, obj, name yields for
      advice functions
    - Aspect: base class to write your own aspects with (you are not required
      to use this, but it is greatly recommended)
    - AOPMeta: classes that are given * advice require to have AOPMeta as
      metaclass, other advised classes may benefit from this metaclass as it
      reduces memory usage

pytilities.delegation 
'''''''''''''''''''''

:Added:
    - DelegationAspect: delegate attributes from a source instance/cls to a
      target. Only supports direct mappings (mappings with the same source and
      target attributes).
    - in_profile, profile_carrier: used to more easily place some profiles on a
      class

:Changed:
    - Profile

:Removed:
    - Delegator, DelegatorFactory: use delegate or any of the other
      possibilities listed in the User Guide instead
    - delegator_factory: use profile_carrier instead.
    - delegated: use in_profile instead.
    - delegate: use DelegationAspect instead. You may want to read about AOP in
      the user guide first

pytilities.descriptors (new) 
''''''''''''''''''''''''''''

:Added:
    - AttributeDescriptor: turns a regular attribute into a descriptor
    - DereferencedDescriptor: returns inner_desc.get.get, sets
      inner_desc.get.set, ...
    - BoundDescriptor: binds an instance to a descriptor, much like bound
      methods
    - RestrictedDescriptor: strip of the get, set or del of a descriptor

pytilities.event 
''''''''''''''''

:Removed:
    - dispatcher, dispatcherswitch (decorators): normally you'd send events
      from an aspect as it's a crosscutting concern, so these no longer have to
      be supported. Use a custom Aspect + DelegationAspect instead.

pytilities.geometry 
'''''''''''''''''''

:Added:
    - DiscreteVector, DiscreteRectangle: A Vector/Rectangle with a discrete
      coordinate space. All aspects and views for Vector/Rectangle work on
      these as well.
    - verbose_rectangle_aspect, verbose_vector_aspect: Aspects to make a
      Rectangle/Vector send out (change) events.
    - ImmutableRectangle, ImmutableVector: immutable views of a
      Rectangle/Vector
    - immutable_rectangle_aspect, immutable_vector_aspect: makes a
      Rectangle/Vector immutable

:Changed:
    - Vector, Rectangle: Due to a change in int division mechanisms in python3,
      these classes will always operate with a continuous coordinate space. I.e
      if your vector has coords (3, 1), then when divided by 2 they become
      (1.5, 0.5) and not (1, 0) as they used to be in previous versions. Use
      DiscreteVector and DiscreteRectangle instead, to get similar behaviour
      back.
    - Vector, DiscreteVector: have an extra overload for assign that accepts
      (x,y) as args

:Removed:
    - BoundVector: use Vector directly instead (use its bound properties
      overload)
    - VerboseVector: make a Vector and do verbose_vector_aspect.apply(v)
      instead. This works for DiscreteVectors as well.
    - VerboseRectangle: make a Rectangle and do
      verbose_rectangle_aspect.apply(v) instead. This works for DiscreteVectors
      as well.

pytilities.overloading 
''''''''''''''''''''''

:Changed:
    - overloaded: its returned function now has a process_args method as well
    - Parameter: its ctor was incorrectly overloaded (ironically). This has
      been fixed, its overloads changed slightly because of this.

pytilities.infinity (new) 
'''''''''''''''''''''''''

Provides a cross-platform alternative to float('inf').

:Added:
    - infinity, negative_infinity, nan
    - is_infinity

pytilities.tests 
''''''''''''''''

:Added:
    - is_public, is_protected, is_private, is_special: attribute name checks


0.1.4
-----

- Mangle, mangling and event.dispatcher: fixed a slight name clash
- Overhauled testing, it is now easier to use
- Removed inheritance feature of DelegatorFactory, it was too vague
- Removed __init_delegation_profiles, there are other ways to achieve the same
  thing
- Changed the DelegatorFactory interface so that it is hopefully more intuitive
  to use
- Added all set operators to delegation.Profile
- Added more tests and fixed some docstrings
- RestrictedDispatcher: Made allow and disallow mutually exclusive. It made no
  sense to specify both


0.1.3
-----

- Added html reference documentation


0.1.2
-----

- Added runtests.py, which allows running unit tests
- Added the types package (forgot this in last release)


0.1.1
-----

- Fixed: the last release wouldn't parse


0.1.0
-----

- Initial release: delegation tools, events, overloading, ...
