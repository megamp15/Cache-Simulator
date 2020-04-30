# File: menu.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/30/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements the cache and the cache-menu commands.

# Imports
import random

# Global Variables
c = []  # List Structure for Cache
cache_hits = 0
cache_miss = 0
LFU_count_line0 = 0
LFU_count_line1 = 0
LFU_count_line2 = 0
LFU_count_line3 = 0


def cache(B, E, S):
    global c  # Updating cache c
    # Using for loops a matrix of lists creates the structure of the cache
    # Using S parameter we know the amount of sets in the entire cache
    for i in range(S):
        c.append([])
        # Using E parameter we know the amount of lines per set
        for e in range(E):
            c[i].append([])
            # Using B parameter we know the amount of bytes of data that is loaded on one line of a set.
            for b in range(B+4):
                if b == 0:
                    c[i][e].append("0")  # Valid Bit
                elif b == 1:
                    c[i][e].append("0")  # Dirty Bit
                elif b == 2:
                    c[i][e].append(0)  # Hidden LRU/LFU bit
                else:
                    c[i][e].append("00")  # Tag + B amounts of data Bytes


def cache_read(address, s, t, b, S, E, B, replace, RAM):
    # Updating global variables
    global cache_hits, cache_miss, c, LFU_count_line0, LFU_count_line1, LFU_count_line2, LFU_count_line3
    # Variables used in function
    hit = False
    # Converting address parameter into 8 bit binary string
    b_address = (bin(int(address[2:], 16))[2:].zfill(8))
    # Separating into different binary bits dependednt on computed parameters t, s, and b from config_cache
    tag = b_address[:int(t)]
    set_index = b_address[int(t):int(t)+int(s)]
    b_offset = b_address[int(t)+int(s):]
    # Fully Associative Cache: set_index = 0 otherwise convert set_index
    if set_index != "":
        print(f"set:{int(set_index, 2)}")
        # Converting set_index from binary string to decimal integer for access to cache list data structure
        si = int(set_index, 2)
    else:
        print(f"set:0")
        si = 0

    # If associativity is 1, tag is not needed if the cache size and block size are large.
    # Ex) 256 byte Cache size with 8 byte block size or 3 bits that produces 32 sets or 5 bits so t=8-(5+3)=0
    if tag != "":
        print(f"tag:{(hex(int(tag, 2)))[2:].upper()}")
    else:
        print("tag:")

    # Check lines in a certain set if valid bit is 1 and tags from address and cache match if there is a tag from address.
    # If there is a hit then we update hit variable to true, assign e to a variable and break out of the loop
    for e in range(E):
        if tag != "":
            if ((str(c[si][e][0]) == "1") and (str(c[si][e][3]).upper() == (str(hex(int(tag, 2)))[2:].zfill(2)).upper())):
                d_e = e
                hit = True
                break
        else:
            if ((str(c[si][e][0])) == "1"):
                d_e = e
                hit = True
                break
    # Cache Hit
    if(hit):
        cache_hits += 1  # Increase global variable for hit
        print("hit:yes")
        print("eviction_line:-1")
        print("ram_address:-1")
        print("data:0x"+c[si][d_e][int(b_offset, 2)+4])
        # LFU global variable updates depending on line hit.
        if replace == 3:
            if d_e == 0:
                LFU_count_line0 += 1
                c[si][0][2] = LFU_count_line0
            elif d_e == 1:
                LFU_count_line1 += 1
                c[si][1][2] = LFU_count_line1
            elif d_e == 2:
                LFU_count_line2 += 1
                c[si][2][2] = LFU_count_line2
            else:
                LFU_count_line3 += 1
                c[si][3][2] = LFU_count_line3
    # Cache Miss
    else:
        cache_miss += 1  # Increase global variable for miss
        print("hit:no")
        # implementation of hit policies. l is the line chosen starting from 1 to E that is reduced by 1 to access the correct index in the cache list data structure.
        if replace == 1:  # Random Replacement
            cnt = 0
            for e1 in range(E):
                if c[si][e1][0] == "1":  # Check to see if all lines are valid
                    cnt += 1
            if cnt != 4:  # If all lines are not valid we evict those lines
                while True:
                    l = random.randint(1, E)
                    if (c[si][l-1][0] == "0"):
                        break
            else:  # If all lines are valid we evict any at random.
                l = random.randint(1, E)
        elif replace == 2:  # Least Recently Used
            if E == 1:
                l = 1  # One line in set so we evict that line
            elif E == 2:
                # Use "Hidden" extra index in cache list data structure to select the line
                # The number of the index bit determines which line needs to be evicted. 0 == line 1 and 1 == line 2 in associativity of 2
                if c[si][0][2] == 0:
                    l = 1  # line to be evicted
                    # Update the bit to the opposite line
                    c[si][0][2] = 1
                else:
                    l = 2  # line to be evicted
                    # Update the bit to the opposite line
                    c[si][0][2] = 0
            else:
                # The least frequently used for associativity of 4 works in a circle where we evict the first line, then second, third, fourth, and then back to the first line
                if c[si][0][2] == 0:
                    # Checks if the index is equal to 0 to denote least recently used
                    l = 1
                    # Set index to 1 since it is not the least recently used anymore
                    c[si][0][2] = 1
                    # Set next index to 0 since that is next in line to be evicted
                    c[si][1][2] = 0
                # Repeats for all lines
                elif c[si][1][2] == 0:
                    l = 2
                    c[si][1][2] = 1
                    c[si][2][2] = 0
                elif c[si][2][2] == 0:
                    l = 3
                    c[si][2][2] = 1
                    c[si][3][2] = 0
                else:
                    l = 4
                    c[si][3][2] = 1
                    # We go back and set first line to 0 to denote least recently used
                    c[si][0][2] = 0
        else:
            # Extra Credit - Least Frequently Used
            if E == 1:
                l = 1  # One line in set so we evict that line
            elif E == 2:
                # Between the two line which LFU hidden index has the minimum frequency. Frequency is set to 1 if its miss since it is only in the cache at that moment. Increases with cache read or write.
                if c[si][0][2] == min(c[si][0][2], c[si][1][2]):
                    l = 1
                    LFU_count_line0 = 1
                    # The first line "hidden" LFU bit is set to 1.
                    c[si][0][2] = LFU_count_line0
                else:
                    l = 2
                    LFU_count_line1 = 1
                    # The second line "hidden" LFU bit is set to 1.
                    c[si][1][2] = LFU_count_line1
            else:
                if c[si][0][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 1
                    LFU_count_line0 = 1
                    # The first line "hidden" LFU bit is set to 1.
                    c[si][0][2] = LFU_count_line0
                elif c[si][1][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 2
                    LFU_count_line1 = 1
                    # The second line "hidden" LFU bit is set to 1.
                    c[si][1][2] = LFU_count_line1
                elif c[si][2][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 3
                    LFU_count_line2 = 1
                    # The third line "hidden" LFU bit is set to 1.
                    c[si][2][2] = LFU_count_line2
                else:
                    l = 4
                    LFU_count_line3 = 1
                    # The fourth line "hidden" LFU bit is set to 1.
                    c[si][3][2] = LFU_count_line3

        print(f"eviction_line:{l}")
        c[si][l-1][0] = "1"  # Access the line in the set and make the valid bit to 1
        if tag != "":
            # Set tag in cache list if there is a tag as stated before.
            c[si][l-1][3] = str(hex(int(tag, 2)))[2:].zfill(2).upper()
        for b in range(4, B+4):
            # Set the B bytes of data from RAM
            c[si][l-1][b] = RAM["0x" +
                                (hex((int(address[2:], 16)-int(b_offset, 2))+(b-4))[2:].zfill(2)).upper()]
        print(f"ram_address:{address}")  # Address passed in
        print("data:0x"+RAM[address])  # Data at the address in RAM


def cache_write(address, data, s, t, b, S, E, B, replace, RAM, write_hit, write_miss):
    # Similar to Cache Read
    global cache_hits, cache_miss, c, LFU_count_line0, LFU_count_line1, LFU_count_line2, LFU_count_line3
    hit = False
    b_address = (bin(int(address[2:], 16))[2:].zfill(8))
    tag = b_address[:int(t)]
    set_index = b_address[int(t):int(t)+int(s)]
    b_offset = b_address[int(t)+int(s):]
    if set_index != "":
        print(f"set:{int(set_index, 2)}")
        si = int(set_index, 2)
    else:
        print(f"set:0")
        si = 0

    if tag != "":
        print(f"tag:{(hex(int(tag, 2)))[2:].upper()}")
    else:
        print("tag:")

    # Checking whether there's a hit
    for e in range(E):
        if tag != "":
            if ((str(c[si][e][0]) == "1") and (str(c[si][e][3]).upper() == (str(hex(int(tag, 2)))[2:].zfill(2)).upper())):
                d_e = e
                hit = True
                break
        else:
            if ((str(c[si][e][0])) == "1"):
                d_e = e
                hit = True
                break
    # Write Hit
    if(hit):
        cache_hits += 1  # Increase global variable for hit
        print("write_hit:yes")
        print("eviction_line:-1")
        print("ram_address:-1")
        print(f"data:{data}")

        c[si][d_e][int(b_offset, 2)+4] = data[2:]
        if write_hit == 1:
            RAM[address] = data[2:]
        else:
            c[si][d_e][1] = 1  # Dirty bit
        # LFU global variable updates depending on line hit.
        if replace == 3:
            if d_e == 0:
                LFU_count_line0 += 1
                c[si][0][2] = LFU_count_line0
            elif d_e == 1:
                LFU_count_line1 += 1
                c[si][1][2] = LFU_count_line1
            elif d_e == 2:
                LFU_count_line2 += 1
                c[si][2][2] = LFU_count_line2
            else:
                LFU_count_line3 += 1
                c[si][3][2] = LFU_count_line3
        print(f"dirty_bit:{c[si][d_e][1]}")

    # Write Miss
    else:
        cache_miss += 1  # Increase global variable for miss
        print("write_hit:no")
        if replace == 1:  # Random Replacement
            cnt = 0
            for e1 in range(E):
                if c[si][e1][0] == "1":  # Check to see if all lines are valid
                    cnt += 1
            if cnt != 4:  # If all lines are not valid we evict those lines
                while True:
                    l = random.randint(1, E)
                    if (c[si][l-1][0] == "0"):
                        break
            else:  # If all lines are valid we evict any at random.
                l = random.randint(1, E)
        elif replace == 2:  # Least Recently Used
            if E == 1:
                l = 1  # evict line
            elif E == 2:
                # Use "Hidden" extra index in cache list data structure to select the line
                # The number of the index bit determines which line needs to be evicted
                if c[si][0][2] == 0:
                    l = 1  # evicted line
                    # Update the bit to the opposite line
                    c[si][0][2] = 1
                else:
                    l = 2  # evicted line
                    # Update the bit to the opposite line
                    c[si][0][2] = 0
            else:
                if c[si][0][2] == 0:
                    # Checks if the index is equal to 0
                    l = 1
                    # Set index to 1
                    c[si][0][2] = 1
                    # Set next index to 0
                    c[si][1][2] = 0
                # Repeats for all lines
                elif c[si][1][2] == 0:
                    l = 2
                    c[si][1][2] = 1
                    c[si][2][2] = 0
                elif c[si][2][2] == 0:
                    l = 3
                    c[si][2][2] = 1
                    c[si][3][2] = 0
                else:
                    l = 4
                    c[si][3][2] = 1
                    # We go back and set first line to 0 to denote least recently used
                    c[si][0][2] = 0
        else:
            # Extra Credit - Least Frequently Used
            if E == 1:
                l = 1  # Evict line
            elif E == 2:
                if c[si][0][2] == min(c[si][0][2], c[si][1][2]):
                    l = 1
                    LFU_count_line0 = 1
                    # The first line "hidden" LFU bit is set to 1.
                    c[si][0][2] = LFU_count_line0
                else:
                    l = 2
                    LFU_count_line1 = 1
                    # The second line "hidden" LFU bit is set to 1.
                    c[si][1][2] = LFU_count_line1
            else:
                if c[si][0][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 1
                    LFU_count_line0 = 1
                    # The first line "hidden" LFU bit is set to 1.
                    c[si][0][2] = LFU_count_line0
                elif c[si][1][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 2
                    LFU_count_line1 = 1
                    # The second line "hidden" LFU bit is set to 1.
                    c[si][1][2] = LFU_count_line1
                elif c[si][2][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 3
                    LFU_count_line2 = 1
                    # The third line "hidden" LFU bit is set to 1.
                    c[si][2][2] = LFU_count_line2
                else:
                    l = 4
                    LFU_count_line3 = 1
                    # The fourth line "hidden" LFU bit is set to 1.
                    c[si][3][2] = LFU_count_line3

        if write_miss == 1:
            print(f"eviction_line:{l}")
            # Access the line in the set
            # Make the valid bit to 1
            c[si][l-1][0] = "1"
            if tag != "":
                # Set tag in cache list 
                c[si][l-1][3] = str(hex(int(tag, 2)))[2:].zfill(2).upper()
            for b in range(4, B+4):
                # Set the B bytes of data from RAM
                c[si][l-1][b] = RAM["0x" +
                                    (hex((int(address[2:], 16)-int(b_offset, 2))+(b-4))[2:].zfill(2)).upper()]

            c[si][l-1][int(b_offset, 2)+4] = data[2:]
            if write_hit == 1:
                RAM[address] = data[2:]
            else:
                c[si][l-1][1] = 1  # setting dirty bit
            print(f"ram_address:{address}")  # Address passed in
            print("data:0x"+RAM[address])  # Data at the address in RAM
            print(f"dirty_bit:{c[si][l-1][1]}")
        else:
            RAM[address] = data[2:]
            print(f"eviction_line:{-1}")
            print(f"ram_address:{address}")  # Address passed in
            print("data:0x"+RAM[address])  # Data at the address in RAM
            print("dirty_bit:0")  # Dirty bit set to 0


def cache_flush(B, E, S):
    # Go through same looping structure with the same parameters as cache function but set all indices to 0 or 00.
    # Does not overide global variable like cache_miss, cache_hit and the LFU variables
    for i in range(S):
        for e in range(E):
            for b in range(B+4):
                if b == 0:
                    c[i][e][b] = "0"
                elif b == 1:
                    c[i][e][b] = "0"
                elif b == 2:
                    c[i][e][b] = "0"
                else:
                    c[i][e][b] = "00"
    print("cache_cleared")


def cache_view(B, E, S, C, replace, write_hit, write_miss):
    # Convert the config cache numbers for choosing policies to there meaning for printing
    if replace == 1:
        R = "random replacement"
    elif replace == 2:
        R = "least recently used"
    else:
        R = "least frequently used"
    if write_hit == 1:
        WH = "write-through"
    else:
        WH = "write-back"
    if write_miss == 1:
        WM = "write-allocate"
    else:
        WM = "no write-allocate"

    # Printing information about Cache
    print(f"cache_size:{C}")
    print(f"data_block_size:{B}")
    print(f"associativity:{E}")
    print(f"replacement_policy:{R}")
    print(f"write_hit_policy:{WH}")
    print(f"write_miss_policy:{WM}")
    print(f"number_of_cache_hits:{cache_hits}")
    print(f"number_of_cache_misses:{cache_miss}")
    print("cache_content:")
    # Using same structure as cache to print the cache list structure
    for i in range(S):
        for e in range(E):
            for b in range(B+4):
                if b != 2:  # Skips the LFU/LRU index which is why it is "hidden"
                    print(c[i][e][b], end=" ")
            print("")


def memory_view(RAM, count):
    # Print Memory information
    print(f"memory_size:{count}")
    print("memory_content:")
    print("Address:Data", end="")
    # Print address then 8 bytes until newline with repeating format
    count = 0
    for r in RAM:
        if count % 8 == 0:
            print(f"\n{r}:", end="")
        print(RAM[r], end=" ")
        count += 1
    print("")


def cache_dump(B, E, S):
    # Create/Open cache.txt and write the cache data bytes.
    o = open("cache.txt", "w")
    for i in range(S):
        for e in range(E):
            for b in range(4, B+4):  # Start at the first index 4 of the data Bytes in the cache
                o.write(c[i][e][b]+" ")
            o.write("\n")


def memory_dump(RAM):
    # Create/Open ram.txt and write the data in the RAM data structure.
    o = open("ram.txt", "w")
    for r in RAM:
        o.write(RAM[r]+"\n")