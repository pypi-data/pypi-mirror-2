#!/usr/bin/env python

#
# Runs all unit tests
#

import logging
import os

# Set up logging
# Note that this has to happen before we import stuff (as things may already go
# wrong by importing things)
logger = logging.getLogger("pytilities")
handler = logging.StreamHandler()  # defaults to stderr
logger.addHandler(handler)

# Uncomment to see log output
logging.getLogger("pytilities.testing").setLevel(logging.DEBUG)

# More imports (have to be placed after logging activation code, to detect even
# the earliest fails)
from pytilities.testing import get_recursive_package_test
import pytilities.testing

# Run unit tests
def run(test_root):
    return pytilities.testing.run(
        get_recursive_package_test(
            os.path.dirname(
                os.path.join(os.getcwd(),
                             __file__)),
            test_root))

if __name__ == '__main__':
    run('pytilities.test')
