'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This project graphs interest of a specific word in US Presidential inaugural addresses over time
Due: 2018-09-14 18:00 PDT
'''

import matplotlib.pyplot as plt
import pickle

# loads the addresses and years
def loadAddresses():
    inFile = open('proj3.pkl', 'r')
    addressesTokenized = pickle.load(inFile)
    years = pickle.load(inFile)
    inFile.close()
    return addressesTokenized, years

# counts how many times targetWord is found in addressesTokenized
def countWord(targetWord, addressesTokenized):
    wordCounts = []
    for address in addressesTokenized:
        wordCount = 0
        for word in address:
            if word == targetWord:
                wordCount += 1
        wordCounts.append(wordCount)
    return wordCounts

# renders and show the graph
def graphUsage(years, targetWordOccurrances):
    plt.plot(years, targetWordOccurrances)
    plt.show()

# driver function
def main():
    # get tokenized addresses
    addressesTokenized, years = loadAddresses()
    
    # find/count word in addresses
    targetWord = raw_input("Target word: ")
    targetWordOccurrances = countWord(targetWord.lower(), addressesTokenized)
    
    # graph word usage
    graphUsage(years, targetWordOccurrances)

main()
