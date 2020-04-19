# File: project.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/19/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements ...

import argparse

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
    pass


def simulate_cache():
    pass


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


if __name__ == "__main__":
    main()
