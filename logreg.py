from __future__ import division  # floating point division
import time  # time utilities
import sys

"""Implement gradient ascent for logistic regression."""

import numpy as np
from jsonparse import load_training, load_testing
from numpy.linalg import norm

import random
def perceptron_train(trainX, trainy, maxiter):
    """Given training data points (trainX) and their labels (trainy -- each either 0 or +1),
    train a hyperplane represented by a weight vector w and bias b
    using the perceptron algorithm, for up to maxiter epochs or until there are no mistakes.

    Return a tuple consisting of
    (1) the weight vector
    (2) the bias
    (3) the training accuracy at the end
    """
    num_traindata, num_dims = trainX.shape
    trainy = np.array(trainy)
    trainy[trainy==0] = -1   # change from 0/1 labeling to -1/1 labeling for perceptron

    w = np.zeros(num_dims)
    b = 0

    convergence_iter = maxiter  # assuming at first that it never converges

    agenda = range(num_traindata)

    for epoch in range(maxiter):
        num_errors = 0
        for i in agenda:
            x = trainX[i, :]
            y = trainy[i]

            if y*np.sign(x.dot(w)+b)<=0:
                # update
                w = w + y*x
                b = b + y

                num_errors += 1

        if num_errors == 0:
            break

    return w, b, 1-num_errors/float(num_traindata)

def sigmoid(x, w, b):
    """P(y=1|x, w, b) with the sigmoid (logistic) function"""
    wx_plus_b = w.dot(x)+b
    # handle overflow
    if wx_plus_b<-500:
        return 0
    else:
        return 1./(1+np.exp(-wx_plus_b))

# PART B: Write your code below
def logreg_train(trainX, trainy, maxiter, eta, alpha, batch_size=1):
    """Given training data points (trainX) and their labels (trainy -- each either 0 or +1),
    train a hyperplane represented by a weight vector w and bias b
    using logistic regression, for maxiter epochs using the eta learning rate
    and alpha L2 regularization weight.

    If eta is a number, use it as a constant learning rate.
    If it is the string 'step', start with a rate of 1, and reduce it by 1/2
    every 5 epochs. (This is called step decay.)

    If batch_size is 1, use stochastic gradient ascent, where the gradient is calculated
    at each training point and w and b updated accordingly.
    Otherwise, split the data into batches given by batch_size, and compute the gradient
    and make the update on each batch (mini-batch gradient ascent).

    Return a tuple consisting of
    (1) the weight vector
    (2) the bias
    (3) the training accuracy at the end
    """
    #TODO: fill in
    num_traindata, num_dims = trainX.shape
    w = np.zeros(num_dims)
    b = 0.

    if eta=='step':
        eta = 1  # and scale by .5 every 5 epochs
        etastep = True
    else:
        etastep = False

    agenda = range(0, num_traindata, batch_size)  # divide into batches

    for epoch in range(maxiter):
        num_errors = 0

        if etastep and epoch%5==4:
            eta *= 0.5

        for start in agenda:  # starting point in batch
            batchy = trainy[start:start+batch_size]
            batchX = trainX[start:start+batch_size, :]

            gradw = np.zeros(num_dims)
            gradb = 0
            for i in range(min(batch_size, batchy.size)): # for leftover minibatch at the end

                x = batchX[i]
                y = batchy[i]

                loss = y - sigmoid(x, w, b)

                if np.abs(loss)>0.5:
                    num_errors += 1  # for training accuracy

                gradw += loss*x
                gradb += loss

            b += eta*gradb
            w += eta*gradw - alpha*w

    return w, b, 1-num_errors/float(num_traindata)

def predict_confidence(w, b, testX):
    """return a vector of probabilities of the class y=1 for each data point x"""
    #TODO: fill in
    predictions = []
    numpoints, _ = testX.shape
    for i in range(numpoints):
        predictions.append(sigmoid(testX[i], w, b))
    return predictions

def get_meansq_accuracy(testy, predictions):
    """return mean square accuracy of predictions"""
    #TODO: fill in
    return 1-(norm(predictions-testy, 2)**2)/float(len(testy))

# PART B: Write your code above

def get_accuracy(testy, predictions):
    """return proportion of correct predictions"""
    # convert probabilities to 0 or 1 predictions first
    predictions = np.array(predictions)
    predictions = (predictions>0.5).astype(int)  # 1 if over 50%, 0 if not
    return 1-norm(predictions-testy, 0)/float(len(testy))

def show_significant_features(w, featurelist):
    wsorted = np.argsort(w)
    print 'Features predicting bill survived:', ', '.join(map(lambda i: featurelist[i], wsorted[:30]))
    print 'Features predicting bill died:', ', '.join(map(lambda i: featurelist[i], wsorted[-30:][::-1]))

