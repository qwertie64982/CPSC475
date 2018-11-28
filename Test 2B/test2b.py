'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Test 2A: This program implements the Viterbi algorithm on the Eisner problem
Usage: python test2b.py matA.csv matB.csv 3 1 3 (3 1 3 is an example of an ice cream eating sequence)
Due: 2018-11-30 18:00 PDT
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
                print("This is an impossible scenario") # no probability of Eisner eating < 1 or > 3 ice cream cones in one day
        except ValueError:
            print("ERROR: Arguments must all be numbers")
            sys.exit(1)
    
    # construct Viterbi trellis
    viterbiMatrix = viterbi(states, observations, sequence)
    
    printResults(viterbiMatrix, len(sequence))

# read a CSV file into a list
def readCSV(filename):
    reader = csv.reader(open(filename, "rb"), delimiter = ",")
    inList = list(reader)
    result = numpy.array(inList).astype("float")
    return result

# calculate Viterbi trellis
# the trellis is represented as a 2D array, where 3, 1, 3 is the example sequence:
#        3  1  3
# start [ ][ ][ ]
#  cold [ ][ ][ ]
#   hot [ ][ ][ ]
#   end [ ][ ][ ]
def viterbi(states, observations, sequence):
    # make empty matrix
    viterbiMatrix = [[0 for observation in sequence] for state in range(len(states))]
    # backPointers = [[-1 for observation in sequence] for state in range(len(states))]
    
    # fill matrix
    viterbiMatrix = initialize(viterbiMatrix, states, observations, sequence) # fill first column
    viterbiMatrix = fill(viterbiMatrix, states, observations, sequence) # fill following columns
    
    # for row in viterbiMatrix:
    #     print row
    # print
    
    return viterbiMatrix

# fill the first column of the Viterbi trellis
def initialize(viterbiMatrix, states, observations, sequence):
    for stateIndex in range(len(viterbiMatrix)):
        newProb = states[0][stateIndex] * observations[stateIndex][sequence[0]-1]
        if (viterbiMatrix[stateIndex][0] == 0 or newProb > viterbiMatrix[stateIndex][sequence[0]-1]):
            viterbiMatrix[stateIndex][0] = newProb
    
    return viterbiMatrix

# fill the rest of the columns in the Viterbi trellis
def fill(viterbiMatrix, states, observations, sequence):
    for seqIndex in range(1, len(sequence)): # -1 because we already did the first column
        for stateIndex in range(len(viterbiMatrix)):
            for stateIndex2 in range(len(viterbiMatrix)): # find the largest of the probabilities of getting to this state from every previous possible state
                newProb = viterbiMatrix[stateIndex2][seqIndex-1] * states[stateIndex2][stateIndex] * observations[stateIndex][sequence[seqIndex]-1]
                if (viterbiMatrix[stateIndex][seqIndex] == 0 or newProb > viterbiMatrix[stateIndex][seqIndex]):
                    viterbiMatrix[stateIndex][seqIndex] = newProb
                    # backPointers[stateIndex][seqIndex] = stateIndex2
    
    return viterbiMatrix

def printResults(viterbiMatrix, maxIndex):
    statesList = [-1 for i in range(maxIndex)]
    
    for i in range(maxIndex-1, -1, -1):
        runningMax = 0.0
        for j, row in enumerate(viterbiMatrix):
            if row[i] > runningMax:
                runningMax = row[i]
                statesList[i] = j
    
    # print statesList
    
    # start and end are included here, but are unused due to the Viterbi matrix implementation
    print("State sequence:"),
    for state in statesList:
        if state == 0:
            print("start"),
        elif state == 1:
            print("cold"),
        elif state == 2:
            print("hot"),
        elif state == 3:
            print("end"),
        else:
            print("ERROR: Invalid state")
            sys.exit(1)

main()
