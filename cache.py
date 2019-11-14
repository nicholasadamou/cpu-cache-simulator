#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cache.py - represents a processor's main cache.
See README.md or https://github.com/nicholasadamou/cpu-cache-simulator
for more information.

Copyright (C) Nicholas Adamou 2019
cpu-cache-simulator is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

import random
from math import log

import util
from line import Line


class Cache:
    """Class representing a processor's main cache."""

    # Replacement policies
    LRU = "LRU"
    LFU = "LFU"
    FIFO = "FIFO"
    RAND = "RAND"

    # Mapping policies
    WRITE_BACK = "WB"
    WRITE_THROUGH = "WT"

    def __init__(self, size, memory_size, block_size, mapping_policy, replacement_policy, write_policy):
        self.size = size  # Cache size
        self.memory_size = memory_size  # Memory size
        self.block_size = block_size  # Block size

        self.mapping_policy = mapping_policy  # Mapping policy
        self.replacement_policy = replacement_policy  # Replacement policy
        self.write_policy = write_policy  # Write policy

        self.lines = [Line(block_size) for _ in range(self.size // self.block_size)]

        # bit offset of cache line tag
        self.tag_offset = int(log(self.size // self.mapping_policy, 2))
        # bit offset of cache line set
        self.set_offset = int(log(self.block_size, 2))

    def load(self, address, data):
        """
        Load a block of memory into the cache.

        :param int address: memory address for data to load to cache
        :param list data: block of memory to load into cache
        :return: tuple containing victim address and data (None if no victim)
        """

        tag = self.get_tag(address)
        set = self.get_set(address)

        index = 0
        victim = None

        # Select the victim based on replacement policy
        if (self.replacement_policy == Cache.LRU or
            self.replacement_policy == Cache.LFU or
            self.replacement_policy == Cache.FIFO):
            # Get the first line in the set
            victim = set[0]

            # Obtain the least used line in the set
            for index in range(len(set)):
                if set[index].use < victim.use:
                    victim = set[index]

            # Set the victims use bit to 0
            # to indicate that it is not used
            victim.use = 0

            # Update use bits of cache line
            if self.replacement_policy == Cache.FIFO:
                self.update_use(victim, set)

        # Obtain random line in the set if using RAND replacement policy
        elif self.replacement_policy == Cache.RAND:
            index = random.randint(0, self.mapping_policy - 1)
            victim = set[index]

        # Replace victim
        victim.modified = 0
        victim.valid = 1
        victim.tag = tag
        victim.data = data

        return (index, victim.data) if victim.modified else ()

    def read(self, address):
        """
        Read a block of memory from the cache.

        :param int address: memory address for data to read from cache
        :return: block of memory read from the cache (None if cache miss)
        """

        tag = self.get_tag(address)
        set = self.get_set(address)

        line = None

        # Search for cache line in set
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Update the use bits of this cache line
        if line:
            if self.replacement_policy == Cache.LRU or self.replacement_policy == Cache.LFU:
                self.update_use(line, set)

        return line.data if line else None

    def write(self, address, byte):
        """
        Write a byte to cache.

        :param int address: memory address for data to write to cache
        :param int byte: byte of data to write to cache
        :return: boolean indicating whether data was written to cache
        """

        tag = self.get_tag(address)
        set = self.get_set(address)

        line = None

        # Search for cache line in set
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Update the data of this cache line
        if line:
            line.data[self.get_offset(address)] = byte
            line.modified = 1

            if self.replacement_policy == Cache.LRU or self.replacement_policy == Cache.LFU:
                self.update_use(line, set)

        return True if line else False

    def print_section(self, start, amount):
        """
        Print a section of the cache.

        :param int start: start address to print from.
        :param int amount: amount of lines to print.
        """

        line_len = len(str(self.size // self.block_size - 1))
        use_len = max(
            [
                len(str(line.use)) for line in self.lines
            ]
        )
        tag_len = int(log((self.mapping_policy * self.memory_size) // self.size, 2))
        address_len = int(log(self.memory_size, 2))

        if start < 0 or (start + amount) > (self.size // self.block_size):
            raise IndexError

        print("\n" + " " * line_len + " " * use_len + "  U M V  T" + " " * tag_len + "<DATA @ ADDRESS>")
        for i in range(start, start + amount):
            print(
                "%s : %s %s %s %s <%s @ %s>" %
                (
                    util.dec_str(i, line_len),
                    util.dec_str(self.lines[i].use, use_len),
                    util.bin_str(self.lines[i].modified, 1),
                    util.bin_str(self.lines[i].valid, 1),
                    util.bin_str(self.lines[i].tag, tag_len),
                    " ".join(
                        [
                            util.hex_str(j, 2) for j in self.lines[i].data
                        ]
                    ),
                    util.bin_str(self.get_physical_address(i), address_len)
                )
            )
        print()

    def get_physical_address(self, index):
        """
        Get the physical address of the cache line at index.

        :param int index: index of cache line to get physical address of
        :return: physical address of cache line
        """

        set_number = index // self.mapping_policy

        tag = self.lines[index].tag << self.tag_offset
        set = set_number << self.set_offset

        return (
            tag + set
        )

    def get_offset(self, address):
        """
        Get the offset from within a set from a physical address.

        :param int address: memory address to get offset from.
        """

        return address & (self.block_size - 1)

    def get_tag(self, address):
        """
        Get the cache line tag from a physical address.

        :param int address: memory address to get tag from.
        """

        return address >> self.tag_offset

    def get_set(self, address):
        """
        Get a set of cache lines from a physical address.

        :param int address: memory address to get set from.
        """

        set_mask = (self.size // (self.block_size * self.mapping_policy)) - 1
        set_number = (address >> self.set_offset) & set_mask
        index = set_number * self.mapping_policy

        start = index
        end = index + self.mapping_policy

        return self.lines[start:end]

    def get_size(self):
        """
        Returns the size of the cache in bytes.

        :return: int Size of the cache in bytes.
        """

        return self.size

    def update_use(self, line, set):
        """
        Update the use bits of a given cache line.

        :param Line line: cache line to update use bits of.
        :param list set: the set to which this line belongs too.
        """

        if self.replacement_policy == Cache.LRU or self.replacement_policy == Cache.FIFO:
            use = line.use

            if line.use < self.mapping_policy:
                line.use = self.mapping_policy

                for other in set:
                    if other is not line and other.use > use:
                        other.use -= 1

        elif self.replacement_policy == Cache.LFU:
            line.use += 1
