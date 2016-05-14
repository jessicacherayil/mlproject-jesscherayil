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
    
    ##SPECIAL CASES## e.g. character name split over page
    if page_num == 235: 
        charFreq['homme du magasin de soie'] = eachPageText('novel.txt')[235].count('homme')
        
    if page_num == 89:
        charFreq['Cardinal de Lorraine'] += 1
        
    if page_num == 241:
        charFreq['Monsieur de Cleves'] += 1
    
    if 'reine d\'Ecosse' in charFreq:
        if 'Dauphine' in charFreq: 
            charFreq['Dauphine'] += charFreq['reine d\'Ecosse']
        else:
            charFreq['Dauphine'] = charFreq['reine d\'Ecosse']
        del charFreq['reine d\'Ecosse']
        
    if 'Mademoiselle de Chartres' in charFreq:
        if 'Princesse' in charFreq: 
            charFreq['Princesse'] += charFreq['Mademoiselle de Chartres']
        else: 
            charFreq['Princesse'] = charFreq['Mademoiselle de Chartres']
        del charFreq['Mademoiselle de Chartres']
        
    if 'Madame de Cleves' in charFreq:
        if 'Princesse' in charFreq: 
            charFreq['Princesse'] += charFreq['Madame de Cleves']
        else:
            charFreq['Princesse'] = charFreq['Madame de Cleves']
        del charFreq['Madame de Cleves']
        
    if 'Diane de Poitiers' in charFreq:
        if 'Valentinois' in charFreq: 
            charFreq['Valentinois'] += charFreq['Diane de Poitiers']
        else:
            charFreq['Valentinois'] = charFreq['Diane de Poitiers']
        del charFreq['Diane de Poitiers']
        
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
    '''{page number: {character: freq, character: freq, ...}}'''
    
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
    '''print frequency dictionary nicely'''
    for page_num in freqDict.keys():
        print "PAGE " + str(page_num) + ":"

        for char, freq in freqDict[page_num].iteritems():
            if freq > 1: 
                print str(char) + " appears " + str(freq) + " times"
            else: 
                print str(char) + " appears " + str(freq) + " time"
        print '\n'
        
def getNumMentionsPerPage(character):
    '''get mentions of each character on each page. not really worth using anymore'''
    pageDict = eachPageText('novel.txt')
    d = characterFreq(pageDict, characters)
    mentions = [] #list of lists. Inner list contains page, charFrequency
    
    for i in range(75,254):
        if i in d:
            if character in d[i]:
                mentions.append(d[i][character])
            else:
                mentions.append(0)
        else: #blank pages 
            mentions.append(0)
    return mentions
    
def getNumMentionsInRange(character, chunk):
    '''Input: character (string), chunk (int, how many pages
    counted at a time)
    Output: list where list[0] is how many times the character
    is mentioned in the first chunk pages'''
    
    charDict = characterFreq(pageDict, characters)
    mentions = []
    
    for i in range(75,254, chunk):
        countMentions = 0
        for j in range(i, i+chunk):
            if j in charDict: 
                if character in charDict[j]:
                    countMentions += charDict[j][character]
                    
        mentions.append(countMentions)
    
    return mentions
    
    
    
characters = ['Madame de Cleves','Dauphine', 'reine d\'Ecosse', 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'la Reine',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'premier valet de chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'homme du magasin de soie']

pageDict = eachPageText('novel.txt')

d = characterFreq(pageDict, characters)
print d

#ISSUES:

#homme du magasin de soie is difficult -- maybe check if page is 235 AND count 'homme' 
#overcounting la reine b/c of "la reine" and "reine d'ecosse" --> check proximity thing or just check if ecosse comes after
#monsieur/madame stuff --> check proximity thing

#visualization stuff --> matplotlib plugin for d3.js
    #input: start page num and end page num, output: pie/bar showing each character's mentions over these pages
    #input: a character, output: how many times each character appears "near" this character. define "near" 
        #as a certain number of pages around the page of input character (like window) 
    #pages , stacked bar plot

#TODO;
#set of variants
#find num pronouns on each page - french stanford corenlp POS tagger
#more plotting stuff  
#run parser