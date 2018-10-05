'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This program calculates the minimum edit distance between two words
Usage: python proj5.py {source} {target}
Due: 2018-10-05 18:00 PDT
'''

import sys

# main driver function
def main():
    if len(sys.argv) != 3: # if the user enters the wrong number of arguments
        print("Usage: proj5.py {source} {target}")
    else:
        source = str(sys.argv[1]) # get source from command line argument 1
        target = str(sys.argv[2]) # get target from command line argument 2
        
        distanceMatrix = fillDistanceMatrix(source, target)
        
        fancyPrint(distanceMatrix, source, target)
        
        printAlignment(distanceMatrix, source, target)

# fills the distance matrix
def fillDistanceMatrix(source, target):
    # initialize the matrix
    distanceMatrix = [[0]]
    
    # steps 1 and 2 - fill the x-axis
    distanceMatrix[0] = [i for i in range(len(target) + 1)]
    
    # step 3 - fill the y-axis
    for j in range(len(source)):
        distanceMatrix.append([j + 1])
    
    # step 4 - fill the rest of the values
    for x in range(1, len(target) + 1):
        for y in range(1, len(source) + 1):
            distanceMatrix[y].append(minDistance(distanceMatrix, x, y, source, target)) # y corresponds to which row in the matrix
    
    return distanceMatrix

# finds the value for a non-edge item in the distance matrix (step 4)
def minDistance(distanceMatrix, x, y, source, target):
    # cost of inserting/deleting is always the same
    delValue = distanceMatrix[y-1][x] + 1
    insValue = distanceMatrix[y][x-1] + 1
    
    # cost of substitution depends on whether or not the chars match
    if target[x-1] == source[y-1]:
        subValue = distanceMatrix[y-1][x-1]
    else:
        subValue = distanceMatrix[y-1][x-1] + 2
    
    # return the smallest of these values
    return min(delValue, insValue, subValue)

# this does not handle 2 digit numbers in the matrix
def fancyPrint(distanceMatrix, source, target):
    distanceMatrix = distanceMatrix[::-1] # invert the matrix, because otherwise 0,0 is at the top left
    source = source[::-1] # invert source so we can print it upside down
    
    print # newline
    
    # print all rows with the source on the left (all but bottom)
    for i in range(len(distanceMatrix) - 1):
        print(source[i] + " " + str(distanceMatrix[i]))
    
    # print the row with the # on the left (bottom)
    print("# " + str(distanceMatrix[len(distanceMatrix) - 1]))
    
    # print the # and target word below the matrix
    print("   # "),
    for j in range(len(target)):
        print(target[j] + " "),
    
    print("\n") # 2 newlines
    
    print("Minimum edit distance: " + str(distanceMatrix[0][len(target)]) + "\n")

def printAlignment(distanceMatrix, source, target):
    pathMatrix = findPath(distanceMatrix, source, target)
    print(str(pathMatrix))

def findPath(distanceMatrix, source, target):
    pathMatrix = []
    
    currentY = 0
    currentX = 0
    currentValue = delValue = insValue = subValue = 0
    canDel = False
    canIns = False
    canSub = False
    while not (currentY == len(source) and currentX == len(target)):
        currentValue = distanceMatrix[currentY][currentX]
        
        if currentY < len(source) and currentX < len(target):
            subValue = distanceMatrix[currentY + 1][currentX + 1]
            if subValue == currentValue or subValue == currentValue + 2:
                canSub = True
        elif currentX < len(target):
            insValue = distanceMatrix[currentY][currentX + 1]
            if insValue == currentValue + 1:
                canIns = True
        elif currentY < len(source):
            delValue = distanceMatrix[currentY + 1][currentX]
            if delValue == currentValue + 1:
                canDel = True
        
        if canSub == True and subValue == currentValue:
            pathMatrix.append("S")
            currentY += 1
            currentX += 1
        elif canDel:
            pathMatrix.append("d")
            currentY += 1
        elif canIns:
            pathMatrix.append("i")
            currentX += 1
        elif canSub:
            pathMatrix.append("s")
            currentY += 1
            currentX += 1
        
        canDel = canIns = canSub = False
    
    return pathMatrix

main()
