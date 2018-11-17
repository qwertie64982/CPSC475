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
    states = readCSV("matA.csv") # A-matrix
    observations = readCSV("matB.csv") # B-matrix
    sequence = sys.argv # user-defined sequence of observations
    if len(sequence) < 2:
        print("ERROR: You must provide at least 1 observation")
        sys.exit(1)
    del sequence[0]
    for i in range(len(sequence)):
        try:
            sequence[i] = int(sequence[i])
            if sequence[i] < 1 or sequence[i] > 3:
                printResults(0) # 0% probability of Eisner eating < 1 or > 3 ice cream cones in one day
        except ValueError:
            print("ERROR: Arguments must all be numbers")
            sys.exit(1)
    
    # construct forward trellis
    forwardMatrix = forward(states, observations, sequence)
    
    # sum the last column (since they all point to the end state)
    endingProb = sumEnds(forwardMatrix)
    printResults(endingProb)

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
    
    # fill matrix
    forward = initialize(forward, states, observations, sequence) # fill first column
    forward = fill(forward, states, observations, sequence) # fill following columns
    
    return forward

# fill the first column of the forward trellis
def initialize(forward, states, observations, sequence):
    for stateIndex in range(len(forward)):
        forward[stateIndex][0] = states[0][stateIndex] * observations[stateIndex][sequence[0]-1]
    return forward

# fill the rest of the columns in the forward trellis
def fill(forward, states, observations, sequence):
    for seqIndex in range(1, len(sequence)): # -1 because we already did the first column
        for stateIndex in range(len(forward)):
            probSum = 0.0
            for stateIndex2 in range(len(forward)): # sum the probabilities of getting to this state from every previous possible state
                probSum += forward[stateIndex2][seqIndex-1] * states[stateIndex2][stateIndex] * observations[stateIndex][sequence[seqIndex]-1]
            forward[stateIndex][seqIndex] = probSum
    
    return forward

# sum the last column of the trellis
# technically, every item in the last column points to the end state,
# so summing them all is really calculating the value of the end state
def sumEnds(forward):
    endingProb = 0.0
    for i in range(len(forward)):
        endingProb += forward[i][-1]
    return endingProb

# print the results and end the program
def printResults(endingProb):
    print("Probability: " + str(round(100 * endingProb, 15)) + "%") # round to remove floating point error
    sys.exit(0) # if printResults() is called when a 0% probability number is discovered

main()
