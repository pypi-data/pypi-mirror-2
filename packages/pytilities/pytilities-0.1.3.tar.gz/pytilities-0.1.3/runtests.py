#!/usr/bin/env python

#
# Runs all unit tests
#

import logging

# Set up logging
# Note that this has to happen before we import stuff (as things may already go
# wrong by importing things)
logger = logging.getLogger("pytilities")
handler = logging.StreamHandler()  # defaults to stderr
logger.addHandler(handler)

# Uncomment to see log output
#logging.getLogger("pytilities").setLevel(logging.DEBUG)


# Run unit tests
from pytilities.test.testall import run
run()

