from nltk.corpus import inaugural
import re
import pickle

def makeList():
    fileIds = inaugural.fileids()
    addresses = [address for address in fileIds]
    return addresses

def tokenize(addresses):
    outFile = open('proj3.txt', 'w')
    for address in addresses:
        addressText = ''
        for sent in inaugural.sents(address):
            sent = ' '.join(sent)
            addressText += (sent + ' ')
        
        addressText = re.sub(r" ' ", "'", addressText) # recombine contractions
        words = re.findall(r"[a-zA-Z0-9']+", addressText) # separate out words into a list
        
#        for word in words:
#            outFile.write(word + ' ')
        pickle.dump(words, outFile)

def main():
    addresses = makeList()
    tokenize(addresses)
    # next stuff

main()
