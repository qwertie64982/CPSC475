'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This program calculates the minimum edit distance between two words
Usage: python proj5.py {source} {target}
Due: 2018-10-05 18:00 PDT
'''

import sys

distanceMatrix = [[0]]

# main driver function
def main():
    if len(sys.argv) != 3: # if the user enters the wrong number of arguments
        print("Usage: proj5.py {source} {target}")
    else:
        source = str(sys.argv[1]) # get source from command line argument 1
        target = str(sys.argv[2]) # get target from command line argument 2
        
        distanceMatrix = fillDistanceMatrix(source, target)
        for row in distanceMatrix[::-1]:
            print(row)

# fills the distance matrix
def fillDistanceMatrix(source, target):
    # steps 1 and 2 - fill the x-axis
    distanceMatrix[0] = [i for i in range(len(target) + 1)]
    
    # step 3 - fill the y-axis
    for j in range(len(source)):
        distanceMatrix.append([j + 1])
    
    # step 4 - fill the rest of the values
    for x in range(1, len(target) + 1):
        for y in range(1, len(source) + 1):
            distanceMatrix[y].append(minDistance(x, y, source, target)) # y corresponds to which row in the matrix
    
    return distanceMatrix

# finds the value for a non-edge item in the distance matrix (step 4)
def minDistance(x, y, source, target):
    # cost of inserting/deleting is always the same
    insValue = distanceMatrix[y-1][x] + 1
    delValue = distanceMatrix[y][x-1] + 1
    
    # cost of substitution depends on whether or not the chars match
    if target[x-1] == source[y-1]:
        subValue = distanceMatrix[y-1][x-1]
    else:
        subValue = distanceMatrix[y-1][x-1] + 2
    
    # return the smallest of these values
    return min(insValue, delValue, subValue)

main()