def logreg_gridsearch(trainX, trainy, devX, devy, maxiter_values, eta_values, alpha_values, batch_size_values):
    hyperparamdict = {}
    for batch_size in batch_size_values:
        for maxiter in maxiter_values:
            for eta in eta_values:
                for alpha in alpha_values:
                    w, b, train_accuracy = logreg_train(trainX, trainy, maxiter=maxiter, eta=eta, alpha=alpha, batch_size=batch_size)
                    print 'maxiter=', maxiter, 'eta=', eta, 'alpha=', alpha, 'batch_size=', batch_size, 'training accuracy=', train_accuracy
                    predictions = predict_confidence(w, b, devX)
                    hyperparamdict[(maxiter, eta, alpha, batch_size)] = {}
                    hyperparamdict[(maxiter, eta, alpha, batch_size)]['dev accuracy'] = get_meansq_accuracy(devy, predictions)
                    hyperparamdict[(maxiter, eta, alpha, batch_size)]['hyperplane'] = w, b
    return hyperparamdict

def perceptron_gridsearch(trainX, trainy, devX, devy, maxiter_values):
    hyperparamdict = {}
    for maxiter in maxiter_values:
        w, b, train_accuracy = perceptron_train(trainX, trainy, maxiter=maxiter)
        print 'maxiter=', maxiter, 'training accuracy=', train_accuracy
        predictions = predict_confidence(w, b, devX)
        hyperparamdict[(maxiter, )] = {}
        hyperparamdict[(maxiter, )]['dev accuracy'] = get_meansq_accuracy(devy, predictions)
        hyperparamdict[(maxiter, )]['hyperplane'] = w, b
    return hyperparamdict

def main(plr):
    trainX, trainy, featuremap = load_training('training.json')
    devX, devy = load_testing('development.json', featuremap)
    testX, testy = load_testing('testing.json', featuremap)
    featurelist = map(lambda x:x[0], sorted(featuremap.items(), key=lambda x:x[1])) # from index to feature
    print 'Loaded data'

    if plr=='l':
        print 'LOGISTIC REGRESSION'
        lr_hyperparamdict = logreg_gridsearch(trainX, trainy, devX, devy,
                                       maxiter_values=[5, 25, 125], # number of epochs
                                       eta_values=[0.1, 0.01, 'step'], # learning rate
                                       alpha_values=[0, 1e-5], # regularization weight
                                       batch_size_values=[200, 1]  # batch size for mini-batch gradient ascent:
                                      )

        print 'Hyperparameter search results:'
        for params in lr_hyperparamdict:
            print params, lr_hyperparamdict[params]['dev accuracy']

        best_hyperparams = max(lr_hyperparamdict.items(), key=lambda x:x[1]['dev accuracy'])[0]

        print 'Testing with hyperplane that produced best mean squared acc on dev:', best_hyperparams
        lr_w, lr_b = lr_hyperparamdict[best_hyperparams]['hyperplane']
        lr_predictions = predict_confidence(lr_w, lr_b, testX)
        print 'PREDICTIONS: ', lr_predictions
        print 'test data', testx, testy
        print 'All-or-nothing accuracy:', get_accuracy(testy, lr_predictions)
        print 'Mean-squared accuracy:', get_meansq_accuracy(testy, lr_predictions)

        show_significant_features(lr_w, featurelist)

    elif plr=='p':
        print 'PERCEPTRON'
        p_hyperparamdict = perceptron_gridsearch(trainX, trainy, devX, devy,
                                       maxiter_values=[5**p for p in range(1, 4)]) # number of epochs

        print 'Hyperparameter search results:'
        for params in p_hyperparamdict:
            print params, p_hyperparamdict[params]['dev accuracy']

        best_hyperparams = max(p_hyperparamdict.items(), key=lambda x:x[1]['dev accuracy'])[0]

        print 'Testing with hyperplane that produced best mean squared acc on dev:', best_hyperparams
        p_w, p_b = p_hyperparamdict[best_hyperparams]['hyperplane']
        p_predictions = predict_confidence(p_w, p_b, testX)
        print 'All-or-nothing accuracy:', get_accuracy(testy, p_predictions)
        print 'Mean-squared accuracy:', get_meansq_accuracy(testy, p_predictions)

        show_significant_features(p_w, featurelist)


if __name__=='__main__':
    """Run the main function"""
    if len(sys.argv)!=2:
        print 'Usage:', sys.argv[0], '{p,l}'
    else:
        main(sys.argv[1])
