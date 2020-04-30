# File: cachesimulator.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/30/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements the main functions of the cachesimulator:
# Initializing the Ram in the init_ram function using the input file from command line argument.
# Configuring the Cache in the config_cache function by asking input from command line.
# Simulating the cache in the simulate_cache() function which holds the menu and calls functions in the menu.py.

# Imports
import argparse
import math
import menu  # import of menu.py file

# Global variables
RAM = {}  # Dictionary structure for RAM
m = 8
count = 0


def init_ram(input):
    global count
    print("initialize the RAM:")
    print("init-ram 0x00 0xFF")
    i = open(input, "r")
    for l in i.read().splitlines():
        # Count is converted to hex which is the key in the RAM dictionary with value being the current line l from input.
        RAM["0x"+(str(hex(count))[2:].zfill(2)).upper()] = l
        count += 1
    i.close()
    print("ram successfully initialized!")


def config_cache():
    # Global variables that are used in menu.py functions
    global C, B, E, replace, write_hit, write_miss, S, s, b, t
    print("configure the cache:")
    # Inputs
    C = int(input("cache size: "))
    B = int(input("data block size: "))
    E = int(input("associativity: "))
    replace = int(input("replacement policy: "))
    write_hit = int(input("write hit policy: "))
    write_miss = int(input("write miss policy: "))
    print("cache successfully configured!")
    # Computations for menu.py functions
    S = int(C/(B*E))
    s = math.log2(S)
    b = math.log2(B)
    t = m-(s+b)
    # Initializing the cache using the menu.cache function
    menu.cache(B, E, S)


def simulate_cache():
    command = ""
    while(command != "quit"):  # Until the command quit is received.
        # MENU
        print("*** Cache simulator menu ***")
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
        # command input
        command = input("")
        # Calls to menu.py functions and passing command arguments and global variables
        if "cache-read" in command:
            menu.cache_read(command[command.find(
                " ")+1:].strip(), s, t, b, S, E, B, replace, RAM)
        elif "cache-write" in command:
            temp = command[command.find(" ")+1:]
            menu.cache_write(temp[: temp.find(" ")].strip(),
                             temp[temp.find(" ")+1:].strip(), s, t, b, S, E, B, replace, RAM, write_hit, write_miss)
        elif "cache-flush" in command:
            menu.cache_flush(B, E, S)
        elif "cache-view" in command:
            menu.cache_view(B, E, S, C, replace, write_hit, write_miss)
        elif "memory-view" in command:
            menu.memory_view(RAM, count)
        elif "cache-dump" in command:
            menu.cache_dump(B, E, S)
        elif "memory-dump" in command:
            menu.memory_dump(RAM)
        else:
            if command != "quit":  # Incase a incorrect menu command is received.
                print("Not a command. Please type one command from the menu.")


def main():
    # Main function that is called when running program.
    # Takes the input file as a command line argument that is passed to init_ram.
    # Config_cache is then called to trigger input from command line.
    # Simulate_cache is called to start the menu and do commands until quit command is entered.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file for initializing the physical memory.",
        type=str
    )
    args = parser.parse_args()

    print("*** Welcome to the cache simulator ***")
    init_ram(args.input)
    config_cache()
    simulate_cache()


if __name__ == "__main__":
    main()
