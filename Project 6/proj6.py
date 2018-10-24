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

# main driver function
def main():
    # get corpus from nltk and tokenize
    rawCorpus = brown.sents(categories = "editorial")
    tokenizedCorpus = tokenizeCorpus(rawCorpus)
    
    # calculate unigram frequencies
    bogJohnMatrix = calculateFrequencies(tokenizedCorpus)
    
    # generate 5 sentences and print them
    for i in range(5):
        print(newSentence(bogJohnMatrix))

# remove most punctuation and transform all words to lowercase
def tokenizeCorpus(rawCorpus):
    tokenizedCorpus = [[word.encode("ascii") for word in sentence] for sentence in rawCorpus]
    
    for i, sentence in enumerate(tokenizedCorpus):
        for j, word in enumerate(sentence):
            tokenizedCorpus[i][j] = re.sub("[.,:;?!()`\"]+", "", word.lower()) # make lowercase and remove special chars except ' and -
        tokenizedCorpus[i] = filter(None, tokenizedCorpus[i]) # remove empty strings from sentences
        tokenizedCorpus[i] = filter(lambda word: word != "\'\'" and word != "--", tokenizedCorpus[i]) # remove strange '' and -- words
    
    return tokenizedCorpus

# calculate relative frequencies and cumulative probabilities for each word
# this is very memory inefficient for the sake of simplicity and easiness to read
def calculateFrequencies(tokenizedCorpus):
    # sum every word
    wordOrder = {} # dictionary that associates each word with its index in all the parallel lists (so they are kept in the order in which they were found)
    wordSums = [] # sum of each word in the corpus
    wordList = [] # each word in the corpus (in order, unlike wordOrder, so words can be found by index)
    wordCount = 0 # total number of words in the corpus
    for sentence in tokenizedCorpus:
        for word in sentence:
            wordCount += 1
            if word in wordOrder: # if the word has been seen before in the corpus
                wordSums[wordOrder[word]] += 1
            else:
                wordOrder[word] = len(wordOrder)
                wordSums.append(1)
                wordList.append(word)
    
    # calculate relative frequencies (# of this word's occurrances / total word count)
    relativeFrequencies = [wordSum / float(wordCount) for wordSum in wordSums]
    
    # calculate cumulative probabilities (each relative frequency + every relative frequency before it)
    cumulativeProbabilities = [relativeFrequencies[0]]
    for i in range(1, len(relativeFrequencies)):
        cumulativeProbabilities.append(relativeFrequencies[i] + cumulativeProbabilities[i-1])
    
    # assemble these all into one list of tuples that can be easily accessed
    # this is the Bogensberger-Johnson matrix, as seen on the P6 assignment sheet
    bogJohnMatrix = []
    for i in range(len(cumulativeProbabilities)):
        bogJohnMatrix.append((wordList[i], relativeFrequencies[i], cumulativeProbabilities[i]))
    
    return bogJohnMatrix

# generate a new sentence based on the words in the Bogensberger-Johnson matrix
# the sentence is 10 words long, ends with a period, and the first letter is capitalized
# because this only uses unigrams, the sentence doesn't make much sense
def newSentence(bogJohnMatrix):
    wordList = [newWord(bogJohnMatrix) for i in range(10)]
    wordList[0] = wordList[0].title()
    completedSentence = ""
    for word in wordList:
        completedSentence += (word + " ")
    completedSentence = completedSentence[:-1] # remove last space
    completedSentence += "."
    return completedSentence

# generates a new word based on the words in the Bogensberger-Johnson matrix
def newWord(bogJohnMatrix):
    randomDecimal = randint(0, 10000000) / 10000000.0
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
