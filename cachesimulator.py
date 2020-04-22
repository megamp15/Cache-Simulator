# File: project.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/19/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements ...

import argparse
import math
import menu
RAM = {}
m = 8


def init_ram(input):
    print("initialize the RAM:")
    print("init-ram 0x00 0xFF")
    i = open(input, "r")
    count = 0
    for l in i.read().splitlines():
        RAM[str(hex(count))] = l
        count += 1
    i.close()
    # print(RAM)
    # for r in RAM:
    #     print(r, RAM[r])
    print("ram successfully initialized!")


def config_cache():
    global C, B, E, replace, write_hit, write_miss, S
    print("\nconfigure the cache:")
    C = int(input("cache size: "))
    B = int(input("data block size: "))
    E = int(input("associativity: "))
    replace = int(input("replacement policy: "))
    write_hit = int(input("write hit policy: "))
    write_miss = int(input("write miss policy: "))
    print("cache successfully configured!")
    S = int(C/(B*E))
    s = math.log2(S)
    b = math.log2(B)
    t = m-(s+b)
    # print(s)
    # print(b)
    # print(t)
    menu.cache(B, E, S)


def simulate_cache():
    command = ""
    while(command != "quit"):
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
        command = input("")
        if "cache-read" in command:
            menu.cache_read(command[command.find(" ")+1:].strip())
        elif "cache-write" in command:
            temp = command[command.find(" ")+1:]
            menu.cache_write(temp[: temp.find(" ")].strip(),
                             temp[temp.find(" ")+1:].strip())
        elif "cache-flush" in command:
            menu.cache_flush(B, E, S)
        elif "cache-view" in command:
            menu.cache_view(B, E, S)
        elif "memory-view" in command:
            menu.memory_view()
        elif "cache-dump" in command:
            menu.cache_dump()
        elif "memory-dump" in command:
            menu.memory_dump()
        else:
            if command != "quit":
                print("Not a command. Please type one command from the menu above.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file for initializing the physical memory.",
        type=str,
    )
    args = parser.parse_args()

    print("*** Welcome to the cache simulator ***")
    init_ram(args.input)
    config_cache()
    simulate_cache()


if __name__ == "__main__":
    main()
