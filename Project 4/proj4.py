'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 4: This program is a Soundex algorithm FST
Usage: python proj4.py {name}
Due: 2018-09-28 18:00 PDT
'''

import re
import sys

# main driver function
def main():
    if len(sys.argv) != 2: # if user provides wrong number of arguments
        print("Usage: python proj4.py {name}")
    else:
        inString = str(sys.argv[1]) # get input as argument 1
        outString = soundex(inString) # run through Soundex
        print(inString + " -> " + outString) # print result

# soundex converter function
# in: alpha string length >= 1
# out: alphanumeric string length 4
def soundex(inString):
    if len(inString) == 1: # the program will work without this conditional but it's more efficient this way
        return inString + "000" # concatenate 0s to make it length 4
    else:
        # preserve first character
        outString = inString[0] # put first character in outString
        inString = inString[1:] # remove first character from inString
        # from here, the program operates on everything but the first character
        
        # make rest of name lowercase for easier processing
        inString = inString.lower()
        
        # [b, f, p, v] -> 1
        inString = re.sub("[bfpv]", "1", inString)
        
        # [c, g, j, k, q, s, x, z] -> 2
        inString = re.sub("[cgjkqsxz]", "2", inString)
        
        # [d, t] -> 3
        inString = re.sub("[dt]", "3", inString)
        
        # [l] -> 4
        inString = re.sub("[l]", "4", inString)
        
        # [m, n] -> 5
        inString = re.sub("[mn]", "5", inString)
        
        # [r] -> 6
        inString = re.sub("[r]", "6", inString)
        
        # reduce multiple numbers in a row to one number (ex. 222 -> 2)
        inString = re.sub("([0-9])\\1+", "\\1", inString)
        
        # remove [vowels + y, w, h]
        inString = re.sub("[aeiouywh]", "", inString)
        
        # lengthen/shorten to number section to 3 characters in length
        inStringLength = len(inString)
        if inStringLength > 3:
            inString = inString[:3]
        elif inStringLength == 2:
            inString += "0"
        elif inStringLength == 1:
            inString += "00"
        elif inStringLength == 0:
            inString = "000"
        
        # concatenate first character and processed name
        outString += inString
        return outString

main()
