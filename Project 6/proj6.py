'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 6: This program explores unigrams by generating 5 sentences from a corpus
Usage: python proj6.py
Due: 2018-10-26 18:00 PDT
'''

from nltk.corpus import brown
import re

def main():
    tmp = brown.sents(categories = "editorial")
    new = [[word.encode("ascii") for word in sentence] for sentence in tmp]
    
    for i, sentence in enumerate(new):
        for j, word in enumerate(sentence):
            new[i][j] = re.sub("[.,?!\"]+", "", word.lower()) # make lowercase and remove special chars except apostrophe
        new[i] = filter(None, new[i]) # remove empty strings
    
    print new[0]
    print new[1]

main()
