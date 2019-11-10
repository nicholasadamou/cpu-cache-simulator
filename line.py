#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""line.py - represents a line within a processor's main cache.
See README.md or https://github.com/nicholasadamou/cpu-cache-simulator
for more information.

Copyright (C) Nicholas Adamou 2019
stockmine is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

class Line:
    """Class representing a line within a processor's main cache."""

    def __init__(self, size):
        self.use = 0
        self.modified = 0
        self.valid = 0
        self.tag = 0
        self.data = [0] * size
