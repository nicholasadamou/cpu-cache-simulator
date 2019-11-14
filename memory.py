#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""memory.py - represents the main memory as an array of bytes.
See README.md or https://github.com/nicholasadamou/cpu-cache-simulator
for more information.

Copyright (C) Nicholas Adamou 2019
cpu-cache-simulator is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

import util


class Memory:
    """Class representing main memory as an array of bytes."""

    def __init__(self, size, block_size):
        """Initialize main memory with a set number of bytes and block size."""

        self.size = size
        self.block_size = block_size

        self.data = [util.rand_byte() for _ in range(size)]

    def get_block(self, address):
        """
        Get the block of main memory (of self.block_size) that contains the byte address.

        :param address: address of byte in block of memory.
        :return: block of memory.
        """

        start = address - (address % self.block_size)  # start address
        end = start + self.block_size  # end address

        if start < 0 or end > self.size:
            raise IndexError

        block = self.data[start:end]

        return block

    def set_block(self, address, data):
        """
        Set the block of main memory (of self.block_size) that contains the byte address.

        :param address: address of byte in block of memory.
        :param data: bytes to set as block of memory.
        :return: block of memory.
        """

        start = address - (address % self.block_size)  # start address
        end = start + self.block_size  # end address

        if start < 0 or end > self.size:
            raise IndexError

        self.data[start:end] = data

    def get_size(self):
        """
        Returns the size of the memory in bytes.

        :return: int The size of the memory in bytes.
        """

        return self.size

    def get_block_size(self):
        """
        Returns the size of a block of memory in bytes.

        :return: int The size of a block of memory in bytes.
        """

        return self.block_size

    def print_section(self, start, amount):
        """
        Print a section of main memory.

        :param int start: start address to print from.
        :param int amount: amount of blocks to print.
        """

        address_length = len(str(self.size - 1))
        start = start - (start % self.block_size)
        amount *= self.block_size

        if start < 0 or (start + amount) > self.size:
            raise IndexError

        print()
        for i in range(start, start + amount, self.block_size):
            print(
                '%s:%s' %
                (
                    util.dec_str(i, address_length),
                    " ".join(
                        [
                            util.hex_str(j, 2) for j in self.get_block(i)
                        ]
                    )
                )
            )
        print()
