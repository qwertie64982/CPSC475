'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 6: This program explores unigrams by generating 5 sentences from a corpus
Usage: python proj6.py
Due: 2018-10-26 18:00 PDT
'''

from nltk.corpus import brown
from random import randint
import re

def main():
    rawCorpus = brown.sents(categories = "editorial")
    tokenizedCorpus = tokenizeCorpus(rawCorpus)
    
    bogJohnMatrix = calculateFrequencies(tokenizedCorpus)
    
    # print tokenizedCorpus[0]
    # print tokenizedCorpus[1]
    
    for i in range(5):
        print(newSentence(bogJohnMatrix))

def tokenizeCorpus(rawCorpus):
    tokenizedCorpus = [[word.encode("ascii") for word in sentence] for sentence in rawCorpus]
    
    for i, sentence in enumerate(tokenizedCorpus):
        for j, word in enumerate(sentence):
            tokenizedCorpus[i][j] = re.sub("[.,:;?!()`\"]+", "", word.lower()) # make lowercase and remove special chars except apostrophe
        tokenizedCorpus[i] = filter(None, tokenizedCorpus[i]) # remove empty strings
        tokenizedCorpus[i] = filter(lambda word: word != "\'\'" and word != "--", tokenizedCorpus[i]) # remove strange '' and -- words
    
    return tokenizedCorpus

# this is very memory inefficient for the sake of simplicity and easiness to read
def calculateFrequencies(tokenizedCorpus):
    wordOrder = {}
    wordSums = []
    wordList = []
    wordCount = 0
    for sentence in tokenizedCorpus:
        for word in sentence:
            wordCount += 1
            if word in wordOrder:
                wordSums[wordOrder[word]] += 1
            else:
                wordOrder[word] = len(wordOrder)
                wordSums.append(1)
                wordList.append(word)
    
    # print wordOrder
    # print wordSums
    # print wordList
    # print wordCount
    
    relativeFrequencies = [wordSum / float(wordCount) for wordSum in wordSums]
    
    # print relativeFrequencies
    
    cumulativeProbabilities = [relativeFrequencies[0]]
    for i in range(1, len(relativeFrequencies)):
        cumulativeProbabilities.append(relativeFrequencies[i] + cumulativeProbabilities[i-1])
    
    # print cumulativeProbabilities[0]
    # print cumulativeProbabilities[-1]
    
    bogJohnMatrix = []
    for i in range(len(cumulativeProbabilities)):
        bogJohnMatrix.append((wordList[i], relativeFrequencies[i], cumulativeProbabilities[i]))
    
    # print bogJohnMatrix
    return bogJohnMatrix

def newSentence(bogJohnMatrix):
    wordList = [newWord(bogJohnMatrix) for i in range(10)]
    wordList[0] = wordList[0].title()
    completedSentence = ""
    for word in wordList:
        completedSentence += (word + " ")
    completedSentence = completedSentence[:-1] # remove last space
    completedSentence += "."
    return completedSentence

def newWord(bogJohnMatrix):
    randomDecimal = randint(0, 10000000)/10000000.0
    runningMax = 0.0
    selectedWord = ""
    for word in bogJohnMatrix:
        if word[2] > runningMax:
            runningMax = word[2]
            selectedWord = word[0]
        if runningMax > randomDecimal:
            break
    return selectedWord

main()
