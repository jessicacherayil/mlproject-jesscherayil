'''Author: Jess Cherayil'''

import re
import codecs
import os
import unicodedata
import csv
import numpy as np
import json

def remove_accents(input_str):
	"""Given string input, returns the same string with no accents"""
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii

def textToList(filename):
	'''given a filename, featurize text into list of words, removing accents'''
	text = remove_accents(codecs.open(filename, 'r','utf8').read())
	textList = text.split()
	txtList = [word.lower() for word in textList]
	return txtList

def justText(filename):
	text = remove_accents(codecs.open(filename, 'r','utf8').read())
	return text

def parseText(l):


	for i in range(len(l)-1):

		word = l[i]

		cleves = ['cleves', 'cleves,', 'cleves.']
		chartres = ['chartres', 'chartres,', 'chartres.']
		mercoeur = ['mercoeur', 'mercoeur,', 'mercoeur.']
		
		guise = ['guise', 'guise,', 'guise.']
		nemours = ['nemours', 'nemours,', 'nemours.']


		if word in cleves:

			if l[i-2] == 'monsieur':
				l[i] = 'monsieurdecleves'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'
			elif l[i-2] == 'prince':
				l[i] = 'monsieurdecleves'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'
			elif l[i-2] == 'princesse':
				l[i] = 'princessedecleves'					
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'

			elif l[i-2] == 'madame':
				l[i] = 'princessedecleves'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'



		elif word in chartres:
			if l[i-2] == 'mademoiselle':
				l[i] = 'princessedecleves'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'
			elif l[i-2] == 'madame':
				l[i] = 'madamedechartres'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'
			elif l[i-2] == 'vidame':
				l[i] = 'vidamedechartres'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'

			


		elif word in mercoeur:
			if l[i-2] == 'duchesse':
				l[i] = 'duchessedemercoeur'
			elif l[i-2] == 'madame':
				l[i] = 'duchessedemercoeur'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'

		elif word in guise:
	
			if l[i-2] == 'chevalier':
				l[i] = 'chevalierdeguise'
			elif l[i-2] == 'monsieur':
				l[i] = 'monsieurdeguise'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'

		elif word in nemours:
			if l[i-2] == 'duc':
				l[i] = 'ducdenemours'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'
			elif l[i-2] == 'monsieur':
				l[i] = 'ducdenemours'
				l[i-2] = 'TO-DELETE'
				l[i-1] = 'TO-DELETE'


	new_l = [x for x in l if x != 'TO-DELETE']

	return new_l



def search(regex,text):
	"""Find all matches of regex in the provided text"""
	regexp = re.compile(regex)
	results = set()
	for phrase in regexp.findall(text):
		results.add(phrase)
	return results

def eachPageText(text,l):
	pageDict = {} #make dict where key is page number, value is text split into words 
	page_nums = search(r'(<[0-9]+>)',text.strip()) #use regex to find all page numbers in text

	for page_num in page_nums: 
		pageDict[int(page_num[1:-1])] = '' #convert page num from str '<###>' format to int ### format

	sortedNums = sorted(pageDict.keys())

	for page_num in range(len(sortedNums)):

		start = l.index('<' +str(sortedNums[page_num]) + '>')
		if page_num != 176:
			end = l.index('<' + str(sortedNums[page_num + 1]) + '>')
		else:
			end = len(l)-24

		pageDict[sortedNums[page_num]] = l[start+1:end]

	return pageDict

def mentionsPerPage(pageDict, chars):


	result = {}

	
	for page in pageDict: 
		charCounts = {}
		for char in chars: 

			eachPage = np.asarray(pageDict[page])

			numMentions = len(np.where(eachPage == char)[0])
			
			charCounts[char] = numMentions

		result[page] = charCounts


	return result


def avgMentionsPerPage(mentionDict, chars):
	avgMention = {}
	for char in chars:
		allSum = 0
		for page in mentionDict:
			if mentionDict[page][char] != 0:

				allSum += mentionDict[page][char] 

		avgMention[char] = float(allSum)/len(mentionDict.keys())
	return avgMention




