# -*- coding: utf-8 -*-

'''Author: Jess Cherayil'''

import re
import codecs
import unicodedata
import csv
import numpy as np

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



def newCharFreq(filename):

    characters = ['MadamedeCleves','Dauphine', 'reine', 'Mademoiselle', 'Princesse',
    'MonsieurdeCleves', 'Prince', 'MadamedeChartres', 'Vidame', 'cour', 'Valentinois',
    'Diane', 'Marguerite', 'Roi', 'roi', 'Henri', 'Nemours', 'Reine',
    'Chevalier', 'Cardinal', 'Sancerre', 'valet', 'Chatelart', 
    'Montgomery', 'MonsieurdeMontmorency', 'Chirurgien', 'Connetable', 'MonsieurdeGuise',
    'Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
    'soie']



    text = remove_accents(codecs.open(filename, 'r','utf8').read())
    textList = text.split()
    textList = np.array(textList)
    indices = {}

    for word in range(len(textList)): 
        if textList[word] == 'Madame':
            if textList[word+1] == 'de' and textList[word+2]=='Cleves':
                textList[word] == 'MadamedeCleves'
                textList = textList[:word+1] + textList[word+3:]
            elif textList[word+1] == 'de' and textList[word+2]=='Chartres':
                textList[word] == 'MadamedeChartres'
                textList = textList[:word+1] + textList[word+3:]
        elif textList[word] == 'Monsieur':
            if textList[word+1] == 'de' and textList[word+2]=='Cleves':
                textList[word] == 'MonsieurdeCleves'
                textList = textList[:word+1] + textList[word+3:]
            elif textList[word+1] == 'de' and textList[word+2]=='Montmorency':
                textList[word] == 'MonsieurdeMontmorency'
                textList = textList[:word+1] + textList[word+3:]
            elif textList[word+1] == 'de' and textList[word+2]=='Guise':
                textList[word] == 'MonsieurdeGuise'
                textList = textList[:word+1] + textList[word+3:]


    for character in characters:
        indices[character] = np.where(textList == character)[0]

    return indices

#print newCharFreq('novel.txt') 
    
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
    indexDict = {}
    tList = []
    
    for page in pageDict:
        inner = {}

        for character in joinedChars:
            noSpacesText = ''.join(pageDict[page]).lower() #page with no spaces
            tList.append(noSpacesText) 
            
            if character in noSpacesText:
                if page not in indexDict:
                    indexDict[page] = [(character, noSpacesText.index(character))]
                elif page in indexDict: 
                    indexDict[page].append((character, noSpacesText.index(character)))
                readableName = characters[joinedChars.index(character)]
                inner[readableName] = noSpacesText.count(character)
                
        freqDict[page] = consolidate(inner,page)

 
    return freqDict, indexDict,tList


 
    
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
    '''get mentions of each character on each page'''
    pageDict = eachPageText('novel.txt')
    d,i,t = characterFreq(pageDict, characters)
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
    
    charDict,iDict = characterFreq(pageDict, characters)
    mentions = []
    
    for i in range(75,254, chunk):
        countMentions = 0
        for j in range(i, i+chunk):
            if j in charDict: 
                if character in charDict[j]:
                    countMentions += charDict[j][character]
                    
        mentions.append(countMentions)
    
    return mentions
    
def writeToCSV(mentionsDict, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Page Number', 'Character','Number of Mentions'])
        
        for page_num in mentionsDict.keys():
            for character in mentionsDict[page_num].keys():
                writer.writerow([page_num, character, mentionsDict[page_num][character]])


def findVocab(search,vocabulary,pageDict):
    '''given a search space, a target vocabulary, and a dictionary mapping
    page number to the text on each page, return the target words found
    in each search space'''
    result = {}
    for k,v in search.items():
        page = v[0]
        space = v[1]
        start = space[0]
        end = space[1]
        if not start < end:
            temp = start
            start = end
            end = temp
        noSpacesText = ''.join(pageDict[page]).lower()

        text = noSpacesText[start:end]
        for word in vocabulary:
            if word in text:
                if (k,page) not in result: 
                    
                    result[(k,page)] = [word]
                else:
                    
                    result[(k,page)].append(word)

    return result




def avgNumMentionsPerPage(characters):
    avgMention = {}
    for character in characters:
        mentions = getNumMentionsPerPage(character)
        avgMention[character] = sum(mentions)/float(len(mentions))
    return avgMention

##########################################################    
characters = ['Madame de Cleves','Dauphine', 'reine d\'Ecosse', 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'la Reine',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'premier valet de chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'homme du magasin de soie']

characters2 = ['Madame-de-Cleves','Dauphine', 'reine', 'Mademoiselle', 'Princesse',
'MonsieurdeCleves', 'Prince', 'MadamedeChartres', 'Vidame', 'cour', 'Valentinois',
'Diane', 'Marguerite', 'Roi', 'roi', 'Henri', 'Nemours', 'Reine',
'Chevalier', 'Cardinal', 'Sancerre', 'valet', 'Chatelart', 
'Montgomery', 'MonsieurdeMontmorency', 'Chirurgien', 'Connetable', 'MonsieurdeGuise',
'Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'soie']

characters3 = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves',
'monsieurdecleves', 'princedecleves', 'madamedechartres', 'vidamedechartres', 'cour', 'valentinois',
'poitiers', 'marguerite', 'henri', 'roi', 'nemours', 'reine', 
'lorraine', 'sancerre', 'chevalierdeguise', 'valet', 'chatelart', 'duchessedemercoeur',
'marechal', 'ferrare', 'monsieurdeguise', 'd\'orange','montgomery',
 'chirurgiens', 'connetable', 'espagnols', 'gentilhomme', 'ecuyer', 
'martigues', 'soie', 'dampierre', 'elisabeth', 'nevers', 'd\'anville', 
'lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 
'madamedemercoeur', 'navarre']

y = [1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0]

pageDict = eachPageText('novel.txt')
print pageDict

#d,i,t = characterFreq(pageDict, characters)
#print avgNumMentionsPerPage(characters)
#search= findSearchSpace(i)
# vocabulary = ['dit', 'regardait', 'voyait', 'ajout', 'revele', 'montre', 'vint', 'vu', 'rougit', 'dansait', 'donne', 'donnait', 'vol']
# #print findVocab(search, vocabulary,pageDict)
#distance_dict = avgNumWords(search, pageDict)


#print avgNumWordsChar(map(str.lower, characters2),distance_dict)
#print avgNumWordsPrin(map(str.lower, characters2),distance_dict)
#findChar(t, characters)
#print avgNumMentionsPerPage(characters3)
#writeToCSV(d, 'mentions.csv')

#for character in characters:
#    print character, sum(getNumMentionsPerPage(character))

#ISSUES:

#overcounting la reine b/c of "la reine" and "reine d'ecosse" --> check proximity thing or just check if ecosse comes after
#monsieur/madame stuff --> check proximity thing

#TODO;
#search for a set of variants instead of consolidate function
#find num pronouns on each page - french stanford corenlp POS tagger
#run parser