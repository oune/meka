import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from tqdm import tqdm
import joblib
from numpy import mean, square, sqrt
from scipy.stats import kurtosis, gstd
from scipy.stats import skew
from scipy.stats import sem
from scipy.stats import iqr
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Model:
    columns = ['Mean', 'RMS', 'VAR', 'STD', 'GSTD', 'IQR',
               'SEM', 'MAX_H', 'MIN_H', 'KUR', 'SKEW', 'CF']

    def __init__(self, value, is_init):
        if is_init is True:
            self.__clf = LocalOutlierFactor(n_neighbors=value, novelty=True)
        else:
            self.__clf = joblib.load(value)

    def save_model(self, filepath):
        if self.__clf is not None:
            joblib.dump(self.__clf, filepath)

    @classmethod
    def load_model(cls, filepath):
        return cls(filepath, False)

    @classmethod
    def init_model(cls, n_neighbors=1000):
        return cls(n_neighbors, True)

    def __extract_feature(self, Hss):

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

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = sqrt(mean(square(Hss[:, i])))  # compute rms for each signal
            a.append(x)  # store the value to empty array

        RMS_H = np.array(a)  # convert list to array
        RMS_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            # compute standard deviation(표준편차) for each signal
            x = np.std(Hss[:, i])
            a.append(x)  # store the value to empty array

        STD_H = np.array(a)  # convert list to array
        STD_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = np.var(Hss[:, i])  # compute Variance for each signal
            a.append(x)  # store the value to empty array

        VAR_H = np.array(a)  # convert list to array
        VAR_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = kurtosis(Hss[:, i])  # compute Kurtosis for each signal
            a.append(x)  # store the value to empty array

        KUR_H = np.array(a)  # convert list to array
        KUR_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = skew(Hss[:, i])  # compute Skewness for each signal
            a.append(x)  # store the value to empty array

        SKEW_H = np.array(a)  # convert list to array
        SKEW_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = gstd(abs(Hss[:, i]))  # compute GSTD for each signal
            a.append(x)  # store the value to empty array

        GSTD_H = np.array(a)  # convert list to array
        GSTD_H.shape

        a = []  # create an empty list

        for i in range(size):  # run a loop to compute every signal in the variable
            x = iqr(Hss[:, i])  # compute IQR for each signal
            a.append(x)  # store the value to empty array

        IQR_H = np.array(a)  # convert list to array
        IQR_H.shape

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
            # compute Crest Factor for each signal
            x = max(Hss[:, i]) / RMS_H[i]
            a.append(x)  # store the value to empty array

        CF_H = np.array(a)  # convert list to array
        CF_H.shape

        Motor_FT = pd.DataFrame([Mean_H, RMS_H, VAR_H, STD_H,
                                 GSTD_H, IQR_H, SEM_H, MAX_H, MIN_H,
                                 KUR_H, SKEW_H, CF_H]).T

        Motor_FT.columns = Model.columns
        # Motor_FT['State'] = 0

        return Motor_FT

    def __feature_process(self, data_frame, batch_size=config['model']['batchsize']):
        before = 0
        train_data = pd.DataFrame(np.zeros((1, 12)), columns=Model.columns)

        if len(data_frame) <= batch_size:
            features = self.__extract_feature(
                data_frame.to_numpy().reshape(-1, 1))
            return features

        for i in tqdm(range(batch_size, len(data_frame), batch_size)):
            features = self.__extract_feature(
                data_frame[before:i].to_numpy().reshape(-1, 1))
            before = i
            train_data = train_data.append(features, ignore_index=True)

        return train_data[1:]

    def predict(self, data_frame):
        # 1정상 -1 비정상
        df = self.__feature_process(data_frame)
        return self.__clf.predict(df), self.__clf.decision_function(df).reshape(-1, 1)

    def training(self, data_frame):
        self.__clf.fit(data_frame)


if __name__ == '__main__':
    arr = np.random.randn(100)
    df = pd.DataFrame(arr).astype('float')
    motor = Model.load_model('motor_tmp.pkl')
    pump = Model.load_model('pump_tmp.pkl')
    print("model loaded")
    a, b = motor.predict(df)
    print(type(a[0]))
    print(type(b))
    print({"res": a, "score": b})
