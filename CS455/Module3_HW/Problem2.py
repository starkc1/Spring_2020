from sklearn import datasets as datasets

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import Ridge

import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

# CS 455 - Artificial Intelligence
# Homework 3 - KNN and Regression Models
# Contributers - Cameron Stark & Dustin Cribbs
# Sources - Github and other online resources

def printAndPlotLinReg(data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target)

    lin_reg = LinearRegression()
    lin_reg.fit(train_X, train_y)
    pred_y = lin_reg.predict(test_X)
    
    print("\nTheta:")
    print(lin_reg.intercept_, lin_reg.coef_)

    # plt.figure("a")
    # plt.hist(abs(test_y - pred_y), bins = 100)
    # plt.xlabel("Error ($k)")
    
    plot("Linear Regression", test_y, pred_y)
    print("MAE = " + str(mean_absolute_error(test_y, pred_y)))

    # plt.figure("b")
    plot_learning_curves(lin_reg, train_X, train_y, "Linear Regression")
    # plt.axis([0, 300, 0, 10])
    plt.show()

def printAndPlotPoly(data, target):
    print("Polynomial Regression")

def printAndPlotLingReg_Regularization(data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target)

    ridge = Ridge(alpha = 0.01)
    ridge.fit(train_X, train_y)

    lin_reg = LinearRegression()
    pred_y = ridge.predict(test_X)
    
    print("Theta:")
    print(ridge.intercept_, ridge.coef_)
    
    plot("Ridge", test_y, pred_y)
    print("MAE = " + str(mean_absolute_error(test_y, pred_y)))

    plot_learning_curves(ridge, train_X, train_y, "Ridge")
    plt.show()
    
    
def plot(model, test_y, pred_y):
    plt.figure(model + " a")
    plt.hist(abs(test_y - pred_y), bins = 100)
    plt.xlabel("Error ($k)")

def plot_learning_curves(model, X, y, modelName):
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2)

    training_errors, validation_errors = [], []

    for m in range(1, len(train_X)):

        model.fit(train_X[:m], train_y[:m])

        train_pred = model.predict(train_X)
        test_pred = model.predict(test_X)

        training_errors.append(np.sqrt(mean_squared_error(train_y, train_pred)))
        validation_errors.append(np.sqrt(mean_squared_error(test_y, test_pred)))

    #print(training_errors)
    plt.figure(modelName + ' b')
    plt.plot(training_errors, "r-+", label = "train")
    plt.plot(validation_errors, "b-", label = "test")
    plt.legend()
    #plt.axis([0, 80, 0, 3])
    
def plotData(data):
    scatter_matrix(data, alpha = 0.2, figsize=(12, 12))
    plt.show()

def printDataDetails(dataset): 
    data = dataset['data']
    headers = dataset['feature_names']
    df = pd.DataFrame(data = data, columns = headers)
    #plotData(df)
    print("\nData Shape & Details")
    print(df.shape)
    print(df.describe().loc[['max', 'min', 'mean']])

def getDiabetesData():
    return datasets.load_diabetes()

def loadDataset():
    df = getDiabetesData()
    printDataDetails(df)
    return df
    #print(df)

def main():
    df = loadDataset()
    data = df['data']
    target = df['target']
    
    #printAndPlotLinReg(data, target)
    #printAndPlotPoly(data, target)
    printAndPlotLingReg_Regularization(data, target)

main()