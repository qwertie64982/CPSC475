'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 7A: This program tokenizes the shakespeare corpus
Usage: python proj7a.py
Due: 2018-11-09 18:00 PDT
'''

from nltk import bigrams
import re

def main():
    rawFileData = readFile("shakespeare.txt")
    tokenizedCorpus = tokenize(rawFileData)
    bigramsList = generateBigrams(tokenizedCorpus)
    print bigramsList[0:10]
    
def readFile(filename):
    try:
        inFile = open(filename, "r")
    except:
        print("File read error")
        raise SystemExit
    
    # Encode as ASCII
    # Decoding as utf-8-sig removes the BOM
    # Encoding with "ignore" removes issues like Unicode character 0x2019
    return inFile.read().decode("utf-8-sig").encode("ascii", "ignore")

def tokenize(rawString):
    tokenizedCorpus = [[word for word in sentence.split()] for sentence in rawString.splitlines()]
    
    # make words only lowercase basic Latin letters, as well as ' and -
    for i, sentence in enumerate(tokenizedCorpus):
        for j, word in enumerate(sentence):
            tokenizedCorpus[i][j] = re.sub("[.,:;?!()`\"]+|[0-9]+", "", word.lower()) # make lowercase, remove numbers, remove special chars except ' and -
        # tokenizedCorpus[i] = filter(None, tokenizedCorpus[i]) # remove empty strings from sentences
        # tokenizedCorpus[i] = filter(lambda word: word != "\'\'" and word != "--", tokenizedCorpus[i]) # remove strange '' and -- words
    tokenizedCorpus = filter(None, tokenizedCorpus) # remove empty sentences []
    tokenizedCorpus = filter(lambda word: word != [""], tokenizedCorpus) # remove empty sentences [""]
    
    # add <s> and </s> tags
    for i, sentence in enumerate(tokenizedCorpus):
        tokenizedCorpus[i].insert(0, "<s>") # add <s> to beginning of all sentences
        tokenizedCorpus[i].append("</s>") # add </s> to end of all sentences
    
    return tokenizedCorpus

def generateBigrams(tokenizedCorpus):
    bigramsList = []
    for sentence in tokenizedCorpus:
        bigramsList.extend(list(bigrams(sentence)))
    return bigramsList

main()
