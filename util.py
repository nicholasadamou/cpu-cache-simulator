#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""util.py - utility functions.
See README.md or https://github.com/nicholasadamou/cpu-cache-simulator
for more information.

Copyright (C) Nicholas Adamou 2019
stockmine is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

import random


def rand_byte():
    """
    Get a random byte.
    :return: random byte (integer from 0 - 255)
    """

    return random.randint(0, 0xFF)


def dec_str(integer, width):
    """
    Get decimal formatted string representation of an integer.

    :param int integer: integer to be converted to decimal string.
    :return: decimal string representation of integer.
    """

    return "{0:0{1}}".format(integer, width)


def bin_str(integer, width):
    """
    Get binary formatted string representation of an integer.

    :param int integer: integer to be converted to binary string.
    :return: binary string representation of integer.
    """

    return "{0:0{1}b}".format(integer, width)


def hex_str(integer, width):
    """
    Get hexadecimal formatted string representation of an integer.

    :param int integer: integer to be converted to hexadecimal string.
    :return: hexadecimal string representation of integer.
    """

    return "{0:0{1}X}".format(integer, width)
