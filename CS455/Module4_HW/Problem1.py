from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV 
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score 

from matplotlib import pyplot as plt

import numpy as np 
import pandas as pd

# CS 455 - Artificial Intelligence
# Homework 4 - Support Vector Machines
# Contributers - Cameron Stark & Dustin Cribbs
# Sources - Github and other online resources

def performSVC(data, target):
    clf = SVC(kernel = 'linear', C = 10)
    s = StandardScaler()
    data_x = s.fit_transform(data)

    y_pred = cross_val_predict(clf, data_x, target, cv = 5)

    print("\nSVC")
    print("Confusion Matrix: ")
    print(confusion_matrix(target, y_pred))
    print("Accuracy Score = " + str(accuracy_score(target, y_pred))) 
    print("Precision Score = " + str(precision_score(target, y_pred, average = 'micro')))
    print("Recall Score = " + str(recall_score(target, y_pred, average = 'micro')))
    print("F1 Score = " + str(f1_score(target, y_pred, average = 'micro'))) 

def performLinearSVC(data, target):
    clf = LinearSVC(C = 10, loss = "hinge")
    s = StandardScaler()
    data_x = s.fit_transform(data)

    y_pred = cross_val_predict(clf, data_x, target, cv = 5)

    print("LinearSVC")
    print("Confusion Matrix:")
    print(confusion_matrix(target, y_pred))
    print("Accuracy Score = " + str(accuracy_score(target, y_pred)))
    print("Precision Score = " + str(precision_score(target, y_pred, average = 'micro')))
    print("Recall Score = " + str(recall_score(target, y_pred, average = 'micro')))
    print("F1 Score = " + str(f1_score(target, y_pred, average = 'micro'))) 

def loadDataset():
    return datasets.load_wine()

def loadData():
    dataset = loadDataset()
    return dataset['data'], dataset['target']

def main():
    data, target = loadData()
    performLinearSVC(data, target)
    performSVC(data, target)

main()