# -*- coding: utf-8 -*-
import plotly.plotly as py
import plotly.graph_objs as go
from mentions import *
import random
import argparse


def makeTrace(character, xLabels,chunk):
    
    yVals = getNumMentionsInRange(character,chunk)
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
    

def makePlot(character1, character2, character3, chunk):
    
    characters = [character1,character2,character3]
    
    xLabels = [i for i in range(75,254,chunk)]
    
    traces = []
    for character in characters:
        traces.append(makeTrace(character,xLabels,chunk))
        
    data = traces
    layout = go.Layout(
        title='Mentions of ' + character1 + ', ' + character2 + ', and ' + character3,
    )
    
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='mentions')
    
    

characters = ['Princesse','Madame de Cleves','Dauphine',
'Prince de Cleves', 'Madame de Chartres', 'Vidame de Chartres', 'La Cour', 'Valentinois',
'Marguerite de France', 'Roi', 'Henri Second', 'Nemours', 'Catherine de Médicis',
'Chevalier de Guise', 'Cardinal de Lorraine', 'Sancerre', 'Premier Valet De Chambre', 'Chatelart', 
'Comte de Montgomery', 'Monsieur de Montmorency', 'Chirurgien', 'Connetable de Montmorency', 'Monsieur de Guise',
'de Ferrare', 'Espagnols', 'Gentilhomme', 'ecuyer',
'homme du magasin de soie']

def main():
    parser = argparse.ArgumentParser(description='Create bar graph of mentions')
    parser.add_argument('char1', type=str, help='character 1')
    parser.add_argument('char2', type=str, help='character 2')
    parser.add_argument('char3', type=str, help='character 3')
    parser.add_argument('chunk', type=int, help='ranges of page numbers')
    args = parser.parse_args()   
    makePlot(args.char1,args.char2,args.char3,args.chunk)
    
    
if __name__=='__main__':
    main()

#text=['27% market share', '24% market share', '19% market share'], #labels for the bars
