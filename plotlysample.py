# -*- coding: utf-8 -*-
import plotly.plotly as py
import plotly.graph_objs as go
from mentions import *
import random

def getNumMentions(character):

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


def makeTrace(character, xLabels):
    
    yVals = getNumMentions(character)
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
    
    
    
def makePlot(characters):
    xLabels = [i for i in range(75,254)]
    
    traces = []
    for character in characters:
        traces.append(makeTrace(character,xLabels))
    
    
    data = traces
    layout = go.Layout(
        title='Character Mentions in La Princesse de Clèves',
    )
    
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='mentions')
    
    
characters = ['Madame de Cleves','Dauphine', 'Reine d\'Ecosse', 'Mademoiselle de Chartres', 'Princesse',
'Monsieur de Cleves', 'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La Cour', 'Valentinois',
'Diane de Poitiers', 'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'la Reine',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'Premier Valet De Chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'homme du magasin de soie']


makePlot(characters)

#text=['27% market share', '24% market share', '19% market share'], #labels for the bars
