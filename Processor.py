import math
import os
import random
import re
import sys
import numpy
import Counter

class Memory:

    def __init__(self):
        self.frames = [None]*30
        self.currentFrame = 0

class PageTableEntry:
    def __init__(self,pageTableID,value):
        self.value=value
        self.pageTableID=pageTableID
        self.inMem = False

    def placeInDisk(self):
        self.inMem = False
        return self
    
    def placeInMem(self):
        self.inMem = True
        return self


class PageTable:
    def __init__(self,processNumber):
        self.id=processNumber
        self.pageEntries=[None]*64
        self.currentFrame=0
    def __getitem__(self,index):
        return self.pageEntries[index]

    def __setitem__(self,index,value):
        self.pageEntries[index] = value

        
class ProcessTable:
    def __init__(self):
        self.pageTables={}
        self.currentProcess = -1
        self.memory = [None]*30
        self.currentMemory=0

    def newTable(self,processNumber):
        self.pageTables[processNumber] = PageTable(processNumber)

    def switch(self,processNumber):
        self.currentProcess = processNumber

    def incrementMemory(self):
        self.currentMemory=(self.currentMemory+1)%30

    def access(self,memoryAddress):
        Counter.access()
        pageIndex = memoryAddress >> 10
        if self.pageTables[self.currentProcess][pageIndex] is None:
            pte = PageTableEntry(self.currentProcess, memoryAddress)
            pte.placeInMem()
            self.putIntoMemory(pte)
            self.pageTables[self.currentProcess][pageIndex] = pte
            Counter.compulsoryMiss()
            Counter.miss()
        else:
            if self.pageTables[self.currentProcess][pageIndex].inMem:
                Counter.hit()
            else:
                Counter.miss()
                pte = self.pageTables[self.currentProcess][pageIndex].placeInMem()
                self.putIntoMemory(pte)
        
    def putIntoMemory(self,pte):
        self.incrementMemory()
        if self.memory[self.currentMemory] is None:
            self.memory[self.currentMemory] = pte
        else:
            tmpPTE = self.memory[self.currentMemory]
            self.pageTables[tmpPTE.pageTableID][tmpPTE.value >> 10].placeInDisk()
            self.memory[self.currentMemory] = pte


commands = {"access": lambda num, processTable: processTable.access(num),
            "new": lambda num, processTable: processTable.newTable(num),
            "switch": lambda num, processTable: processTable.switch(num)
            }

def read(processTable,line):
    inputArr= line.split()
    tmp = inputArr[0]
    commands[inputArr[0]](int(inputArr[1]),processTable)

if __name__ == '__main__':
  
    try:

        with open(sys.argv[1], mode='r') as file:
            processTable = ProcessTable()
            for line in file:
                read(processTable,line)

            print("Accesses: ", Counter.accesses)
            print("Hits: ", Counter.hits)
            print("Compulsory Misses: ", Counter.compulsoryMisses)
            print("Misses: ", Counter.misses)
        
    except FileNotFoundError:
        print("(null): can't open file '%s': [Errno 2] No such file or directory"%sys.argv[1])