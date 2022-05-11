import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pickle
import joblib

import scipy
import scipy.stats
from numpy import mean, square, sqrt
from scipy.stats import kurtosis
from scipy.stats import skew
from collections import Counter
from scipy.stats import kurtosis
from scipy.stats import skew
import random
import math as m
from time import time


def extract_feature(Hss):
    s, size = Hss.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = np.mean(Hss[:, i])  # compute mean for each signal
        a.append(x)  # store the value to empty array

    Mean_H = np.array(a)  # convert list to array
    Mean_H.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = np.max(Hss[:, i])  # compute max for each signal
        a.append(x)  # store the value to empty array

    MAX_H = np.array(a)  # convert list to array
    MAX_H.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = np.min(Hss[:, i])  # compute min for each signal
        a.append(x)  # store the value to empty array

    MIN_H = np.array(a)  # convert list to array
    MIN_H.shape

    from numpy import sqrt, mean, square

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = sqrt(mean(square(Hss[:, i])))  # compute rms for each signal
        a.append(x)  # store the value to empty array

    RMS_H = np.array(a)  # convert list to array
    RMS_H.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = np.std(Hss[:, i])  # compute standard deviation(표준편차) for each signal
        a.append(x)  # store the value to empty array

    STD_H = np.array(a)  # convert list to array
    STD_H.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = np.var(Hss[:, i])  # compute Variance for each signal
        a.append(x)  # store the value to empty array

    VAR_H = np.array(a)  # convert list to array
    VAR_H.shape

    from scipy.stats import kurtosis

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = kurtosis(Hss[:, i])  # compute Kurtosis for each signal
        a.append(x)  # store the value to empty array

    KUR_H = np.array(a)  # convert list to array
    KUR_H.shape

    from scipy.stats import skew

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = skew(Hss[:, i])  # compute Skewness for each signal
        a.append(x)  # store the value to empty array

    SKEW_H = np.array(a)  # convert list to array
    SKEW_H.shape

    from scipy.stats import gstd

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = gstd(abs(Hss[:, i]))  # compute GSTD for each signal
        a.append(x)  # store the value to empty array

    GSTD_H = np.array(a)  # convert list to array
    GSTD_H.shape

    from scipy.stats import iqr

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = iqr(Hss[:, i])  # compute IQR for each signal
        a.append(x)  # store the value to empty array

    IQR_H = np.array(a)  # convert list to array
    IQR_H.shape

    from scipy.stats import sem

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = sem(Hss[:, i])  # compute SEM for each signal
        a.append(x)  # store the value to empty array

    SEM_H = np.array(a)  # convert list to array
    SEM_H.shape

    # from scipy.stats import median_abs_deviation

    # a = [] #create an empty list

    # for i in range(size):  #run a loop to compute every signal in the variable
    #    x = median_abs_deviation(Hss[:, i])  #compute MAD for each signal
    #    a.append(x)  #store the value to empty array

    # MAD_H = np.array(a) #convert list to array
    # MAD_H.shape

    a = []  # create an empty list

    for i in range(size):  # run a loop to compute every signal in the variable
        x = max(Hss[:, i]) / RMS_H[i]  # compute Crest Factor for each signal
        a.append(x)  # store the value to empty array

    CF_H = np.array(a)  # convert list to array
    CF_H.shape

    Motor_FT = pd.DataFrame([Mean_H, RMS_H, VAR_H, STD_H,
                             GSTD_H, IQR_H, SEM_H, MAX_H, MIN_H,
                             KUR_H, SKEW_H, CF_H]).T

    names = ['Mean', 'RMS', 'VAR', 'STD', 'GSTD',
             'IQR', 'SEM', 'MAX_H', 'MIN_H',
             'KUR', 'SKEW', 'CF']
    Motor_FT.columns = names
    # Motor_FT['State'] = 0

    return Motor_FT


def feature_process(data_frame, batch_size=5110):
    columns = ['Mean', 'RMS', 'VAR', 'STD', 'GSTD', 'IQR', 'SEM', 'MAX_H', 'MIN_H', 'KUR', 'SKEW']
    before = 0
    train_data = pd.DataFrame(np.zeros((1, 11)), columns=columns)
    for i in tqdm(range(batch_size, len(data_frame), batch_size)):
        features = extract_feature(data_frame[before:i].to_numpy().reshape(-1, 1))
        before = i
        train_data = train_data.append(features, ignore_index=True)

    return train_data[1:]


def get_anomaly_scores(clf, data):
    return clf.decision_function(data).reshape(-1, 1)


def get_abnormal_data(df):
    vib1_abnormal_random = []
    max_value = max(df)
    min_value = min(df)
    value = max(abs(max_value), abs(min_value))
    for i in tqdm(range(0, len(df))):
        a = random.uniform(0, value * 0.25)
        if df[i] > 0:
            vib1_abnormal_random.append(df[i] + a)
        elif df[i] < -0:
            vib1_abnormal_random.append(df[i] - a)
    return pd.DataFrame(vib1_abnormal_random,
                        columns=['x1'])


def collection(filepath):
    columns = ['Mean', 'RMS', 'VAR', 'STD', 'GSTD', 'IQR', 'SEM', 'MAX_H', 'MIN_H', 'KUR', 'SKEW', 'CF']
    df = pd.DataFrame(np.zeros((1, 12)), columns=columns)
    for i, file1 in enumerate(filepath):
        vib1 = pd.read_csv(file1, sep='\t', names=['time', 'data'],
                           header=None, encoding='CP949').iloc[:47962461, 1]

        vib1_features = feature_process(vib1)
        df = df.append(pd.DataFrame(vib1_features, columns=columns))

    return df


clf = LocalOutlierFactor(n_neighbors=1000,novelty=True)
clf.fit(X_train)

plt.rcParams.update(plt.rcParamsDefault)
plt.style.use('seaborn-notebook')


X_valid = pd.read_csv('03_30/VIB_0330_motor_51200.csv', sep = '\t',
                     names = ['time', 'data'], header = None, encoding = 'CP949').iloc[:47962461,1]
X_abnormal = get_abnormal_data(X_valid)
X_valid = feature_process(X_valid)

anomaly_scores = clf.predict(X_valid)
anomaly_scores = pd.DataFrame(anomaly_scores.reshape(-1) ,columns=['x1'])

X_abnormal = feature_process(X_abnormal)
outliers = clf.predict(X_abnormal)
outliers = pd.DataFrame(outliers.reshape(-1) ,columns=['x1'])