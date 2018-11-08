'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 7A: This program uses n-grams/probabilities from the Shakespeare corpus to generate new sentences
Usage: python proj7b.py
Due: 2018-11-09 18:00 PDT
'''

import pickle
from random import randint
import re

# main driver function
def main():
    # Read Bogensberger-Johnson n-gram matrices from pickle file
    try:
        inPickle = open("proj7b.pkl", "r")
    except:
        print("File read error")
        raise SystemExit
    print("Importing unigrams matrix...")
    unigramsMatrix = pickle.load(inPickle)
    print("Importing bigrams matrix...")
    bigramsMatrix = pickle.load(inPickle)
    print("Importing trigrams matrix...")
    trigramsMatrix = pickle.load(inPickle)
    print("Importing quadgrams matrix...")
    quadgramsMatrix = pickle.load(inPickle)
    
    print # newline
    
    print("UNIGRAMS:")
    for i in range(2):
        print(newSentence(unigramsMatrix, 1))
    print # newline
    
    print("BIGRAMS:")
    for i in range(2):
        print(newSentence(bigramsMatrix, 2))
    print # newline
    
    print("TRIGRAMS:")
    for i in range(2):
        print(newSentence(trigramsMatrix, 3))
    print # newline
    
    print("QUADGRAMS:")
    for i in range(2):
        print(newSentence(quadgramsMatrix, 4))
    print # newline

# generates a sentence based on a Bogensberger-Johnson n-gram matrix
def newSentence(ngramsMatrix, n):
    if n == 1:
        return newUnigramSentence(ngramsMatrix)
    elif n == 2:
        ngramList = []
        ngramList.append(newNgram((None, "<s>"), ngramsMatrix, n)) # <s>
        for i in range(4): # 6 - 2 (start and end)
            ngramList.append(newNgram(ngramList[i], ngramsMatrix, n))
        ngramList.append(endingNgram(ngramsMatrix, n)) # </s>
        # print str(ngramList)
        return renderSentence(ngramList, n)
    elif n == 3:
        ngramList = []
        ngramList.append(newNgram((None, None, "<s>"), ngramsMatrix, n)) # <s>
        for i in range(2): # 4 - 2 (start and end)
            ngramList.append(newNgram(ngramList[i], ngramsMatrix, n))
        ngramList.append(endingNgram(ngramsMatrix, n)) # </s>
        # print(str(ngramList))
        return renderSentence(ngramList, n)
    elif n == 4:
        ngramList = []
        ngramList.append(newNgram((None, None, None, "<s>"), ngramsMatrix, n)) # <s>
        for i in range(1): # 3 - 2 (start and end)
            ngramList.append(newNgram(ngramList[i], ngramsMatrix, n))
        ngramList.append(endingNgram(ngramsMatrix, n)) # </s>
        # print (str(ngramList))
        return renderSentence(ngramList, n)
    else:
        print("Unsupported n-gram")
        raise SystemExit

# generates a sentence based on a Bogensberger-Johnson unigram matrix
def newUnigramSentence(unigramsMatrix):
    wordList = [newWord(unigramsMatrix) for i in range(12)] # 12 words
    wordList[0] = wordList[0].title()
    completedSentence = ""
    for word in wordList:
        completedSentence += (word + " ")
    completedSentence = completedSentence[:-1] # remove last space
    completedSentence += "."
    return completedSentence

# generates a new word based on a Bogensberger-Johnson unigram matrix
def newWord(unigramsMatrix):
    randomDecimal = randint(0, 10000000000) / 10000000000.0
    runningMax = 0.0
    # selectedWord = ""
    for word in unigramsMatrix:
        if word[2] > runningMax:
            runningMax = word[2]
            selectedWord = word[0]
        if runningMax > randomDecimal:
            break
    return selectedWord

def newNgram(target, ngramsMatrix, n):
    selectedNgram = (None, None, None, None)
    # print("searching for " + target[n-1])
    while selectedNgram[0] != target[n-1] or selectedNgram[n-1] == "</s>":
        randomDecimal = randint(0, 10000000000) / 10000000000.0
        runningMax = 0.0
        for item in ngramsMatrix:
            if item[2] > runningMax:
                runningMax = item[2]
                selectedNgram = item[0]
            if runningMax > randomDecimal:
                break
        # print("Checking " + selectedNgram[0])
    return selectedNgram

def endingNgram(ngramsMatrix, n):
    selectedNgram = (None, None, None, None)
    # print("Finding final ngram")
    while selectedNgram[n-1] != "</s>":
        randomDecimal = randint(0, 10000000000) / 10000000000.0
        runningMax = 0.0
        for item in ngramsMatrix:
            if item[2] > runningMax:
                runningMax = item[2]
                selectedNgram = item[0]
            if runningMax > randomDecimal:
                break
    return selectedNgram

def renderSentence(ngramList, n):
    # print("Rendering sentence")
    completedSentence = ""
    if n == 2:
        for i in range(1, len(ngramList)): # read ngram[0] for all but the first
            if i == len(ngramList) - 1:
                completedSentence += (ngramList[i-1][1] + " ")
            completedSentence += (ngramList[i][0] + " ")
    elif n == 3:
        completedSentence += (ngramList[0][1] + " ")
        for i in range(1, len(ngramList)): # read ngram[0] for all but the first
            if i == len(ngramList) - 1:
                completedSentence += (ngramList[i-1][1] + " ")
                completedSentence += (ngramList[i-1][2] + " ")
                completedSentence += (ngramList[i][0] + " ")
                completedSentence += (ngramList[i][1] + " ")
            else:
                completedSentence += (ngramList[i][0] + " ")
    elif n == 4:
        completedSentence += (ngramList[0][1] + " ")
        completedSentence += (ngramList[0][2] + " ")
        for i in range(1, len(ngramList)): # read ngram[0] for all but the first
            if i == len(ngramList) - 1:
                completedSentence += (ngramList[i-1][1] + " ")
                completedSentence += (ngramList[i-1][2] + " ")
                completedSentence += (ngramList[i-1][3] + " ")
                completedSentence += (ngramList[i][0] + " ")
                completedSentence += (ngramList[i][1] + " ")
                completedSentence += (ngramList[i][2] + " ")
            else:
                completedSentence += (ngramList[i][0] + " ")
    completedSentence = completedSentence[0].capitalize() + completedSentence[1:] # capitalize first letter
    completedSentence = completedSentence[:-1] # remove last space
    completedSentence += "."
    completedSentence = re.sub("<s> ", "", completedSentence) # remove <s> in cases like ('<s>', 'kent', '</s>')
    return completedSentence

main()
