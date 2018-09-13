'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This project graphs interest of a specific word in US Presidential inaugural addresses over time
Due: 2018-09-14 18:00 PDT
'''

from nltk.corpus import inaugural
import pickle
import re

# creates addresses, a list of raw inaugural addresses from nltk.corpus.inaugural
def makeList():
    fileIds = inaugural.fileids()
    addresses = [address for address in fileIds]
    return addresses

# turns addresses into addressesTokenized, converting everything to lowercase words with no extraneous characters except '
# also returns a list of year integers as a parallel list to addressesTokenized
def tokenize(addresses):
    outFile = open('proj3.pkl', 'w')
    addressesTokenized = []
    years = []
    for address in addresses:
        addressText = ''
        years.append(int(address[:4])) # grab year from filename to make x-axis
        for sent in inaugural.sents(address):
            sent = ' '.join(sent)
            addressText += (sent + ' ')
        
        addressText = re.sub(r" ' ", "'", addressText) # recombine contractions (ex. don't, they're, America's, it's, etc.)
        words = re.findall(r"[a-zA-Z0-9']+", addressText) # separate out words into a list and remove extraneous characters
        words = [word.lower() for word in words] # make every word lowercase so search is case-insensitive
        
        addressesTokenized.append(words)
        # pickle.dump(words, outFile)
    pickle.dump(addressesTokenized, outFile)
    pickle.dump(years, outFile)
    outFile.close()

# driver function
def main():
    # get addresses
    addresses = makeList()
    tokenize(addresses)

main()
