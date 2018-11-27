'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Test 2A: This program implements the forward algorithm on the Eisner problem
Usage: python test2a.py 3 1 3 (3 1 3 is an example of an ice cream eating sequence)
Due: 2018-11-19 18:00 PDT
'''

import csv
import numpy
import sys

# main driver function
def main():
    sequence = sys.argv # user-defined sequence of observations
    if len(sequence) < 4:
        print("ERROR: You must provide the A and B matrices and at least 1 observation")
        sys.exit(1)
    try:
        states = readCSV(sys.argv[1]) # A-matrix
        observations = readCSV(sys.argv[2]) # B-matrix
    except IOError:
        print("ERROR: File can't be read or doesn't exist")
        sys.exit(1)
    del sequence[0] # remove first argument
    del sequence[0] # remove input file argument
    del sequence[0] # remove output file argument
    for i in range(len(sequence)):
        try:
            sequence[i] = int(sequence[i])
            if sequence[i] < 1 or sequence[i] > 3:
                print("This is an impossible scenario") # 0% probability of Eisner eating < 1 or > 3 ice cream cones in one day TODO: modify this
        except ValueError:
            print("ERROR: Arguments must all be numbers")
            sys.exit(1)
    
    # construct forward trellis
    forwardMatrix, backPointers = forward(states, observations, sequence)
    
    printResults(forwardMatrix, backPointers, len(sequence))
    
    for line in forwardMatrix:
        print str(line)

# read a CSV file into a list
def readCSV(filename):
    reader = csv.reader(open(filename, "rb"), delimiter = ",")
    inList = list(reader)
    result = numpy.array(inList).astype("float")
    return result

# calculate forward trellis
# the trellis is represented as a 2D array, where 3, 1, 3 is the example sequence:
#        3  1  3
# start [ ][ ][ ]
#  cold [ ][ ][ ]
#   hot [ ][ ][ ]
#   end [ ][ ][ ]
def forward(states, observations, sequence):
    # make empty matrix
    forward = [[0 for observation in sequence] for state in range(len(states))]
    backPointers = [[-1 for observation in sequence] for state in range(len(states))]
    
    # fill matrix
    forward = initialize(forward, states, observations, sequence) # fill first column
    forward = fill(forward, backPointers, states, observations, sequence) # fill following columns
    
    return forward, backPointers

# fill the first column of the forward trellis
def initialize(forward, states, observations, sequence):
    for stateIndex in range(len(forward)):
        newProb = states[0][stateIndex] * observations[stateIndex][sequence[sequence[0]-1]-1]
        if (forward[stateIndex][0] == 0 or newProb > forward[stateIndex][sequence[0]-1]):
            forward[stateIndex][0] = newProb
    return forward

# fill the rest of the columns in the forward trellis
def fill(forward, backPointers, states, observations, sequence):
    for seqIndex in range(1, len(sequence)): # -1 because we already did the first column
        for stateIndex in range(len(forward)):
            for stateIndex2 in range(len(forward)): # sum the probabilities of getting to this state from every previous possible state
                newProb = forward[stateIndex2][seqIndex-1] * states[stateIndex2][stateIndex] * observations[stateIndex][sequence[seqIndex]-1]
                if (forward[stateIndex][seqIndex] == 0 or newProb > forward[stateIndex][seqIndex]):
                    forward[stateIndex][seqIndex] = newProb
                    backPointers[stateIndex][seqIndex] = stateIndex2
    for line in backPointers:
        print line
    print
    
    return forward

# sum the last column of the trellis
# technically, every item in the last column points to the end state,
# so summing them all is really calculating the value of the end state
def sumEnds(forward):
    endingProb = 0.0
    for i in range(len(forward)):
        endingProb += forward[i][-1]
    return endingProb

def printResults(forward, backPointers, maxIndex):
    statesList = [-1]
    
    runningMax = 0.0
    for i, row in enumerate(forward):
        if row[maxIndex-1] > runningMax:
            runningMax = row[maxIndex-1]
            statesList[0] = i
    
    for j in range(maxIndex-1, 0, -1):
        statesList.append(backPointers[statesList[-1]][j])
    
    # statesList now contains numbers 0-3 representing the most probable states (start, cold, hot, end)
    # TODO: turn these into human-readable strings

main()
