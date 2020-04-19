# File: project.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/19/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements ...

import argparse
import menu
RAM = {}


def init_ram(input):
    print("initialize the RAM:")
    print("init-ram 0x00 0xFF")
    i = open(input, "r")
    count = 0
    for l in i.read().splitlines():
        RAM[str(hex(count))] = l
        count += 1
    i.close()
    print("ram successfully initialized!")


def config_cache():
    global c_size, block_size, associativity, replace, write_hit, write_miss
    print("\nconfigure the cache:")
    c_size = int(input("cache size: "))
    block_size = int(input("data block size: "))
    associativity = int(input("associativity: "))
    replace = int(input("replacement policy: "))
    write_hit = int(input("write hit policy: "))
    write_miss = int(input("write miss policy: "))
    print("cache successfully configured!")


def simulate_cache():
    print("\n*** Cache simulator menu ***")
    print("type one command: ")
    print("1. cache-read")
    print("2. cache-write")
    print("3. cache-flush")
    print("4. cache-view")
    print("5. memory-view")
    print("6. cache-dump")
    print("7. memory-dump")
    print("8. quit")
    print("****************************")
    command = ""
    while(command != "quit"):
        command = input("")
        if command == "cache-read":
            menu.cache_read()
        if command == "cache-write":
            menu.cache_write()
        if command == "cache-flush":
            menu.cache_flush()
        if command == "cache-view":
            menu.cache_view()
        if command == "memory-view":
            menu.memory_view()
        if command == "cache-dump":
            menu.cache_dump()
        if command == "memory-dump":
            menu.memory_dump()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file for initializing the physical memory.",
        type=str,
    )
    args = parser.parse_args()

    print("*** Welcome to the cache simulator ***")
    # init_ram(args.input)
    # config_cache()
    simulate_cache()


if __name__ == "__main__":
    main()
