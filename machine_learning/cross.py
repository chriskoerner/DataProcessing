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
     "/Users/chris/Dropbox/Experiment/SVM_Experiments/learn_discipline/data_to_learn_discipline_k=5")

skf = cross_validation.StratifiedKFold(y, 10)



clf = svm.sparse.SVC()




for train_index, test_index in skf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    X_train = preprocessing.normalize(X_train)
    X_test = preprocessing.normalize(X_test)

    cv = clf.fit(X_train, y_train)

    prediction = clf.predict(X_test)


    print "test shape %s" % (y_test.shape)
    print "prediction shape %s" % (prediction.shape)

    print metrics.f1_score(prediction, y_test)
