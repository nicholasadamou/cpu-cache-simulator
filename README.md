<h1 align="center">
  <br>
  <a href="https://github.com/nicholasadamou/cpu-cache-simulator"><img src="https://cdn1.iconfinder.com/data/icons/modern-future-technology/128/computer-chip2-2-512.png" alt="Logo" width="15%"></a>
  <br>
  cpu-cache-simulator
  <br>
</h1>

<h4 align="center">A python-based simulator for a CPU cache that I wrote for <em>CSC 218 Computer Organization</em></h4>

<p align="center">
	<img src="https://img.shields.io/badge/Course-Assignment-blue" alt="Course Project" />
    <a href="https://github.com/nicholasadamou/cpu-cache-simulator/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/license-Apachev2-blue" alt="Course Project" />
    </a>
    <a href="https://saythanks.io/to/NicholasAdamou">
        <img src="https://img.shields.io/badge/say-thanks-ff69b4.svg" alt="Say Thanks">
    </a>
</p>

---

## 🤔 What is '_cpu-cache-simulator_'?

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

### Usage

```shell script
Commands
usage: COMMAND PARAM PARAM
* ADDRESS, BYTE, & AMOUNT must be an integer

write ADDRESS BYTE - write byte from memory
read ADDRESS - read byte from memory
randwrite AMOUNT - write random byte to random location in memory AMOUNT times
randread AMOUNT - read byte from random location in memory AMOUNT times
printcache START LENGTH - print LENGTH lines of cache from START
printmem START LENGTH - print LENGTH blocks of memory from START
stats - print out hits, misses, and hit/miss ratio
help - prints this message
quit - quit the simulator
```

## Example

Here is an example run:

[![asciicast](https://asciinema.org/a/YJhd8610I4Mmhyrl9vfLcwBTq.svg)](https://asciinema.org/a/YJhd8610I4Mmhyrl9vfLcwBTq)

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
