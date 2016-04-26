# -*- coding: utf-8 -*-

'''Author: Jess Cherayil'''

import re
import codecs
import unicodedata

def remove_accents(input_str):
    """Given string input, returns the same string with no accents"""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def search(regex,text):
    """Find all matches of regex in the provided text"""
    regexp = re.compile(regex)
    results = set()
    for phrase in regexp.findall(text):
        results.add(phrase)
    return results

def eachPageText(filename):
    """Given a filename, opens Princesse de Cleves text file, 
    creates a dictionary where each key is a page number, and each
    value is a list of words on that page"""
    
    text = remove_accents(codecs.open(filename, 'r','utf8').read())
    textList = text.split()

    pageDict = {} #make dict where key is page number, value is text split into words 
    page_nums = search(r'(<[0-9]+>)',text.strip()) #use regex to find all page numbers in text

    for page_num in page_nums: 
        pageDict[int(page_num[1:-1])] = '' #convert page num from str '<###>' format to int ### format
    
    sortedNums = sorted(pageDict.keys())

    for page_num in range(len(sortedNums)):
        start = textList.index('<' +str(sortedNums[page_num]) + '>')
        if page_num != 176:
            end = textList.index('<' + str(sortedNums[page_num + 1]) + '>')
        else:
            end = len(textList)-24
        
        
        pageDict[sortedNums[page_num]] = textList[start+1:end]

 
    return pageDict
    
def consolidate(charFreq,page_num):
    '''Given an inner dictionary mapping each character
    to its frequency on a page, iterate to accumulate counts
    among characters with several nicknames'''
    
    if page_num == 235: 
        pass
        #word 'homme' is there
    
    if 'Dauphine' in charFreq and 'reine d\'Ecosse' in charFreq:
        charFreq['Dauphine'] += charFreq['reine d\'Ecosse']
        del charFreq['reine d\'Ecosse']
    if 'Mademoiselle de Chartres' in charFreq and 'Princesse' in charFreq:
        charFreq['Princesse'] += charFreq['Mademoiselle de Chartres']
        del charFreq['Mademoiselle de Chartres']
    if 'reine d\'Ecosse' in charFreq:
        del charFreq['reine d\'Ecosse']
    if 'Mademoiselle de Chartres' in charFreq:
        del charFreq['Mademoiselle de Chartres']
    if 'La Reine' in charFreq:
        charFreq['Catherine de Medicis'] = charFreq['La Reine']
        del charFreq['La Reine']
    return charFreq
        
        
def characterFreq(pageDict, characters):
    """Given a dictionary mapping page numbers to a list of words on that
    page and a list of characters, create a dictionary where each key is a page
    number and each value is another dictionary. In this other dictionary, each
    key is a character and the value is the number of times the character is 
    mentioned on that page"""
    '''{page number: {character: freq, character: freq}}'''
    
    joinedChars = [character.replace(" ", "").lower() for character in characters] #character name with no spaces
    
    freqDict = {}
    
    for page in pageDict:
        inner = {}
        for character in joinedChars:
            noSpacesText = ''.join(pageDict[page]).lower() #page with no spaces
            
            if character in noSpacesText:
                readableName = characters[joinedChars.index(character)]
                inner[readableName] = noSpacesText.count(character)
                
        freqDict[page] = consolidate(inner,page)

 
    return freqDict
    
def printCharFreq(freqDict):
    for page_num in freqDict.keys():
        print "PAGE " + str(page_num) + ":"

        for char, freq in freqDict[page_num].iteritems():
            print str(char) + " appears " + str(freq) + " times"
        print '\n'
            
    
    
characters = ['Dauphine', 'reine d\'Ecosse', 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'la Reine',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'premier valet de chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer ',
'homme du magasin de soie']


#ISSUES:
#names broken up over pages: 
    #cardinal de lorraine 89
    #de Nemours 138, 223 -- probably resolved
    #monsieur de cleves 241
#overcounting la reine
#homme du magasin de soie is difficult -- maybe check if page is 235 AND word 'homme' is there


pageDict = eachPageText('novel.txt')
#print pageDict
d = characterFreq(pageDict, characters)
print d
#printCharFreq(d)

#print dictionary nicely
#monsieur/madame stuff
#visualization stuff
#matplotlib plugin for d3.js

