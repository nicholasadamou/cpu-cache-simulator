# cpu-cache-simulator

This is a simulator for a CPU cache that I wrote for CSC 218 Computer Organization. It's
meant to demonstrate some of the different
[replacement](https://en.wikipedia.org/wiki/CPU_cache#Replacement_policies),
[write](https://en.wikipedia.org/wiki/CPU_cache#Write_policies), and [mapping
policies](https://en.wikipedia.org/wiki/CPU_cache#Associativity) that CPUs can
implement.

To run the CPU cache simulator:

```shell script
python3 simulator.py
```

Once you start the simulator, you can enter commands to modify and read from the memory (which is randomized on initialization), and therefore indirectly modify the cache. You can also print the contents of the memory and cache, as well as view statistics about the cache's performance.

## Commands

**read** ADDRESS - read byte from memory (byte must be an int)

**write** ADDRESS BYTE - write random byte to memory (byte must be an int)

**printcache** START LENGTH - print LENGTH lines of cache from START

**printmem** START LENGTH - print LENGTH blocks of memory from START

**stats** - print out hits, misses, and hit/miss ratio

**help** - prints out this list of commands as well as simulation details

**quit** - quit the simulator

## Example

Here is an example run:

[![asciicast](https://asciinema.org/a/hdSIiyETobky13pCOzzMwKjeV.svg)](https://asciinema.org/a/hdSIiyETobky13pCOzzMwKjeV)

## License

Copyright 2019 Nicholas Adamou

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
