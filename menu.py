c = []


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


def cache_read(address):
    print("ADDRESS:", address)


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


def cache_view(B, E, S):
    for i in range(S):
        for e in range(E):
            for b in range(B+3):
                print(c[i][e][b], end=" ")
            print("")


def memory_view():
    print("5")


def cache_dump():
    print("6")


def memory_dump():
    print("7")
