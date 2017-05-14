#Gender Prediction in La Princesse de Clèves

Data: Since the dataset is small, I've pushed training.json, development.json, and testing.json to this repository. You can also see the original text by opening novel.txt. 

Main Files Used:
- distances.py was used to parse the text and extract features
- jsonparse.py and logreg.py were used to run a logistic regression model on this data

Output Files: 
- output.csv is a spreadsheet of interactions captured by my program. The first column is the
initiator of the interaction, the second column is the recipient of the interaction, and the 
third column is a word describing the type of interaction that occurred. 
- mentions.csv is a spreadsheet mapping characters to the number of times they were mentioned
on each page in the novel. 