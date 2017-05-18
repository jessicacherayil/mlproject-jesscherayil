# -*- coding: utf-8 -*-
'''Author: Jess Cherayil'''

# -*- coding: utf-8 -*-
import plotly.plotly as py
import plotly.graph_objs as go
from mentions import *
import random
import argparse
from distances import *

#avgDict - avg number of mentions per page -- XAXIS: character,  YAXIS: number of mentions 
#pDist - avg distance from the princesse
#cDist - avg distance from any other character
#dialogue - proportion of dialogue to other things
#pRaw -- number of interactions with the princess
#royalty -- number of interactions with reine, roi

def makeTrace(character, xLabels, avgDict):
	
	yVals = avgDict[character]
	randColor = 'rgb(' + str(random.randint(0,256)) + str(random.randint(0,256)) + str(random.randint(0,256)) + ')'
	
	trace0 = go.Bar(
		x=xLabels, #labels for x-axis
		y=yVals, #y-values for each x-value 
		name = character,
		marker=dict(
			color=randColor,
			line=dict(
				color=randColor,
				width=1.5,
			)
		),
		opacity=0.6
	)
	
	return trace0

def makePlot(characters,avgDict):
	xLabels = characters
	 
	traces = []
	for character in characters:
		traces.append(makeTrace(character,xLabels,avgDict))
	 
	 
	data = traces

	layout = go.Layout(
		title='Average Number of Mentions Per Page',
		xaxis = dict(
			title = 'Character'
			),
		yaxis=dict(
			title = 'Average Number of Mentions'
			),
	)
	 
	 
	fig = go.Figure(data=data, layout=layout)
	if len(characters)<10:
		plot_url = py.plot(fig, filename='avg_mentions')
	else:
		plot_url = py.plot(fig, filename ='avg_mentions')
	



def main():
	characters2 = ['dauphine', 'd\'ecosse', 'mademoiselledechartres', 'princessedecleves', 'madamedecleves',
	'monsieurdecleves', 'princedecleves', 'madamedechartres', 'vidamedechartres', 'cour', 'valentinois',
	'poitiers', 'marguerite', 'henri', 'roi', 'ducdenemours', 'monsieurdenemours', 'reine', 
	'lorraine', 'sancerre', 'chevalierdeguise', 'valet', 'chatelart', 'duchessedemercoeur',
	'marechal', 'ferrare', 'monsieurdeguise', 'd\'orange','montgomery',
	 'chirurgiens', 'connetable', 'espagnols', 'gentilhomme', 'ecuyer', 
	'martigues', 'soie', 'dampierre', 'elisabeth', 'nevers', 'd\'anville', 
	'lignerolles', 'dauphin', 'francois', 'conde', 'tournon', 'estouteville', 
	'madamedemercoeur', 'navarre']
	#parser = argparse.ArgumentParser(description='Create bar graph of mentions')
	#parser.add_argument('chunk', type=int, help='ranges of page numbers')
	#args = parser.parse_args()   
	#makePlot(commonChars, args.chunk)
	jt = justText('novel.txt')
	a= parseText(textToList('novel.txt'))
	
	eachPage = eachPageText(jt, a)
	mentionDict= mentionsPerPage(eachPage, characters2)
	avgDict= avgMentionsPerPage(mentionDict, characters2)
	makePlot(characters2, avgDict)
	
	
if __name__=='__main__':
	main()