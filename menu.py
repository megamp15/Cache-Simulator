# File: menu.py
# Author(s): Mahir Pirmohammed, Ashok Meyyappan
# Date: 04/19/2020
# Section: 510
# E-mail: megamp15@tamu.edu
# Description:
# e.g. The content of this file implements the cache and the cache-menu commands.

import random

c = []
cache_hits = 0
cache_miss = 0
LFU_count_line0 = 0
LFU_count_line1 = 0
LFU_count_line2 = 0
LFU_count_line3 = 0


def cache(B, E, S):
    global c
    for i in range(S):
        c.append([])
        for e in range(E):
            c[i].append([])
            for b in range(B+4):
                if b == 0:
                    c[i][e].append("0")
                elif b == 1:
                    c[i][e].append("0")
                elif b == 2:
                    c[i][e].append(0)
                else:
                    c[i][e].append("00")


def cache_read(address, s, t, b, S, E, B, replace, RAM):
    global cache_hits, cache_miss, c, LFU_count_line0, LFU_count_line1, LFU_count_line2, LFU_count_line3
    hit = False
    b_address = (bin(int(address[2:], 16))[2:].zfill(8))
    tag = b_address[:int(t)]
    set_index = b_address[int(t):int(t)+int(s)]
    b_offset = b_address[int(t)+int(s):]
    # print(b_address)
    # print(tag)
    # print(set_index)
    # print(b_offset)
    # print(LFU_count_line0)
    # print(LFU_count_line1)
    # print(LFU_count_line2)
    # print(LFU_count_line3)
    if set_index != "":
        print(f"set:{int(set_index, 2)}")
        si = int(set_index, 2)
    else:
        print(f"set:0")
        si = 0
    if tag != "":
        print(f"tag:{ (hex(int(tag, 2)))[2:]}")
    else:
        print("tag:")

    for e in range(E):
        if tag != "":
            if ((str(c[si][e][0]) == "1") and (str(c[si][e][3]) == str(hex(int(tag, 2)))[2:].zfill(2))):
                d_i = si
                d_e = e
                hit = True
                break
        else:
            if ((str(c[si][e][0])) == "1"):
                d_i = si
                d_e = e
                hit = True
                break
    if(hit):
        cache_hits += 1
        print("write_hit:yes")
        print("eviction_line:-1")
        print("ram_address:-1")
        print("data:0x"+c[d_i][d_e][int(b_offset, 2)+4])
        if replace == 3:
            if d_e == 0:
                LFU_count_line0 += 1
                c[d_i][0][2] = LFU_count_line0
            elif d_e == 1:
                LFU_count_line1 += 1
                c[d_i][1][2] = LFU_count_line1
            elif d_e == 2:
                LFU_count_line2 += 1
                c[d_i][2][2] = LFU_count_line2
            else:
                LFU_count_line3 += 1
                c[d_i][3][2] = LFU_count_line3

    else:
        cache_miss += 1
        print("write_hit:no")
        if replace == 1:
            cnt = 0
            for e1 in range(E):
                if c[si][e1][0] == "1":
                    cnt += 1
            if cnt != 4:
                while True:
                    l = random.randint(1, E)
                    if (c[si][l-1][0] == "0"):
                        break
            else:
                l = random.randint(1, E)
        elif replace == 2:
            if E == 1:
                l = 1
            elif E == 2:
                if c[si][0][2] == 0:
                    l = 1
                    c[si][0][2] = 1
                else:
                    l = 2
                    c[si][0][2] = 0
            else:
                if c[si][0][2] == 0:
                    l = 1
                    c[si][0][2] = 1
                    c[si][1][2] = 0
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
                    c[si][0][2] = 0

                # Before
                # if c[si][0][2] == 0:
                #     if c[si][1][2] == 0:
                #         l = 1
                #         c[si][0][2] = 1
                #         c[si][1][2] = 0
                #     else:
                #         l = 2
                #         c[si][0][2] = 1
                #         c[si][1][2] = 1
                # else:
                #     if c[si][1][2] == 0:
                #         l = 3
                #         c[si][0][2] = 0
                #         c[si][1][2] = 1
                #     else:
                #         l = 4
                #         c[si][0][2] = 0
                #         c[si][1][2] = 0
        else:
            # Extra Credit
            if E == 1:
                l = 1
            elif E == 2:
                if c[si][0][2] == min(c[si][0][2], c[si][1][2]):
                    l = 1
                    LFU_count_line0 = 1
                    c[si][0][2] = LFU_count_line0
                else:
                    l = 2
                    LFU_count_line1 = 1
                    c[si][1][2] = LFU_count_line1
            else:
                if c[si][0][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 1
                    LFU_count_line0 = 1
                    c[si][0][2] = LFU_count_line0
                elif c[si][1][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 2
                    LFU_count_line1 = 1
                    c[si][1][2] = LFU_count_line1
                elif c[si][2][2] == min(c[si][0][2], c[si][1][2], c[si][2][2], c[si][3][2]):
                    l = 3
                    LFU_count_line2 = 1
                    c[si][2][2] = LFU_count_line2
                else:
                    l = 4
                    LFU_count_line3 = 1
                    c[si][3][2] = LFU_count_line3

        print(f"eviction_line:{l}")
        c[si][l-1][0] = "1"
        if tag != "":
            c[si][l-1][3] = str(hex(int(tag, 2)))[2:].zfill(2)
        for b in range(4, B+4):
            c[si][l-1][b] = RAM["0x" +
                                hex((int(address[2:], 16)-int(b_offset, 2))+(b-4))[2:].zfill(2)]
        print(f"ram_address:{address}")
        print("data:0x"+RAM[address])


def cache_write(address, data):
    print("ADDRESS:", address)
    print("DATA", data)


def cache_flush(B, E, S):
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

    print(f"cache_size:{C}")
    print(f"data_block_size:{B}")
    print(f"associativity:{E}")
    print(f"replacement_policy:{R}")
    print(f"write_hit_policy:{WH}")
    print(f"write_miss_policy:{WM}")
    print(f"number_of_cache_hits:{cache_hits}")
    print(f"number_of_cache_misses:{cache_miss}")
    print("cache_content:")
    for i in range(S):
        for e in range(E):
            for b in range(B+4):
                if b != 2:
                    print(c[i][e][b], end=" ")
            print("")


def memory_view(RAM, count):
    print(f"memory_size:{count}")
    print("memory_content:")
    print("Address:Data", end="")
    count = 0
    for r in RAM:
        if count % 8 == 0:
            print(f"\n{r}:", end="")
        print(RAM[r], end=" ")
        count += 1
    print("")


def cache_dump(B, E, S):
    o = open("cache.txt", "w")
    for i in range(S):
        for e in range(E):
            for b in range(4, B+4):
                o.write(c[i][e][b]+" ")
            o.write("\n")


def memory_dump(RAM):
    o = open("ram.txt", "w")
    for r in RAM:
        o.write(RAM[r]+"\n")
