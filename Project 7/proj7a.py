'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 7A: This program tokenizes the Shakespeare corpus and generates n-grams/probabilities
Usage: python proj7a.py
Due: 2018-11-09 18:00 PDT
'''

import nltk
import pickle
import re

# main driver function
def main():
    # read and tokenize data
    print("Reading file...")
    rawFileData = readFile("shakespeare.txt")
    print("Tokenizing...")
    tokenizedCorpus = tokenize(rawFileData)
    
    # generate n-grams
    print("Generating unigrams...")
    unigramsList = generateUnigrams(tokenizedCorpus)
    print("Generating bigrams...")
    bigramsList = generateBigrams(tokenizedCorpus)
    print("Generating trigrams...")
    trigramsList = generateTrigrams(tokenizedCorpus)
    print("Generating quadgrams...")
    quadgramsList = generateQuadgrams(tokenizedCorpus)
    
    # calculate Bogensberger-Johnson matrices
    print("Calculating unigrams Bogensberger-Johnson matrix...")
    unigramsMatrix = calculateBGM(unigramsList)
    print("Calculating bigrams Bogensberger-Johnson matrix...")
    bigramsMatrix = calculateBGM(bigramsList)
    print("Calculating trigrams Bogensberger-Johnson matrix...")
    trigramsMatrix = calculateBGM(trigramsList)
    print("Calculating quadgrams Bogensberger-Johnson matrix...")
    quadgramsMatrix = calculateBGM(quadgramsList)
    
    # write matrices to pickle file
    try:
        outFile = open("proj7b.pkl", "w+")
    except:
        print("File write error")
        raise SystemExit
    print("Writing unigrams matrix to file...")
    pickle.dump(unigramsMatrix, outFile)
    print("Writing bigrams matrix to file...")
    pickle.dump(bigramsMatrix, outFile)
    print("Writing trigrams matrix to file...")
    pickle.dump(trigramsMatrix, outFile)
    print("Writing quadgrams matrix to file...")
    pickle.dump(quadgramsMatrix, outFile)
    outFile.close()
    
    print("Successfully generated (1-4)-grams and wrote to proj7b.pkl.")

# read the corpus from .txt file and exit if it fails
# return the entire file as a string encoded as ASCII
def readFile(filename):
    try:
        inFile = open(filename, "r")
    except:
        print("File read error")
        raise SystemExit
    
    # encode as ASCII
    # decoding as utf-8-sig removes the BOM
    # encoding with "ignore" removes issues like Unicode character 0x2019
    rawString = inFile.read().decode("utf-8-sig").encode("ascii", "ignore")
    
    inFile.close()
    return rawString

# tokenize the file (as a string) into a list of sentences, which are lists of words
# words are only lowercase basic Latin letters which can have apostrophes and hyphens
# all sentences begin with <s> and end with </s>
def tokenize(rawString):
    tokenizedCorpus = [[word for word in sentence.split()] for sentence in rawString.splitlines()]
    
    # make words only lowercase basic Latin letters, as well as ' and -
    for i, sentence in enumerate(tokenizedCorpus):
        for j, word in enumerate(sentence):
            tokenizedCorpus[i][j] = re.sub("[.,:;?!()`\"\[\]]+|[0-9]+", "", word.lower()) # make lowercase, remove numbers, remove special chars except ' and -
        # tokenizedCorpus[i] = filter(None, tokenizedCorpus[i]) # remove empty strings from sentences
        # tokenizedCorpus[i] = filter(lambda word: word != "\'\'" and word != "--", tokenizedCorpus[i]) # remove strange '' and -- words
    tokenizedCorpus = filter(None, tokenizedCorpus) # remove empty sentences []
    tokenizedCorpus = filter(lambda word: word != [""], tokenizedCorpus) # remove empty sentences [""]
    
    # add <s> and </s> tags
    for i, sentence in enumerate(tokenizedCorpus):
        tokenizedCorpus[i].insert(0, "<s>") # add <s> to beginning of all sentences
        tokenizedCorpus[i].append("</s>") # add </s> to end of all sentences
    
    return tokenizedCorpus

# generate unigrams (without <s> and </s> tags)
# return a list of every word in the corpus in order
def generateUnigrams(tokenizedCorpus):
    unigramsList = []
    for sentence in tokenizedCorpus:
        for word in sentence:
            if word != "<s>" and word != "</s>":
                unigramsList.append(word)
    return unigramsList

# generate bigrams
# return a list of all possible bigrams from the corpus, in order
def generateBigrams(tokenizedCorpus):
    bigramsList = []
    for sentence in tokenizedCorpus:
        bigramsList.extend(list(nltk.bigrams(sentence)))
    return bigramsList

# generate trigrams
# return a list of all possible trigrams from the corpus, in order
def generateTrigrams(tokenizedCorpus):
    trigramsList = []
    for sentence in tokenizedCorpus:
        if len(sentence) >= 3:
            trigramsList.extend(list(nltk.trigrams(sentence)))
    return trigramsList

# generate quadgrams
# return a list of all possible quadgrams from the corpus, in order
def generateQuadgrams(tokenizedCorpus):
    quadgramsList = []
    for sentence in tokenizedCorpus:
        if len(sentence) >= 4:
            quadgramsList.extend(list(nltk.ngrams(sentence, 4)))
    return quadgramsList

# calculate relative frequencies and cumulative probabilities for each n-gram
# this is very memory inefficient for the sake of simplicity and easiness to read
def calculateBGM(ngramsList):
    # sum every n-gram
    ngramOrder = {} # dictionary that associates each n-gram with its index in all the parallel lists (so they are kept in the order in which they were found)
    ngramSums = [] # sum of each n-gram in the list
    ngramList = [] # each n-gram in the list
    ngramCount = 0 # total number of n-grams in the list
    for ngram in ngramsList:
        ngramCount += 1
        if ngram in ngramOrder: # if the word has been seen before in the corpus
            ngramSums[ngramOrder[ngram]] += 1
        else:
            ngramOrder[ngram] = len(ngramOrder)
            ngramSums.append(1)
            ngramList.append(ngram)
    
    # calculate relative frequencies (# of this n-gram's occurrances / total n-gram count)
    relativeFrequencies = [ngramSum / float(ngramCount) for ngramSum in ngramSums]
    
    # calculate cumulative probabilities (each relative frequency + every relative frequency before it)
    cumulativeProbabilities = [relativeFrequencies[0]]
    for i in range(1, len(relativeFrequencies)):
        cumulativeProbabilities.append(relativeFrequencies[i] + cumulativeProbabilities[i-1])
    
    # assemble these all into one list of tuples that can be easily accessed
    # this is the Bogensberger-Johnson matrix, as seen on the P6 assignment sheet
    bogJohnMatrix = []
    for i in range(len(cumulativeProbabilities)):
        bogJohnMatrix.append((ngramList[i], relativeFrequencies[i], cumulativeProbabilities[i]))
    
    return bogJohnMatrix

main()
