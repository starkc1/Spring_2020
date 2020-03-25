from sklearn import datasets as datasets
import numpy












def loadDataset():
    wineData = datasets.load_wine()
    return wineData

def main():
    dataset = loadDataset()
    print(dataset.data)
    print(dataset.target)
    print(dataset.target_names)
    print(dataset.feature_names)
    print(dataset.DESCR)

main()