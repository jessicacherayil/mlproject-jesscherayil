

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
		montmorency = ['montmorency', 'montmorency,', 'montmorency.']
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
				l[i] == 'duchessedemercoeur'
			elif l[i-2] == 'madame':
				l[i] == 'duchessedemercoeur'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'
		elif word in montmorency:
			if l[i-2] == 'monsieur':
				l[i] == 'monsieurdemontmorency'
			elif l[i-2] == 'connetable':
				l[i] == 'connetabledemontmorency'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'
		elif word in guise:
			if l[i-2] == 'chevalier':
				l[i] == 'chevalierdeguise'
			elif l[i-2] == 'monsieur':
				l[i] == 'monsieurdeguise'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'
		elif word in nemours:
			if l[i-2] == 'monsieur':
				l[i] == 'chevalierdeguise'
			elif l[i-2] == 'monsieur':
				l[i] == 'monsieurdeguise'
			l[i-2] = 'TO-DELETE'
			l[i-1] = 'TO-DELETE'

	new_l = [x for x in l if x != 'TO-DELETE']

	return new_l


characters = ['Dauphine', 'Marie-Stuart', 'd\'Ecosse', 
 'La cour', 'Duchesse de Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Henri', 'Roi', 'Duc de Nemours', 'Catherine de Medicis', 'La Reine', 
'Cardinal de Lorraine', 'Sancerre',  'valet', 'Chatelart', 
'Marechal de Saint-Andre', 'Monsieur de Ferrare',  'Prince d\'Orange','Comte de Montgomery',
'chirurgien',  'espagnols', 'Gentilhomme', 'ecuyer', 
'Madame de Martigues', 'soie', 'Madame de Dampierre', 'Elizabeth', 'Duc de Nevers', 'Monsieur d\'Anville', 
'Lignerolles', 'Monsieur le Dauphin', 'Francois II', 'Prince de Conde', 'Madame de Tournon', 'Estouteville', 
 'Roi de Navarre']



characters = ['Dauphine', 'Marie-Stuart', 'd\'Ecosse', 'Mademoiselle de Chartres', 'Princesse de Cleves',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La cour', 'Duchesse de Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Henri', 'Roi', 'Duc de Nemours', 'Catherine de Medicis', 'La Reine', 
'Cardinal de Lorraine', 'Sancerre', 'Chevalier de Guise', 'valet', 'Chatelart', 'Duchesse de Mercoeur',
'Marechal de Saint-Andre', 'Monsieur de Ferrare', 'Monsieur de Guise', 'Prince d\'Orange','Comte de Montgomery',
'Monsieur de Montmorency', 'chirurgien', 'Connetable de Montmorency', 'espagnols', 'Gentilhomme', 'ecuyer', 
'Madame de Martigues', 'soie', 'Madame de Dampierre', 'Elizabeth', 'Duc de Nevers', 'Monsieur d\'Anville', 
'Lignerolles', 'Monsieur le Dauphin', 'Francois II', 'Prince de Conde', 'Madame de Tournon', 'Estouteville', 
'Madame de Mercoeur', 'Roi de Navarre']

#print textToList('novel.txt')
print parseText(textToList('novel.txt'))