def avgDistance(l, chars):
	'''given the text and a list of characters, 
	return the average distance in number of words
	from a character's mention to a mention of the princess'''

	npl = np.asarray(l)

	princesse = np.where(npl == 'princessedecleves')[0]

	#print 'PRINCESSE', princesse

	charDists = {}
	for char in chars:

		dists = np.append(np.where(npl == char)[0], np.where(npl == char+',')[0])
		np.append(dists, np.where(npl == char+'.')[0])

		charDists[char] = dists


	avgs = {}
	for char in charDists:

		avg = 0
		denom = 1
		for elt in charDists[char]: 
			for i in range(len(princesse)): 
				if princesse[i]>elt:
					avg += (princesse[i]-elt) 
					denom += 1
					break

		avgs[char] = float(avg)/denom-1

	return avgs

def charAvgDistance(l, chars):
	'''given the text and a list of characters, return the average distance
	between a character's mention, and the mention of the next character'''

	npl = np.asarray(l)

	charDists = {}
	for char in chars:
		dists = np.append(np.where(npl == char)[0], np.where(npl == char+',')[0])
		np.append(dists, np.where(npl == char+'.')[0])
		charDists[char] = np.sort(dists)

	mentionAvg = []
	avgs = {}
	for char in charDists:
		
		#print 'CHAR IS', char
		#print 'ELT LENGTH', len(charDists[char])
		avg = 0
		denom = 1
		for elt in charDists[char]: #for every mention of the king
			
			next = []

			for char2 in charDists: #iterate through all other characters

				if char != char2: 

					for elt2 in charDists[char2]: #for each of their mentions

						
						if elt2 > elt: #see if mentioned after, append distance
							next.append((char2,elt2-elt)) 


							break

			if len(next) > 0: 
				so = sorted(next, key =lambda x:x[1])
				mentionAvg.append(so[0][1])
			

		avgs[char] = float(sum(mentionAvg))/len(mentionAvg)				
					
	return avgs

def tfidf_scores(l, characters):
	'''given the text and a list of characters, find their top 10 most commonly
	used words and give tfidf_scores for each character'''

	pass

def findVocab(l, chars,vocab):
	'''return the type of interaction (given by the vocab) between two characters. 
	format: d[char1, char2] = interaction'''
	npl = np.asarray(l)
	result = {}
	charDists = {}
	for char in chars: #create dictionary of indices of character mention in text
		dists = np.append(np.where(npl == char)[0], np.where(npl == char+',')[0])
		np.append(dists, np.where(npl == char+'.')[0])
		charDists[char] = np.sort(dists) 

	for char in charDists:

		for elt in charDists[char]: #for every mention of the king
			next = []
			for char2 in charDists: #iterate through all other characters

				if char != char2: 

					for elt2 in charDists[char2]: #for each of their mentions

						if elt2 > elt: #see if mentioned after, append distance
							next.append((char2,elt2,elt)) 
							break
			if len(next) > 0: 

				so = sorted(next, key =lambda x:x[2]-x[1])
				minVal = so[0]
				for vword in vocab:
					if vword in l[minVal[2]:minVal[1]]:
						if (char,minVal[0]) not in result:

							result[(char,minVal[0])] = [vword]
						else:
							if vword not in result[(char,minVal[0])]:
								result[(char,minVal[0])].append(vword)
							

	return result

def writeInteractions(intDict, filename):
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Initiator', 'Recipient','Type'])
		
		for elt in intDict:
			if len(intDict[elt])>1:
				for exch in intDict[elt]:
					writer.writerow([elt[0], elt[1], exch])
			else:
				writer.writerow([elt[0], elt[1], intDict[elt][0]])


				
