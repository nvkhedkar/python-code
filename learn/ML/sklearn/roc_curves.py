# example of a roc curve for a predictive model
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from matplotlib import pyplot
import numpy as np
import sys
from sklearn import datasets, svm, metrics


def get_digits_data():
    digits = datasets.load_digits()

    # flatten the images
    n_samples = len(digits.images)
    X_loc = digits.images.reshape((n_samples, -1))
    y_all = digits.target
    print(type(y_all), y_all.shape, np.unique(y_all))
    return X_loc, y_all


def get_data_random():
    # generate 2 class dataset
    X_loc, y_loc = make_classification(n_samples=1000, n_classes=2, random_state=1)
    return X_loc, y_loc


X, y = get_data_random()
# split into train/test sets
trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)
# fit a model
model = LogisticRegression(solver='lbfgs')
model.fit(trainX, trainy)

y_pred = model.predict(testX)
print(f"accuracy: {metrics.accuracy_score(testy, y_pred)}")
print(f"f1 score: {metrics.f1_score(testy, y_pred)}")
print(metrics.classification_report(testy, y_pred, digits=4)) # target_names=target_names
# predict probabilities
yhat = model.predict_proba(testX)
# retrieve just the probabilities for the positive class
pos_probs = yhat[:, 1]
# plot no skill roc curve
pyplot.plot([0, 1], [0, 1], linestyle='--', label='No Skill')
# calculate roc curve for model
fpr, tpr, threshold = roc_curve(testy, pos_probs)
lt = list(threshold)
print(f"threshold: ")
[print(f"{x:.8f}") for x in lt]

# print(f"FPR: {fpr}")
# print(f"tPR: {tpr}")
# plot model roc curve
pyplot.plot(fpr, tpr, marker='.', label='Logistic')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()
