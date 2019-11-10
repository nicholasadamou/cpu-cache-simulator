#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""simulator.py - main driver program of cpu-cache-simulator.
See README.md or https://github.com/nicholasadamou/cpu-cache-simulator
for more information.

Copyright (C) Nicholas Adamou 2019
cpu-cache-simulator is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

from pyfiglet import Figlet

from math import log

import util

try:
    import gnureadline as readline
except ImportError:
    import readline

from cache import Cache
from memory import Memory

INVALID_RESPONSE = "\nERROR: invalid response, try again.\n"
OUT_OF_BOUNDS_ERROR = "\nERROR: out of bounds\n"
INCORRECT_SYNTAX_ERROR = "\nERROR: incorrect syntax\n"

REPLACEMENT_POLICIES = ["LRU", "LFU", "FIFO", "RAND"]
WRITE_POLICIES = ["WB", "WT"]


class Simulator:
    """Class modeling the processor cache simulator"""

    def __init__(self, memory_size, cache_size, block_size, mapping_policy, replacement_policy, write_policy):
        self.memory_size = memory_size
        self.cache_size = cache_size
        self.block_size = block_size
        self.mapping_policy = mapping_policy
        self.replacement_policy = replacement_policy
        self.write_policy = write_policy

        self.hits = 0
        self.misses = 0

        self.memory = Memory(
            2 ** memory_size,
            2 ** block_size
        )
        self.cache = Cache(
            2 ** cache_size,
            2 ** memory_size,
            2 ** block_size,
            2 ** mapping_policy,
            replacement_policy,
            write_policy
        )

    def run(self):
        command = None

        self.print_details()

        while command != 'quit':
            operation = input("Enter a command > ")
            operation = operation.split()

            try:
                command = operation[0]
                params = operation[1:]

                if command == 'write' and len(params) == 2:
                    address = int(params[0])
                    byte = int(params[1])

                    self.write(address, byte)

                elif command == 'read' and len(params) == 1:
                    address = int(params[0])
                    byte = self.read(address)

                    print(
                        "\nByte 0x%s (%s) read from %s cache\n" % (
                            util.hex_str(byte, 2),
                            byte,
                            util.bin_str(address, self.memory_size)
                        )
                    )

                elif command == "printcache" and len(params) == 2:
                    start = int(params[0])
                    amount = int(params[1])

                    self.cache.print_section(start, amount)

                elif command == "printmem" and len(params) == 2:
                    start = int(params[0])
                    amount = int(params[1])

                    self.memory.print_section(start, amount)

                elif command == "stats" and len(params) == 0:
                    ratio = (self.hits / ((self.hits + self.misses) if self.misses else 1)) * 100

                    print("\nHits: {0} | Misses: {1}".format(self.hits, self.misses))
                    print("Hit/Miss Ratio: {0:.2f}%".format(ratio) + "\n")

                elif command == 'help':
                    self.print_details()

                elif command != 'quit':
                    print(INVALID_RESPONSE)
            except IndexError:
                print(OUT_OF_BOUNDS_ERROR)
            except:
                print(INCORRECT_SYNTAX_ERROR)

    def read(self, address):
        """Read a byte from cache."""

        cache_block = self.cache.read(address)

        if cache_block:
            self.hits += 1
        else:
            block = self.memory.get_block(address)
            victim = self.cache.load(address, block)
            cache_block = self.cache.read(address)

            self.misses += 1

            # Write victim line's block to memory if replaced
            if victim:
                self.memory.set_block(victim[0], victim[1])

        return cache_block[self.cache.get_offset(address)]

    def write(self, address, byte):
        """Write a byte to cache."""

        written = self.cache.write(address, byte)

        if written:
            self.hits += 1
        else:
            self.misses += 1

        if self.write_policy == Cache.WRITE_THROUGH:
            # Write block to memory
            block = self.memory.get_block(address)

            block[self.cache.get_offset(address)] = byte

            self.memory.set_block(address, block)

            print()
            print("Byte 0x%s (%s) written to block %s @ %s in main memory\n" % (
                    util.hex_str(byte, 2),
                    byte,
                    self.memory.get_block(address),
                    util.bin_str(address, self.memory_size)
                )
            )

        elif self.write_policy == Cache.WRITE_BACK:
            if not written:
                # Write block to cache
                block = self.memory.get_block(address)

                self.cache.load(address, block)
                self.cache.write(address, byte)

                print()
                print("Byte 0x%s (%s) written to block %s @ %s in cache\n" % (
                        util.hex_str(byte, 2),
                        byte,
                        block,
                        util.bin_str(address, self.memory_size)
                    )
                )
            else:
                # address was already previously written too,
                # simply overriding current value held @ that
                # address

                print()
                print("Byte 0x%s (%s) written @ %s in cache\n" % (
                        util.hex_str(byte, 2),
                        byte,
                        util.bin_str(address, self.memory_size)
                    )
                )

    def print_details(self):
        """
        Print the details of the simulation.
        """

        mapping_str = "2^%s-way set associative" % self.mapping_policy
        print()
        print("Main Memory")
        print("Memory size: %s bytes (%s blocks)" % (
                str(self.memory.get_size()),
                str(self.memory.get_size() // self.memory.get_block_size())
            )
        )
        print("Block size: %s bytes" % str(self.memory.get_block_size()))
        print()

        print("Cache")
        print("Cache size: %s bytes (%s lines, %s-bit addresses)" % (
                str(self.cache.get_size()),
                str(self.cache.get_size() // self.memory.get_block_size()),
                str(int(log(self.memory.get_size(), 2)))
            )
        )
        print()

        print("Policies")
        print("Mapping policy: %s" % ("direct" if self.mapping_policy == 0 else mapping_str))
        print("Replacement policy: %s" % self.replacement_policy)
        print("Write policy: %s" % self.write_policy)
        print()

        print(
            "Commands\n" +
            "usage: COMMAND PARAM PARAM\n\n" +
            "write ADDRESS BYTE - write byte from memory (byte must be an integer)\n" +
            "read ADDRESS - read byte from memory (byte must be an integer)\n" +
            "printcache START LENGTH - print LENGTH lines of cache from START\n" +
            "printmem START LENGTH - print LENGTH blocks of memory from START\n" +
            "stats - print out hits, misses, and hit/miss ratio\n" +
            "help - prints this message\n" +
            "quit - quit the simulator\n"
        )


if __name__ == '__main__':
    custom_fig = Figlet(font='slant')
    print(custom_fig.renderText('cpu cache simulator'))
    print("This is a simulator for a CPU cache that I wrote for CSC 218 Computer Organization.\n" +
          "It's meant to demonstrate some of the different replacement, write, \n" +
          "and mapping policies that CPUs can implement.\n")

    memory_size = 0
    cache_size = 0
    block_size = 0

    mapping_policy = 0
    replacement_policy = ""
    write_policy = ""

    while True:
        response = input("Size of Main Memory (in 2^N bytes) > ")

        if response.isdigit():
            memory_size = int(response)
            break

        print(INVALID_RESPONSE)

    while True:
        response = input("Size of Cache (in 2^N bytes) > ")

        if response.isdigit():
            cache_size = int(response)
            break

        print(INVALID_RESPONSE)

    while True:
        response = input("Size of a block of memory (in 2^N bytes) > ")

        if response.isdigit():
            block_size = int(response)
            break

        print(INVALID_RESPONSE)

    while True:
        response = input("Mapping policy for cache (in 2^N ways) > ")

        if response.isdigit():
            mapping_policy = int(response)
            break

        print(INVALID_RESPONSE)

    while True:
        response = input("Replacement policy for cache {" + ", ".join(REPLACEMENT_POLICIES) + "} > ")

        if any(policy.lower() == response.lower() for policy in REPLACEMENT_POLICIES):
            replacement_policy = response
            break

        print(INVALID_RESPONSE)

    while True:
        response = input("Write policy for cache {" + ", ".join(WRITE_POLICIES) + "} > ")

        if any(policy.lower() == response.lower() for policy in WRITE_POLICIES):
            write_policy = response
            break

        print(INVALID_RESPONSE)

    simulator = Simulator(
        memory_size,
        cache_size,
        block_size,
        mapping_policy,
        replacement_policy,
        write_policy
    )

    simulator.run()
