import random

c = []
cache_hits = 0
cache_miss = 0


def cache(B, E, S):
    global c
    for i in range(S):
        c.append([])
        for e in range(E):
            c[i].append([])
            for b in range(B+3):
                if b == 0:
                    c[i][e].append("0")
                elif b == 1:
                    c[i][e].append("0")
                else:
                    c[i][e].append("00")


def cache_read(address, s, t, b, S, E, B, replace, RAM):
    global cache_hits, cache_miss, c
    hit = False
    b_address = (bin(int(address[2:], 16))[2:].zfill(8))
    tag = b_address[:int(t)]
    set_index = b_address[int(t):int(t)+int(s)]
    b_offset = b_address[int(t)+int(s):]
    print("set:", int(set_index, 2))
    print("tag:", int(tag, 2))
    # for i in range(S):
    #     for e in range(E):
    #         if ((str(c[i][e][0]) == "1") and (str(c[i][e][2]) == str(hex(int(tag)))[2:].zfill(2))):
    #             d_i = i
    #             d_e = e
    #             hit = True
    #             break
    # if(hit):
    #     cache_hits += 1
    #     print("hit:yes")
    #     print("eviction_line:-1")
    #     print("ram_address:-1")
    #     print("data:0x"+c[d_i][d_e][int(b_offset, 2)+3])
    # else:
    #     cache_miss += 1
    #     print("hit:no")
    #     if replace == 1:
    #         l = random.randint(1, S*E)
    #         if E == 1:
    #             r = str(l-1)+"0"
    #             print(r)
    #         elif E == 2:
    #             r = bin(l-1)[2:].zfill(2)
    #         else:
    #             r = "0"+str(l-1)
    #     print("eviction_line:", l)
    #     print("ram_address:", address)
    #     print("data:0x"+RAM[address])
    #     for i in range(S):
    #         for e in range(E):
    #             for b in range(B+3):
    #                 if b == 0:
    #                     c[int(r[0])][int(r[1])][b] = "1"
    #                 elif b == 1:
    #                     pass
    #                 elif b == 2:
    #                     c[int(r[0])][int(r[1])][b] = str(
    #                         hex(int(tag)))[2:].zfill(2)
    #                 else:
    #                     c[int(r[0])][int(r[1])][b] = RAM["0x"+hex(
    #                         (int(address[2:], 16)-int(b_offset))+(b-3))[2:].zfill(2)]


def cache_write(address, data):
    print("ADDRESS:", address)
    print("DATA", data)


def cache_flush(B, E, S):
    for i in range(S):
        for e in range(E):
            for b in range(B+3):
                if b == 0:
                    c[i][e][b] = "0"
                elif b == 1:
                    c[i][e][b] = "0"
                else:
                    c[i][e][b] = "00"
    print("cache_cleared")


def cache_view(B, E, S, C, replace, write_hit, write_miss):
    if replace == 1:
        R = "random replacement"
    else:
        R = "least Recently Used"
    if write_hit == 1:
        WH = "write-through"
    else:
        WH = "write-back"
    if write_miss == 1:
        WM = "write-allocate"
    else:
        WM = "no write-allocate"

    print("cache_size:", C)
    print("data_block_size:", B)
    print("associativity:", E)
    print("replacement_policy:", R)
    print("write_hit_policy:", WH)
    print("write_miss_policy:", WM)
    print("number_of_cache_hits:", cache_hits)
    print("number_of_cache_misses:", cache_miss)
    print("cache_content:")
    for i in range(S):
        for e in range(E):
            for b in range(B+3):
                print(c[i][e][b], end=" ")
            print("")


def memory_view(RAM, count):
    print("memory_size:", count)
    print("memory_content:")
    print("Address:Data")
    count = 0
    for r in RAM:
        if count % 8 == 0:
            print("\n", r, ":", end="")
        print(RAM[r], end=" ")
        count += 1


def cache_dump(B, E, S):
    o = open("cache.txt", "w+")
    for i in range(S):
        for e in range(E):
            for b in range(3, B+3):
                o.write(c[i][e][b]+" ")
            o.write("\n")


def memory_dump(RAM):
    o = open("ram.txt", "w+")
    for r in RAM:
        o.write(RAM[r]+"\n")
