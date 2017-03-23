
A description of your problem and motivations.
La Princesse de Clèves is a novel often considered an early feminist work because of the way the female characters hold their ground in a patriarchal society. But are men and women really equally represented in the royal court? Is there a power imbalance that a computer may be able to detect? With this project, I intend to predict the gender of characters based on how they interact with others in the court. If men and women interact somewhat equally, it should be difficult for my program to detect the gender of an unknown character.  

A brief survey of existing work, with links to the relevant papers or websites
Character Interaction Extraction -- These researchers build a weighted graph based on character interactions within several plays and scripts for movies. They then used logistic regression to classify the novels in several ways (e.g. romance or not, play or movie, released before 2000 or not, etc.). They evaluated their results using AUC (area under curve)

The dataset(s) you will be using, with a link if relevant

Princesse de Clèves text (.txt file)

A description of the featurization and classification algorithms that you envision using. While you will most likely use some form of supervised classification, you may also like to apply some unsupervised methods like clustering and dimensionality reduction as an aid to featurization or data exploration.

I will be using logistic regression to learn a hyperplane between male and female characters. This way, if a test character lies on one side of the hyperplane, I can see with what confidence level they are positioned. 

How you will evaluate your results (accuracy, mean squared error, precision/recall,...)

I will compute accuracy twice for each part of my program (the first part is where I attempt to recognize all interactions in the novel, the second part is where I predict gender). For the first part, I have a spreadsheet of “true labels” -- that is, all the interactions between characters in the novel, provided by Professor Bilis. I intend to compare this spreadsheet with my eventual spreadsheet. Then I can compute the number of interactions captured by my program / the total number of actual interactions. Second, since my test set for prediction will be relatively small, I can create the true labels for each character. Then I can just compute accuracy based on how many characters’ genders my model predicted correctly.

Is the primary purpose of your task prediction, or do you also want to explain something about the data (i.e., analyzing features that are predictive of a class, the way you did in PS2 and perhaps in PS3)?

The primary purpose of my task is prediction, but the results from this will also demonstrate whether interaction is a good predictor of gender. 

Responsibilities of each team member. These may evolve over the course of your project, but it helps to have a plan.
Jess --- do everything. 


Three goals. Be realistic about them, but also ambitious.
What to complete by April 20th when the project update is due. The second milestone on April 06th is writing code to parse your data, so don't include data loading as a goal.
The minimum desired outcome of your project by the final submission on May 15th
The ideal final outcome of your project

April 20: By this point, I hope to be able to generate a graph of interactions in La Princesse de Clèves, and have captured at least 50% of the total interactions. 
May 15: My minimum desired outcome is a graph of interactions and a logistic regression model that predicts gender.
The ideal final outcome would be some sort of visualization for both the graph and the logistic regression model -- this would be a more useful way of showing the data to other people.  

