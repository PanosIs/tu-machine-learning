# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:41:51 2020

@author: Charlotte
"""

from pandas import read_excel
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

#Finding zones with latitude and longitude
#how many clusters? ----> 4
from src.regressors.support_vector_machine import SVMWrapper


def elbowcurve(data):
    Nc = range(1, 10)
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    score = [kmeans[i].fit(data).score(data) for i in range(len(kmeans))]
    pyplot.plot(Nc,score)
    pyplot.xlabel('Number of Clusters')
    pyplot.ylabel('Score')
    pyplot.title('Elbow Curve')
    pyplot.show()

#Do clustering
def clustering(data):
    model = KMeans(n_clusters = 4)
    model.fit(data)
    colormap = np.array(['Red', 'Blue', 'Green','Orange'])
    pyplot.scatter(data['X6 longitude'],data['X5 latitude'], c = colormap[model.labels_])
    pyplot.show()
    return model.labels_

#one hot encoding of clusters
def onehot_encoding(m):
    onehot_encoder = OneHotEncoder(sparse=False)
    m = m.reshape(len(m), 1)
    onehot_encoded = onehot_encoder.fit_transform(m)
    return onehot_encoded

def preprocess_data(dataset):
    x = dataset[['X5 latitude', 'X6 longitude']]
    # One hot encoding of clusters
    m = clustering(x)
    onehot_encoded = onehot_encoding(m)

    print("Preparing train-test split")
    # Splitting the dataset into Training set and Test Set
    X = dataset.iloc[:, 1:-3].values
    X = np.append(X, onehot_encoded, axis=1)
    y = dataset.iloc[:, 7].values

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    print("Normalizing values")
    # Standardisation
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    return x_train, x_test, y_train, y_test

if __name__ == "__main__":
    print("Loading data")
    # Load dataset
    dataset= read_excel('resources/Real_estate_valuation_data_set.xlsx')
    preprocess_data(dataset)


