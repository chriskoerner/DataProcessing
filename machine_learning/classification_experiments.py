"""
a simple classification script

needs libsvm files as input
"""
import argparse
import os

from sklearn.datasets import load_svmlight_file
from sklearn import preprocessing
from sklearn import svm, metrics
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix

import pylab as plt
import sys

def drange(start, stop, step):
    """
    range for floats
    """
    r = start
    while r < stop:
            yield r
            r += step

parser = argparse.ArgumentParser(description='Program to do some simple SVM experiments')
parser.add_argument("libsvm_file", type=str)

args = parser.parse_args()

print args

if args.libsvm_file is None:
    parser.print_help()

    sys.exit(-1)

print args.libsvm_file

X, y = load_svmlight_file(args.libsvm_file)






for x in drange(0.1, 1.0, 0.1):
    precisions = []
    recalls = []
    f1scores = []

    clf = svm.sparse.SVC(C = x, kernel = 'linear')

    skf = cross_validation.StratifiedKFold(y, 10, indices=True)

    fold = 0
    
    for train_index, test_index in skf:
        fold += 1
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        X_train = preprocessing.normalize(X_train)
        X_test = preprocessing.normalize(X_test)

        cv = clf.fit(X_train, y_train)

        prediction = clf.predict(X_test)

        cm = confusion_matrix(prediction, y_test)

        plt.matshow(cm)
        plt.title('Confusion matrix')
        plt.colorbar()

        if not os.path.isdir("out"):
            os.mkdir("out")

        plt.savefig("out/confusion_matrix_" + str(fold) + "_C_" + str(x) + ".pdf")

        f1scores.append(metrics.f1_score(prediction, y_test))
        precisions.append(metrics.precision_score(prediction, y_test))
        recalls.append(metrics.recall_score(prediction, y_test))

    print "-------------------------"
    print "C paramenter: %s" % x
    print "avg f1 score: %s" % (sum(f1scores)/ len(f1scores))
    print "avg precision score: %s" % (sum(precisions)/ len(f1scores))
    print "avg recall score: %s" % (sum(recalls)/ len(f1scores))
    print "-------------------------"