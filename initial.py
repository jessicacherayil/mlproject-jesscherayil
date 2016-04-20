# -*- coding: utf-8 -*-

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

    for page_num in range(len(sortedNums)-1):
        start = textList.index('<' +str(sortedNums[page_num]) + '>')
        if page_num != len(sortedNums-1):
            end = textList.index('<' + str(sortedNums[page_num + 1]) + '>')
        else:
            end = len(textList)-1
        pageDict[sortedNums[page_num]] = textList[start+1:end]

    return pageDict
        
def characterFreq(pageDict, characters):
    """Given a dictionary mapping page numbers to a list of words on that
    page and a list of characters, create a dictionary where each key is a page
    number and each value is another dictionary. In this other dictionary, each
    key is a character and the value is the number of times the character is 
    mentioned on that page"""
    '''{page number: {character: freq, character: freq}}'''
    
    joinedChars = [character.replace(" ", "").lower() for character in characters]
    
    freqDict = {}
    
    for page in pageDict:
        inner = {}
        for character in joinedChars:
            noSpacesText = ''.join(pageDict[page]).lower()
            print character
            if character in noSpacesText:
                readableName = characters[joinedChars.index(character)]
                inner[readableName] = noSpacesText.count(character)
                
        freqDict[page] = inner
                
    return freqDict
    
    
    
characters = ['Dauphine', 'MarieStuart', 'reine d\'Ecosse', 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Duchesse de Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Le Roi', 'Henri Second', 'Duc de Nemours', 'La Reine', 'Catherine de Medicis',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'premier valet de chambre', 'Chastelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'Monsieur de Ferrare', 'Espagnols', 'Gentilhomme de Monsieur de Cleves', 'ecuyer ami du gentilhomme',
'homme du magasin de soie']

#characters2 = ['ladauphine', 'mariestuart', 'reined\'ecosse', 'mademoiselledechartres', 'princessedeclèves',
#'monsieurdeclèves', 'leprincedeclèves', 'madamedechartres', 'vidamedechartres', 'lacour', 'laduchessedevalentinois',
#'dianedepoitiers', 'margueritedefrance', 'leroi', 'henrisecond', 'ducdenemours', 'lareine', 'catherinedemédicis',
#'lechevalierdeguise', 'cardinaldelorraine', 'sancerre', 'premiervaletdechambre', 'chastelart', 
#'lecomtedemontgomery', 'monsieurdemontmorency', 'leschirurgiens', 'connétabledemontmorency', 'monsieurdeguise',
#'monsieurdeferrare', 'lesespagnols', 'legentilhommedemonsieurdeclèves', 'unécuyeramidugentilhomme',
#'hommedumagasindesoie']

pageDict = eachPageText('novel.txt')
print characterFreq(pageDict, characters)
    
	
