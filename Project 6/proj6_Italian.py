'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 6: This program explores unigrams by generating an Italian word based on a corpus. 
Usage: python proj6_Italian.py
Due: 2018-10-26 18:00 PDT
'''

from random import randint

def main():
    # tuples contain: (word, relative frequency, cumulative probability)
    corpus = [("al", .3, .3), ("tavola", .1, .4), ("non", .05, .45), ("ci", .05, .5), ("invecchia", .4, .9), ("mai", .1, 1)]
    # corpus = sorted(corpus, key=lambda cumulativeFreq: cumulativeFreq[2]) # sort corpus by the third item in every tuple (cumulative probability) - NOT NEEDED B/C LIST IS ORDERED
    
    randomDecimal = randint(0, 100)/100.0
    runningMax = 0.0
    selectedWord = ""
    for word in corpus:
        if word[2] > runningMax:
            runningMax = word[2]
            selectedWord = word[0]
        if runningMax > randomDecimal:
            break
    print selectedWord,
    print randomDecimal,
    print runningMax

main()
