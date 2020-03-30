from sklearn import datasets as datasets
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score
from sklearn import metrics

from sklearn.linear_model import LogisticRegression

import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

# CS 455 - Artificial Intelligence
# Homework 3 - KNN and Regression Models
# Contributers - Cameron Stark & Dustin Cribbs

def buildAndPrintKNN(df, target):
    clf = KNeighborsClassifier(n_neighbors=10)
    s = StandardScaler()
    df = s.fit_transform(df)


    target_pred = cross_val_predict(clf, df, target, cv = 5)

    print("\nKNeighbors")
    print("Confusion Matrix:")
    print(confusion_matrix(target, target_pred))
    print("Accuracy: " + str(accuracy_score(target, target_pred)))
    print("Precision: " + str(precision_score(target, target_pred, average='micro')))
    print("Recall: " + str(recall_score(target, target_pred, average='micro')))
    print("F1: " + str(f1_score(target, target_pred, average='macro')))

    # target_dummies = pd.get_dummies(target, drop_first=False).values

    # figure, axis = plt.subplots(figsize=(10, 10))

    # axis.plot([0,1], [0,1], 'k--')
    # axis.set_xlim([0.0, 1.0])
    # axis.set_ylim([0.0, 1.05])
    # axis.set_xlabel('False Positive Rate')
    # axis.set_ylabel('True Positive rate')
    # axis.set_title('ROC')
    # fpr = []
    # tpr = []
    # for i in range(1, 4):
    #     fpr[i], tpr[i], _ = metrics.roc_curve(target_dummies[:, i - 1], target_pred[:, i - 1]) 
    #     axis.plot(fpr[i], tpr[i], label='ROC For Class')

    # axis.legend(loc="best")
    # axis.grid(alpha=.4)
    # plt.show()


def buildAndPrintLogRegression(df, target):
    s = StandardScaler()
    df = s.fit_transform(df)
    clf = LogisticRegression().fit(df, target)
    

    target_pred = cross_val_predict(clf, df, target, cv = 5)
    print("\nLogistic Regression")
    print("Confusion Matrix:")
    print(confusion_matrix(target, target_pred))
    print("Accuracy: " + str(accuracy_score(target, target_pred)))
    print("Precision: " + str(precision_score(target, target_pred, average='micro')))
    print("Recall: " + str(recall_score(target, target_pred, average='micro')))
    print("F1: " + str(f1_score(target, target_pred, average='micro')))

def plotData(data):
    scatter_matrix(data, alpha = 0.2, figsize=(12, 12))
    plt.show()

def printDataDetails(data):
    #print(data)
    print(data.shape)
    print(data.describe().loc[['max', 'min', 'mean']])

def getWineData():
    return datasets.load_wine()

def loadTargetDataset():
    wineData = getWineData()
    target_data = wineData['target']
    #target_columns = wineData['target_names']
    # df = pd.DataFrame(data = target_data)
    
    return target_data

def loadDataset():
    wineData = getWineData()
    data = wineData['data']
    headers = wineData['feature_names']
    df = pd.DataFrame(data = data, columns = headers)

    return df

def main():
    df = loadDataset()
    target = loadTargetDataset()
    printDataDetails(df)
    #plotData(df)
    buildAndPrintKNN(df, target)
    buildAndPrintLogRegression(df, target)

main()