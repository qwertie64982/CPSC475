'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Test 2A: This program implements the forward algorithm on the Eisner problem
Usage: python test2a.py 3 1 3 (3 1 3 is an example of an ice cream eating sequence)
Due: 2018-11-16 18:00 PDT
'''

def main():
    # TODO: read these from files later
    states = [[0.0, 0.5, 0.5, 0.0], [0.0, 0.7, 0.2, 0.1], [0.0, 0.2, 0.7, 0.1], [0.0, 0.0, 0.0, 0.0]] # A-matrix
    observations = [[0.0, 0.0, 0.0], [0.6, 0.3, 0.1], [0.1, 0.3, 0.6], [0.0, 0.0, 0.0]] # B-matrix
    
    # TODO: get these from command line args
    # check for anything other than 1, 2, 3 in numbers, if so return 0
    sequence = [3, 1, 3]
    
    forwardProb = forward(states, observations, sequence)

def forward(states, observations, sequence):
    numStates = len(states)
    lenSequence = len(sequence)
    forward = [[0 for j in range(lenSequence + 2)] for i in range(numStates + 2)]
    forward[0][0] = 1.0
    for t in range(lenSequence):
        for s in range(numStates):
            for transitionIndex in range(len(states[s])):
                x = forward[s][t]
                y = states[s][transitionIndex]
                z = observations[transitionIndex][sequence[t]-1]
                # print x,
                # print y,
                # print z,
                print x * y * z,
                print "into [" + str(transitionIndex) + "][" + str(t+1) + "]" # TODO: Why does it overwrite?
                
                forward[transitionIndex][t+1] = x * y * z
    print str(forward)
    return 0

main()
