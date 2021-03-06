'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 5: This program calculates the minimum edit distance between two words
Usage: python proj5.py {source} {target}
Due: 2018-10-05 18:00 PDT, extension to 2018-10-08 18:00 PDT
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
# (value, ins, del, sub)
def fillDistanceMatrix(source, target):
    # initialize the matrix
    distanceMatrix = [[(0, False, False, False)]]
    
    # steps 1 and 2 - fill the x-axis
    distanceMatrix[0] = [(i, True, False, False) for i in range(len(target) + 1)]
    
    # step 3 - fill the y-axis
    for j in range(len(source)):
        distanceMatrix.append([(j + 1, False, True, False)])
    
    # step 4 - fill the rest of the values
    for x in range(1, len(target) + 1):
        for y in range(1, len(source) + 1):
            distanceMatrix[y].append(minDistance(distanceMatrix, x, y, source, target)) # y corresponds to which row in the matrix
    
    return distanceMatrix

# finds the value for a non-edge item in the distance matrix (step 4)
def minDistance(distanceMatrix, x, y, source, target):
    # cost of substitution depends on whether or not the chars match
    if target[x-1] == source[y-1]:
        subValue = distanceMatrix[y-1][x-1][0]
    else:
        subValue = distanceMatrix[y-1][x-1][0] + 2
    
    # cost of inserting/deleting is always the same
    delValue = distanceMatrix[y-1][x][0] + 1
    insValue = distanceMatrix[y][x-1][0] + 1
    
    # return the smallest of these values
    canIns = False
    canDel = False
    canSub = False
    if min(insValue, delValue, subValue) == insValue:
        if insValue == delValue:
            canDel = True
        if insValue == subValue:
            canSub = True
        return (insValue, True, canDel, canSub)
    elif min(insValue, delValue, subValue) == delValue:
        if delValue == insValue:
            canIns = True
        if delValue == subValue:
            canSub = True
        return (delValue, canIns, True, canSub)
    elif min(insValue, delValue, subValue) == subValue:
        if subValue == insValue:
            canIns = True
        if subValue == delValue:
            canDel = True
        return (subValue, canIns, canDel, True)

# prints the distance matrix with labels on the axes
# as well as the minimum edit distance
# this does not handle 2 digit numbers in the matrix well
def fancyPrint(distanceMatrix, source, target):
    distanceMatrix = distanceMatrix[::-1] # invert the matrix, because otherwise 0,0 is at the top left
    source = source[::-1] # invert source so we can print it upside down
    
    print # newline
    
    # print all rows with the source on the left (all but bottom)
    for i in range(len(distanceMatrix) - 1):
        print(source[i]),
        for value in distanceMatrix[i]:
            if value[0] < 10:
                print(""),
            print(value[0]),
        print
    
    # print the row with the # on the left (bottom)
    print("#"),
    for value in distanceMatrix[len(distanceMatrix) - 1]:
        if value[0] < 10:
            print(""),
        print(value[0]),
    print
    
    # print the # and target word below the matrix
    print("   # "),
    for j in range(len(target)):
        print(target[j] + " "),
    
    print("\n") # 2 newlines
    
    print("Minimum edit distance: " + str(distanceMatrix[0][len(target)][0]) + "\n")

# prints the alignment between the source and target strings
def printAlignment(distanceMatrix, source, target):
    # create a list of steps for the transformation
    pathMatrix = findPath(distanceMatrix, source, target)
    
    # generate alignment of source and target strings
    # Unicode character is Greek small epsilon,
    #   as used in 'Speech and Language Processing' by Jurafsky and Martin
    sourceOutput = ""
    targetOutput = ""
    sourceIndex = 0
    targetIndex = 0
    for step in pathMatrix:
        if step == "s": # substitution
            sourceOutput += source[sourceIndex]
            sourceIndex += 1
            targetOutput += target[targetIndex]
            targetIndex += 1
        elif step == "d": # deletion
            sourceOutput += source[sourceIndex]
            sourceIndex += 1
            targetOutput += "*"
        elif step == "i": # insertion
            sourceOutput += "*"
            targetOutput += target[targetIndex]
            targetIndex += 1
        sourceOutput += " "
        targetOutput += " "
    
    # print alignment
    print("Alignment:"),
    for instruction in pathMatrix:
        print(instruction),
    print # newline
    print("Source:    " + sourceOutput)
    print("          "),
    for i in range(len(sourceOutput) / 2):
        print("|"),
    print # newline
    print("Target:    " + targetOutput)

# find the steps to transform the source to the target
def findPath(distanceMatrix, source, target):
    pathMatrix = []
    
    currentY = len(source) # current Y coordinate in the distance matrix
    currentX = len(target) # current X coordinate in the distance matrix
    canIns = False # whether an insertion could be used to get to this point
    canDel = False # whether a deletion could be used to get to this point
    canSub = False # whether a substitution could be used to get to this point
    
    # iterate from the top right until we reach the bottom left of the distance matrix
    while not (currentY == 0 and currentX == 0):
        currentValue = distanceMatrix[currentY][currentX][0]
        canIns = distanceMatrix[currentY][currentX][1]
        canDel = distanceMatrix[currentY][currentX][2]
        canSub = distanceMatrix[currentY][currentX][3]
        
        # add the best step to the path
        if canSub: # substitution always checked first in case of 0-cost sub
            pathMatrix.append("s")
            currentY -= 1
            currentX -= 1
        elif canDel: # deletion
            pathMatrix.append("d")
            currentY -= 1
        elif canIns: # insertion
            pathMatrix.append("i")
            currentX -= 1
        else: # debug
            print("I'm stuck")
            break
        
        # reset the booleans for the next iteration
        canDel = canIns = canSub = False
    
    return pathMatrix[::-1]

main()
