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
Test utilities

Allows testing whole test hierarchies. 

Note: It involves copying testall.py files around, etc, I'm sure there are
better ways of doing this, for my projects it was good enough though.

Functions:

    - `test_suite_from_package`: Recursively get test suite of all tests in a 
    package

    - `run`: Run test and print results to stderr
"""

__docformat__ = 'reStructuredText'

import unittest
import os
import logging

_logger = logging.getLogger("pytilities.testing")

# note: implementation hiding is quite horrible here, imo might want to TODO.
# usage is way too difficult to explain and too difficult in general
# If someone could point me to something that already provides hierarchical
# testing, please do, send an email
def test_suite_from_package(module_file, module_name):
    """
    Recursively get test suite of all tests in a package and its child packages

    For this to work correctly you must build a specific hierarchy of test
    packages. Each package to be test should contain a test package. Each test
    package must contain a testall.py file, you can find them all over
    pytilities, just copy one of them, no changes are required. For example::

        pytilities
            test
                testall.py
            event
                test
                    testall.py
            ...

    Note that this may not work as expected::
        proj
            test
            p
                b
                    test
    
    Running tests from proj.test will not run tests from b. You must 'fill in 
    the gaps', i.e. p needs a test package as well to prevent the recursion to
    stop at p.

    Parameters:

        `module_file` :: string
            the testall.py file path. (use
            __file__)

        `module_name`:: string
            name of the calling module. (use __name__)

    Usage example:
        See pytilities.test (or any other test package)
    """
    package = ".".join(module_name.split(".")[:-1])
    current_dir = os.path.dirname(module_file)
    parent_dir = os.path.join(current_dir, "..")
    parent_package = ".".join(package.split(".")[:-1])
    test_loader = unittest.defaultTestLoader

    _logger.debug(" ".join((module_file, module_name, package,
                                      parent_package, current_dir)))
    _logger.debug(module_name)

    # grab test suites from child packages from our parent package, if any
    test_suite = test_loader.loadTestsFromNames(
        ".".join((parent_package, f, "test", "testall", "test_suite"))
        for f in os.listdir(parent_dir)
        if f[0] != "_" and f != "test"
           and os.path.isdir(os.path.join(parent_dir, f, "test")))

    _logger.debug([package + "." + os.path.splitext(f)[0]
            for f in os.listdir(current_dir)
           if f[0] != "_" and f != "testall.py" and f[-3:] == ".py"])

    # grab test suites from modules of current test package
    test_suite.addTest(
        test_loader.loadTestsFromNames(
            package + "." + os.path.splitext(f)[0]
            for f in os.listdir(current_dir)
            if f[0] != "_" and f != "testall.py" and f[-3:] == ".py"))

    return test_suite

def run(test):
    """
    Run test and print results to stderr

    Parameters:

        `test`
            the TestCase to run
    """
    runner = unittest.TextTestRunner()
    return runner.run(test)
