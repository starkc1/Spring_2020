from sklearn import datasets as datasets

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt


def printAndPlotLinReg(data, target):
    train_X, test_X, train_y, test_y = train_test_split(data, target, test_size = 0.33)

    lin_reg = LinearRegression()
    lin_reg.fit(train_X, train_y)
    pred_y = lin_reg.predict(test_X)
    
    print("\nTheta:")
    print(lin_reg.intercept_, lin_reg.coef_)

    plt.figure("a")
    plt.hist(abs(test_y - pred_y), bins = 100)
    plt.xlabel("Error ($k)")
    

    print("MAE = " + str(mean_absolute_error(test_y, pred_y)))

    # plt.figure("b")
    plot_learning_curves(lin_reg, train_X, train_y)
    # plt.axis([0, 300, 0, 10])
    plt.show()

def printAndPlotPoly(data, target):
    poly = PolynomialFeatures(2)
    data = poly.fit_transform(data)

    


def plot_learning_curves(model, X, y):
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2)

    training_errors, validation_errors = [], []

    for m in range(1, len(train_X)):

        model.fit(train_X[:m], train_y[:m])

        train_pred = model.predict(train_X)
        test_pred = model.predict(test_X)

        training_errors.append(np.sqrt(mean_squared_error(train_y, train_pred)))
        validation_errors.append(np.sqrt(mean_squared_error(test_y, test_pred)))

    #print(training_errors)
    plt.figure('b')
    plt.plot(training_errors, "r-+", label = "train")
    plt.plot(validation_errors, "b-", label = "test")
    plt.legend()
    #plt.axis([0, 80, 0, 3])
    


def printDataDetails(dataset): 
    data = dataset['data']
    headers = dataset['feature_names']
    df = pd.DataFrame(data = data, columns = headers)
    
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
    printAndPlotLinReg(data, target)
    printAndPlotPoly(data, target)

main()