def saveToJSON(characters, avgDict, pdist, cdist):
	vecList = []
	women = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves', 'madamedecleves',
	'madamedechartres', 'vidamedechartres','valentinois',
	'poitiers', 'marguerite', 'reine', 'duchessedemercoeur', 
	'martigues', 'dampierre', 'elisabeth','tournon', 'estouteville', 
	'madamedemercoeur']

	test = ['lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 'madamedemercoeur', 'navarre']
	for char in characters:
		vec = {}
		vec['avg-per-page'] = avgDict[char]
		vec['pdist'] = pdist[char]
		vec['cdist'] = cdist[char]
		if char not in test: 
			vec['target'] = int(char in women)
		vecList.append((char,vec))
	print 'length', len(vecList)
	return vecList

def printNice(vecList,filename, start, end):

	f = open(filename, 'w')

	for vec in vecList[start:end]:

		stuff = json.dumps(vec[1]) 
		f.write(json.dumps(vec[0]))
		f.write(str(stuff))
		f.write('\n')


	

	

# characters = ['Dauphine', 'Marie-Stuart', 'd\'Ecosse', 
#  'La cour', 'Duchesse de Valentinois',
# 'Diane de Poitiers', 'Marguerite de France', 'Henri', 'Roi', 'Duc de Nemours', 'Catherine de Medicis', 'La Reine', 
# 'Cardinal de Lorraine', 'Sancerre',  'valet', 'Chatelart', 
# 'Marechal de Saint-Andre', 'Monsieur de Ferrare',  'Prince d\'Orange','Comte de Montgomery',
# 'chirurgien',  'espagnols', 'Gentilhomme', 'ecuyer', 
# 'Madame de Martigues', 'soie', 'Madame de Dampierre', 'Elizabeth', 'Duc de Nevers', 'Monsieur d\'Anville', 
# 'Lignerolles', 'Monsieur le Dauphin', 'Francois II', 'Prince de Conde', 'Madame de Tournon', 'Estouteville', 
#  'Roi de Navarre']

vocabulary = ['dit', 'regardait', 'voyait', 'ajout', 'revele', 'montre', 'vint', 'vu', 'rougit', 'dansait', 'donne', 'donnait', 'vol']

characters = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves',
'monsieurdecleves', 'princedecleves', 'madamedechartres', 'vidamedechartres', 'cour', 'valentinois',
'poitiers', 'marguerite', 'henri', 'roi', 'nemours', 'reine', 
'lorraine', 'sancerre', 'chevalierdeguise', 'valet', 'chatelart', 'duchessedemercoeur',
'marechal', 'ferrare', 'monsieurdeguise', 'd\'orange','montgomery',
 'chirurgiens', 'connetable', 'espagnols', 'gentilhomme', 'ecuyer', 
'martigues', 'soie', 'dampierre', 'elisabeth', 'nevers', 'd\'anville', 
'lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 
'madamedemercoeur', 'navarre']

characters2 = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves', 'madamedecleves',
'monsieurdecleves', 'princedecleves', 'madamedechartres', 'vidamedechartres', 'cour', 'valentinois',
'poitiers', 'marguerite', 'henri', 'roi', 'ducdenemours', 'monsieurdenemours', 'reine', 
'lorraine', 'sancerre', 'chevalierdeguise', 'valet', 'chatelart', 'duchessedemercoeur',
'marechal', 'ferrare', 'monsieurdeguise', 'd\'orange','montgomery',
 'chirurgiens', 'connetable', 'espagnols', 'gentilhomme', 'ecuyer', 
'martigues', 'soie', 'dampierre', 'elisabeth', 'nevers', 'd\'anville', 
'lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 
'madamedemercoeur', 'navarre']


#print textToList('novel.txt')
jt = justText('novel.txt')
a= parseText(textToList('novel.txt'))
# eachPage = eachPageText(jt, a)
# mentionDict= mentionsPerPage(eachPage, characters2)
# pDist = avgDistance(a, characters2)
# cDist = charAvgDistance(a, characters2)

# avgDict= avgMentionsPerPage(mentionDict, characters2)
# j = saveToJSON(characters2, avgDict, pDist, cDist)
# printNice(j, 'training.json', 0, 35)
# printNice(j, 'development.json', 35, 40)
# printNice(j, 'testing.json', 40, 48)

#print a
#charAvgDistance(a, characters)

r=findVocab(a, characters2, vocabulary)
writeInteractions(r, 'output.csv')