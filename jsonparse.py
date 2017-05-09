"""Load data files in the provided JSON format
into X and y arrays."""

import json
import numpy as np

# PART A

def load_training(filename):
    """given a file where each line is a data-point represented as a JSON
    dictionary, with one of the keys ('target') being the class label
    and the rest being the features, return a representation of the dataset
    as a tuple consisting of
    (1) an array X where each row is a data-point and each column a feature
    (excluding the target). A feature not specified for a point has the value 0 for that point.
    Ignore the "id" feature which simply names the data-point.
    (2) an array y where each entry is the value of the target
    class label,
    (3) a dictionary mapping feature names to the indices you selected for them.
    For example, a file containing these two lines
    {'spots': 4, 'weight': 300, 'calves': 1, 'id': 'Marge', 'target': 1}
    {'spots', 2, 'id': 'Nandi', 'weight': 350, 'target': -1}
    should be parsed into the tuple (X, y, featuremap)
    where X = np.array([[4, 300, 1], [2, 350, 0]]), y = [1, -1],
    featuremap = {'spots': 0, 'weight': 1, 'calves': 2}
    The correspondences between feature names ('spots', etc.) and indices (0, 1,...) can be arbitrary,
    but must be consistent, obviously, across all the data-points and the featuremap.
    """
    # TODO: fill in
    # Hint: don't use json.load() on the file directly. Read the lines of the files and
    # use json.loads()
    # Keep in mind that dictionaries are unordered.

    lines = [json.loads(line) for line in open(filename).readlines()]
    # map feature names to indices
    featuremap = {}
    curidx = 0
    for line in lines:
        for feat in line:
            if feat != 'target' and feat!='id':
                if feat not in featuremap:
                    featuremap[feat] = curidx
                    curidx += 1
    # construct data
    X = np.zeros((len(lines), curidx))
    y = np.zeros(len(lines))
    for li, line in enumerate(lines):
        for feat, featval in line.items():
            if feat == 'target':
                y[li] = featval
            elif feat!='id':
                X[li, featuremap[feat]] = featval
    return X, y, featuremap

def load_testing(filename, featuremap):
    """given a file where each line is a data-point represented as a JSON
    dictionary, with one of the keys ('target') being the class label
    and the rest being the features, as well as an ordered list of features,
    return a representation of the dataset as a tuple consisting of
    (1) an array X where each row is a data-point and each column a feature
    (excluding the target). A feature not specified for a point has the value 0 for that point.
    (2) an array y where each entry is the value of the target
    class label.
    The features should match the feature-index correspondences in featuremap.
    Any features not seen in featuremap are ignored
    """
    lines = [json.loads(line) for line in open(filename).readlines()]
    X = np.zeros((len(lines), max(featuremap.values())+1))
    y = np.zeros(len(lines))
    for li, line in enumerate(lines):
        for feat, featval in line.items():
            if feat == 'target':
                y[li] = featval
            elif feat in featuremap:
                X[li, featuremap[feat]] = featval
            # else, feature doesn't exist, so ignore
    return X, y
