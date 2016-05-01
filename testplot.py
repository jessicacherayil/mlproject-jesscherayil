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

pageDict = eachPageText('novel.txt')
d = characterFreq(pageDict, characters)
mentions = []
for i in range(75,254):
    if i in d:
        if 'Princesse' in d[i]:
            mentions.append(d[i]['Princesse'])
        else:
            mentions.append(0)
    else:
        mentions.append(0)
            
print 'mention len', len(mentions)
princesse_mentions = []
for i in range (75, 254):
    princesse_mentions.append([str(i),mentions[i-75]])
    print i
    print mentions[i-75]

        
#princesse_mentions = [print [str(i), mentions[i]] for i in range(75, 253) if i in d]
n_groups = len(princesse_mentions)

fig, ax = plt.subplots()
#plt.figure(figsize = (10,10))
ax.set_title('Character Mentions in Princesse de Cleves', size=20)

index = np.arange(n_groups)
bar_width = 0.5

opacity = 0.4
error_config = {'ecolor': '0.3'}

number = []
ranges = []
for item in princesse_mentions:
    number.append(item[1])
    ranges.append(item[0])

rects1 = plt.bar(index, number, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config)

plt.xlabel('Page number')
plt.ylabel('Number of Mentions')
plt.xticks(index + bar_width, (ranges[0],ranges[1],ranges[2],ranges[3]))
plt.legend()

mpld3.show()
#
#fig, ax = plt.subplots()
#ax.grid(True, alpha=0.3)
#
#N = 50
#df = pd.DataFrame(index=range(N))
#df['x'] = np.random.randn(N)
#df['y'] = np.random.randn(N)
#df['z'] = np.random.randn(N)
#
#labels = []
#for i in range(N):
#    label = df.ix[[i], :].T
#    label.columns = ['Row {0}'.format(i)]
#    # .to_html() is unicode; so make leading 'u' go away with str()
#    labels.append(str(label.to_html()))
#
#points = ax.plot(df.x, df.y, 'o', color='b',
#                 mec='k', ms=15, mew=1, alpha=.6)
#
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_title('Character Mentions in Princesse de Cleves', size=20)
#
#tooltip = plugins.PointHTMLTooltip(points[0], labels,
#                                   voffset=10, hoffset=10, css=css)
#plugins.connect(fig, tooltip)
#
#mpld3.show()