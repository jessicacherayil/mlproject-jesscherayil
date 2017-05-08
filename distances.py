

'''Author: Jess Cherayil'''

import re
import codecs
import os
import unicodedata
import csv
import numpy as np

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
			elif l[i-2] == 'prince':
				l[i] = 'monsieurdecleves'
			elif l[i-2] == 'princesse':
				l[i] = 'princessedecleves'
			elif l[i-2] == 'madame':
				l[i] = 'princessedecleves'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'


		elif word in chartres:
			if l[i-2] == 'mademoiselle':
				l[i] = 'princessedecleves'
			elif l[i-2] == 'madame':
				l[i] = 'madamedechartres'
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
			elif l[i-2] == 'monsieur':
				l[i] = 'ducdenemours'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'

	new_l = [x for x in l if x != 'TO-DELETE']

	return new_l

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
		
		print 'CHAR IS', char
		#print 'ELT LENGTH', len(charDists[char])
		avg = 0
		denom = 1
		for elt in charDists[char]: #for every mention of the king
			
			next = []

			for char2 in charDists: #iterate through all other characters

				if char != char2: 

					for elt2 in charDists[char2]: #for each of their mentions

						#next_keys = [x[0] for x in next]
						
						if elt2 > elt: #see if mentioned after, append distance
							next.append((char2,elt2-elt)) 
							#print len(next)

							break

			if len(next) > 0: 
				so = sorted(next, key =lambda x:x[1])
				#print len(next)
				mentionAvg.append(so[0][1])
				#print 'INTERMEDIATE', len(mentionAvg)
			

			

		print 'MENTIONAVG LEN', len(mentionAvg)
		avgs[char] = float(sum(mentionAvg))/len(mentionAvg)

							
					
	return avgs




# characters = ['Dauphine', 'Marie-Stuart', 'd\'Ecosse', 
#  'La cour', 'Duchesse de Valentinois',
# 'Diane de Poitiers', 'Marguerite de France', 'Henri', 'Roi', 'Duc de Nemours', 'Catherine de Medicis', 'La Reine', 
# 'Cardinal de Lorraine', 'Sancerre',  'valet', 'Chatelart', 
# 'Marechal de Saint-Andre', 'Monsieur de Ferrare',  'Prince d\'Orange','Comte de Montgomery',
# 'chirurgien',  'espagnols', 'Gentilhomme', 'ecuyer', 
# 'Madame de Martigues', 'soie', 'Madame de Dampierre', 'Elizabeth', 'Duc de Nevers', 'Monsieur d\'Anville', 
# 'Lignerolles', 'Monsieur le Dauphin', 'Francois II', 'Prince de Conde', 'Madame de Tournon', 'Estouteville', 
#  'Roi de Navarre']



characters = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves',
'monsieurdecleves', 'princedecleves', 'madamedechartres', 'vidamedechartres', 'cour', 'valentinois',
'poitiers', 'marguerite', 'henri', 'roi', 'nemours', 'reine', 
'lorraine', 'sancerre', 'chevalierdeguise', 'valet', 'chatelart', 'duchessedemercoeur',
'marechal', 'ferrare', 'monsieurdeguise', 'd\'orange','montgomery',
 'chirurgiens', 'connetable', 'espagnols', 'gentilhomme', 'ecuyer', 
'martigues', 'soie', 'dampierre', 'elisabeth', 'nevers', 'd\'anville', 
'lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 
'madamedemercoeur', 'navarre']

#print textToList('novel.txt')
a= parseText(textToList('novel.txt'))
#print a
print charAvgDistance(a, characters)