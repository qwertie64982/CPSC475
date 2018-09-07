'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Project 2: This project demonstrates counting how many times a substring occurs within a text file
Due: 2018-09-07 18:00 PDT
'''

def my_open():
    while(True):
        fin = raw_input('Enter an input file name (must exist):\n')
        try:
            fin = open(fin, 'r')
            break
        except:
            print("Invalid file name.  Try again.")
    return fin

def search_file(fin):
    string = fin.read()
    subStr = raw_input("Enter a substring:\n")
    return countSub(string, subStr)

def searchSub(string,subStr,posStr_in):
    posSub = 0;
    posStr = posStr_in
    while (posSub < len(subStr)):
        if string[posStr] == subStr[posSub]:
            posSub = posSub + 1
            posStr = posStr + 1
        else:
            return -1
    return posStr_in

def countSub(string, subStr):
    posStr = 0
    numberOccurrances = 0
    lastSub = len(string) - len(subStr)

    while (posStr <= lastSub):
        pos = searchSub(string, subStr, posStr)
        if (pos >= 0):
            numberOccurrances += 1
        posStr += 1
    return numberOccurrances

def main():
    fin = my_open()

    occurrances = search_file(fin)
    fin.close()
    print occurrances



main()
