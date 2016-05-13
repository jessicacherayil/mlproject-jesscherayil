# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins
from mentions import *

# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""

import numpy as np
import matplotlib.pyplot as plt

def getNumMentions(character):

    pageDict = eachPageText('novel.txt')
    d = characterFreq(pageDict, characters)
    mentions = [] #list of lists. Inner list contains page, charFrequency
    
    for i in range(75,254):
        if i in d:
            if character in d[i]:
                mentions.append((str(i),d[i][character]))
            else:
                mentions.append((str(i),0))
        else: #blank pages 
            mentions.append((str(i),0))
    return mentions
    
def plot(character, mentionList):
    n_groups = len(mentionList)
    
    plt.figure(figsize = (17,7))
    fig, ax = plt.subplots()
    
    ax.set_title('Mentions of ' + str(character) + ' in Princesse de Cleves', size=20)
    
    
    index = np.arange(n_groups)
    bar_width = 0.5
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    number = []
    ranges = []
    for item in mentionList:
        number.append(item[1])
        ranges.append(item[0])
    

    char1 = plt.bar(index, number, bar_width,
                    alpha=opacity,
                    color='b',
                    error_kw=error_config)
    
    plt.xlabel('Page number')
    plt.ylabel('Number of Mentions')
    xlabels = [ranges[i] for i in range(0,179)] #labels of page numbers
    plt.xticks(index + bar_width, xlabels)
    plt.legend()
    plt.tight_layout()
    mpld3.show()

princesse = getNumMentions('Roi')
plot('Roi', princesse)


#toggle character visualizations --> if HTML, template 
#normalize counts, cross entropy between characters