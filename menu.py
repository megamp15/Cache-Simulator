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


def cache_read(address, s, t, b):
    b_address = str(bin(int(address[2:], 16))[2:].zfill(8))
    tag = b_address[:int(t)]
    set_index = b_address[int(t):int(t)+int(s)]
    b_offset = b_address[int(t)+int(s):]
    # print(b_address)
    # print(b_address[:int(t)])
    # print(b_address[int(t):int(t)+int(s)])
    # print(b_address[int(t)+int(s):])
    # print("ADDRESS:", address)
    # print("Address in binary:", b_address)
    # print("s:", int(s), ": ")
    # print("t:", int(t))
    # print(f"b:{int(b)}")


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
        if len(r[2:]) == 1:
            r_temp = r[:2] + "0"+r[2:]
        else:
            r_temp = r
        if count % 8 == 0:
            print("\n", r_temp, ":", end="")
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
