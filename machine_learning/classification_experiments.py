from sklearn.datasets import load_svmlight_file
from sklearn import preprocessing
from sklearn import svm, metrics
from sklearn import cross_validation

#import numpy

################################################################################
# Data IO and generation

# import some data to play with

#X, y = load_svmlight_file("/Users/chris/Dropbox/Experiment/SVM_Experiments/learn_discipline/data_to_learn_discipline_k=5")

X, y = load_svmlight_file(
     "/Users/chris/Dropbox/Experiment/SVM_Experiments/learn_academic_status/specialist_svm")

skf = cross_validation.StratifiedKFold(y, 10, indices=True)



clf = svm.sparse.SVC(kernel = 'linear')


precisions = []
recalls = []
f1scores = []

for train_index, test_index in skf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    X_train = preprocessing.normalize(X_train)
    X_test = preprocessing.normalize(X_test)

    cv = clf.fit(X_train, y_train)

    prediction = clf.predict(X_test)

    f1scores.append(metrics.f1_score(prediction, y_test))
    precisions.append(metrics.precision_score(prediction, y_test))
    recalls.append(metrics.recall_score(prediction, y_test))

print "avg f1 score: %s" % (sum(f1scores)/ len(f1scores))
print "avg precision score: %s" % (sum(precisions)/ len(f1scores))
print "avg recall score: %s" % (sum(recalls)/ len(f1scores))
