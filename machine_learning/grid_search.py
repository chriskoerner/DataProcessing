"""
Modified Grid Search
"""
import argparse
from pprint import pprint

from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.datasets.svmlight_format import load_svmlight_file
from sklearn import svm
import sys

parser = argparse.ArgumentParser(description='Program to do some simple gridsearch')
parser.add_argument("libsvm_file", type=str)

args = parser.parse_args()

if args.libsvm_file is None:
    parser.print_help("error")
    sys.exit(-1)

X, y = load_svmlight_file(args.libsvm_file)


# split the dataset in two equal part respecting label proportions
train, test = iter(StratifiedKFold(y, 2, indices=True)).next()


tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = [
    ('precision', precision_score),
    ('recall', recall_score),
    ('f1_score', f1_score)
]

for score_name, score_func in scores:
    clf = GridSearchCV(svm.sparse.SVC(C=1), tuned_parameters, score_func=score_func)

    clf.fit(X[train], y[train], cv=StratifiedKFold(y[train], 5, indices=True))
    y_true, y_pred = y[test], clf.predict(X[test])

    print "Classification report for the best estimator: "
    print clf.best_estimator
    print "Tuned for '%s' with optimal value: %0.3f" % (
        score_name, score_func(y_true, y_pred))
    print classification_report(y_true, y_pred)
    print "Grid scores:"
    pprint(clf.grid_scores_)
    print