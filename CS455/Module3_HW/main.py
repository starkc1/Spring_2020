from sklearn import datasets as datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

# CS 455 - Artificial Intelligence
# Homework 3 - KNN and Regression Models
# Contributers - Cameron Stark & Dustin Cribbs








def buildAndPrintKNN(df_train, target_train):
    fields = ["Accuracy"]
#, "Precision", "recall", "F1 Score"
    acurracy = calculateKNearestNeighbor(df_train, target_train, "accuracy").mean() * 100
    #precision = calculateKNearestNeighbor(df_train, target_train, "precision").mean() * 100
    #recall = calculateKNearestNeighbor(df_train, target_train, "recall").mean() * 100
    #f1Score = calculateKNearestNeighbor(df_train, target_train, "f1").mean() * 100
    knn_df = pd.DataFrame(data = [acurracy], columns=fields) 
    print(knn_df)

def calculateKNearestNeighbor(df_train, target_train, scoringVal):
    kfold = KFold(n_splits=10)
    result = cross_val_score(KNeighborsClassifier(n_neighbors=3), df_train, target_train.values.ravel(), cv = kfold, scoring = scoringVal)
    return result


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
    df = pd.DataFrame(data = target_data)
    
    return df

def loadDataset():
    wineData = getWineData()
    data = wineData['data']
    headers = wineData['feature_names']
    df = pd.DataFrame(data = data, columns = headers)

    return df

def main():
    df = loadDataset()
    target_df = loadTargetDataset()
    printDataDetails(df)
    #plotData(df)
    df_train, df_test, target_train, target_test = train_test_split(df, target_df, test_size = 0.3)

    buildAndPrintKNN(df_train, target_train)




main()