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

def makeTrace(character, xLabels, d):
	if character in d:
		yVals = d[character]
	else:
		yVals = 0.0
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

def makePlot(characters,feat):

##########################################
	jt = justText('novel.txt')
	a= parseText(textToList('novel.txt'))
	
	eachPage = eachPageText(jt, a)
	mentionDict= mentionsPerPage(eachPage, characters2)

	if feat == 'avg_mentions':
		d= avgMentionsPerPage(mentionDict, characters2)
		bigTitle = 'Average Number of Mentions Per Page'

	elif feat == 'distance_from_princesse':
		d = avgDistance(a, characters)
		bigTitle = 'Average Distance (in words) from Princesse'

	elif feat == 'distance_from_char':
		d = charAvgDistance(a, characters)
		bigTitle = 'Average Distance (in words) from Any Character'

	elif feat == 'dialogue':
		d = dialogue('output.csv')
		bigTitle = 'Proportion of Dialogue Interactions'

	elif feat == 'pRaw':
		d =princesseInt('output.csv')
		bigTitle = 'Proportion of Interactions with Princesse'

	elif feat == 'royalty':
		d = royaltyInt('output.csv')
		bigTitle = 'Proportion of Interactions with Royalty'

#######################################

	xLabels = characters
	 
	traces = []
	for character in characters:
		traces.append(makeTrace(character,xLabels,d))	 
	data = traces

#####################################################################	
	layout = go.Layout(
		title=bigTitle,
		xaxis = dict(
			title = 'Character'
			),
		yaxis=dict(
			title = bigTitle
			),
	)
	 
	 
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename =feat)
	



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
	parser = argparse.ArgumentParser()
	parser.add_argument('feature', type=str, help='which feature to graph')
	args = parser.parse_args()   
	

	makePlot(characters2, args.feature)
	
	
if __name__=='__main__':
	main()