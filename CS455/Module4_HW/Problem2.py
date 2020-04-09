from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import SVR, LinearSVR
from sklearn import datasets
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PolynomialFeatures
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score 

from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix


def performSVR(data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target, test_size = 0.20)

    clf = SVR(kernel = 'rbf', epsilon = 0.1, c = 1, max_iter = 10000, gamma = 'scale')

    clf.fit(train_X, train_y)
    pred_y = clf.predict(test_X)
    print(mean_absolute_error(test_y, pred_y))

    plt.figure("a")
    plt.hist(abs(test_y - pred_y), bins = 100)
    plt.xlabel("Error ($k)")

    plot_learning_curves(clf, train_X, train_y)
    plt.show()

def performLinearSVR(data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target, test_size = 0.20)

    clf = Pipeline([
        ("poly_features", PolynomialFeatures(degree = 3, include_bias = False)),
        ("LinearSVR", LinearSVR(epsilon = 0.1, max_iter = 10000))
    ])

    clf.fit(train_X, train_y)
    pred_y = clf.predict(test_X)
    print(mean_absolute_error(test_y, pred_y))

    plt.figure('a')
    plt.hist(abs(test_y - pred_y), bins = 100)
    plt.xlabel("Error ($k)")

    plot_learning_curves(clf, train_X, train_y)
    plt.show()

def plot_learning_curves(model, data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target, test_size = 0.20)

    training_errors, validation_errors = [], []

    for m in range(1, len(train_X)):
        model.fit(train_X[:m], train_y[:m])

        train_pred = model.predict(train_X)
        test_pred = model.predict(test_X)

        training_errors.append(np.sqrt(mean_squared_error(train_y, train_pred)))
        validation_errors.append(np.sqrt(mean_squared_error(test_y, test_pred)))

    plt.figure("Learning Curves")
    plt.plot(training_errors, "r-+", label = "train")
    plt.plot(validation_errors, "b-", label = "test")
    plt.legend()
    #plt.axis([0, 80, 0, 3])

def printDetails(data, columns):
    df = pd.DataFrame(data = data, columns = columns)
    print(df.shape)
    print(df.describe().loc[['min', 'max', 'mean']])
    scatter_matrix(df, alpha = 0.2, figsize = (12,12))
    plt.show()

def loadDataset():
    return datasets.load_diabetes()

def loadData():
    dataset = loadDataset()
    return dataset['data'], dataset['target'], dataset['feature_names']

def main():
    data, target, columns = loadData()
    printDetails(data, columns)
    performLinearSVR(data, target)
    performLinearSVR(data, target)

main()