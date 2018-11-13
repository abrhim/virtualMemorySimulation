misses=0
compulsoryMisses=0
hits=0
accesses=0



def miss():
    global misses
    misses += 1
def hit():
    global hits
    hits +=1
def access():
    global accesses
    accesses+=1
def compulsoryMiss():
    global compulsoryMisses
    compulsoryMisses+=1
