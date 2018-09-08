'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This project graphs interest of a specific word in US Presidential inaugural addresses over time
Due: 2018-09-14 18:00 PDT
'''

import matplotlib.pyplot as plt
from nltk.corpus import inaugural # TODO: Can I assume graders will have these installed?
import pickle
import re

YEARS = [1789, 1793, 1797, 1801, 1805, 1809, 1813, 1817, 1821, 1825, 1829, 1833, 1837, 1841, 1845, 1849, 1853, 1857, 1861, 1865, 1869, 1873, 1877, 1881, 1885, 1889, 1893, 1897, 1901, 1905, 1909, 1913, 1917, 1921, 1925, 1929, 1933, 1937, 1941, 1945, 1949, 1953, 1957, 1961, 1965, 1969, 1973, 1977, 1981, 1985, 1989, 1993, 1997, 2001, 2005, 2009]

def makeList():
    fileIds = inaugural.fileids()
    addresses = [address for address in fileIds]
    return addresses

def tokenize(addresses):
    outFile = open('proj3.txt', 'w')
    addressesTokenized = []
    for address in addresses:
        addressText = ''
        for sent in inaugural.sents(address):
            sent = ' '.join(sent)
            addressText += (sent + ' ')
        
        addressText = re.sub(r" ' ", "'", addressText) # recombine contractions (ex. don't, they're, America's, it's, etc.)
        words = re.findall(r"[a-zA-Z0-9']+", addressText) # separate out words into a list
        
#        for word in words:
#            outFile.write(word + ' ')
        addressesTokenized.append(words)
        pickle.dump(words, outFile) # TODO: Write lists to .txt file like this?
    outFile.close()
    return addressesTokenized

def countWord(targetWord, addressesTokenized): # TODO: Should I check case-insensitive?
    wordCounts = []
    for address in addressesTokenized:
        wordCount = 0
        for word in address:
            if word == targetWord:
                wordCount += 1
        wordCounts.append(wordCount)
    return wordCounts

def graphUsage(targetWordOccurrances):
    plt.plot(YEARS, targetWordOccurrances) # TODO: I want to make this prettier. If I install pyplot, will graders be able to run it?
    plt.show()

def main():
    # get addresses
    addresses = makeList()
    addressesTokenized = tokenize(addresses)
    
    # find/count word in addresses
    targetWord = raw_input("Target word: ")
    targetWordOccurrances = countWord(targetWord, addressesTokenized)
    
    # graph word usage
    graphUsage(targetWordOccurrances)

main()
