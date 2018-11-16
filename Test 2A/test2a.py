'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Test 2A: This program implements the forward algorithm on the Eisner problem
Usage: python test2a.py 3 1 3 (3 1 3 is an example of an ice cream eating sequence)
Due: 2018-11-19 18:00 PDT
'''

import sys

def main():
    # TODO: read these from files later
    states = [[0.0, 0.5, 0.5, 0.0], [0.0, 0.7, 0.2, 0.1], [0.0, 0.2, 0.7, 0.1], [0.0, 0.0, 0.0, 0.0]] # A-matrix
    observations = [[0.0, 0.0, 0.0], [0.6, 0.3, 0.1], [0.1, 0.3, 0.6], [0.0, 0.0, 0.0]] # B-matrix
    
    # check for anything other than 1, 2, 3 in numbers, if so return 0, as well as length (>0)
    sequence = sys.argv
    if len(sequence) < 2:
        print("ERROR: You must provide at least 1 observation")
        sys.exit(1)
    del sequence[0]
    for i in range(len(sequence)):
        try:
            sequence[i] = int(sequence[i])
        except ValueError:
            print("ERROR: Arguments must all be numbers")
            sys.exit(1)
    
    forwardMatrix = forward(states, observations, sequence)
    
    endingProb = sumEnds(forwardMatrix)
    print(endingProb)

def forward(states, observations, sequence):
    forward = [[0 for observation in sequence] for state in range(len(states))]
    forward = initialize(forward, states, observations, sequence)
    forward = fill(forward, states, observations, sequence)
    return forward

def initialize(forward, states, observations, sequence):
    for stateIndex in range(len(forward)):
        forward[stateIndex][0] = states[0][stateIndex] * observations[stateIndex][sequence[0]-1]
    return forward

def fill(forward, states, observations, sequence):
    for seqIndex in range(1, len(sequence)): # -1 because we already did the first column
        for stateIndex in range(len(forward)):
            probSum = 0.0
            for stateIndex2 in range(len(forward)):
                probSum += forward[stateIndex2][seqIndex-1] * states[stateIndex2][stateIndex] * observations[stateIndex2][sequence[seqIndex]-1]
            forward[stateIndex][seqIndex] = probSum
    
    return forward

def sumEnds(forward):
    endingProb = 0.0
    for i in range(len(forward)):
        endingProb += forward[i][-1]
    return endingProb

main()
