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
    for i in range(5):
        print(newSentence(unigramsMatrix, 1))
    print # newline
    
    print("BIGRAMS:")
    for i in range(5):
        print(newSentence(bigramsMatrix, 2))
    print # newline
    
    print("TRIGRAMS:")
    for i in range(5):
        print(newSentence(trigramsMatrix, 3))
    print # newline
    
    print("QUADGRAMS:")
    for i in range(5):
        print(newSentence(quadgramsMatrix, 4))
    print # newline

# generates a sentence based on a Bogensberger-Johnson n-gram matrix
def newSentence(ngramsMatrix, n):
    if n == 1:
        return newUnigramSentence(ngramsMatrix)
    elif n == 2:
        ngramList = []
        ngramList.append(newNgram((None, "<s>"), ngramsMatrix)) # <s>
        for i in range(4): # 6 - 2 (start and end)
            ngramList.append(newNgram(ngramList[i], ngramsMatrix))
        ngramList.append(endingNgram(ngramsMatrix)) # </s>
        return str(ngramList) # TODO: when actually formatting the sentence, just read ngram[0] for all but the first
    elif n == 3:
        return "todo"
    elif n == 4:
        return "todo"
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

def newNgram(target, ngramsMatrix):
    selectedNgram = (None, None)
    print "searching for " + target[1]
    while selectedNgram[0] != target[1] or selectedNgram[1] == "</s>":
        randomDecimal = randint(0, 10000000000) / 10000000000.0
        runningMax = 0.0
        for ngram in ngramsMatrix:
            if ngram[2] > runningMax:
                runningMax = ngram[2]
                selectedNgram = ngram[0]
            if runningMax > randomDecimal:
                break
    return selectedNgram

def endingNgram(ngramsMatrix):
    selectedNgram = (None, None)
    while selectedNgram[1] != "</s>":
        randomDecimal = randint(0, 10000000000) / 10000000000.0
        runningMax = 0.0
        for ngram in ngramsMatrix:
            if ngram[2] > runningMax:
                runningMax = ngram[2]
                selectedNgram = ngram[0]
            if runningMax > randomDecimal:
                break
    return selectedNgram

main()
