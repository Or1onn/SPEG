import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd


def calc_mae(y_true, y_pred):
    return np.abs(y_true - y_pred).mean()


def calc_rmse(y_true, y_pred):
    return np.sqrt(((y_true - y_pred) ** 2).mean())


def calc_nmae(y_true, y_pred):
    return (np.abs(y_true - y_pred).mean() / y_true.mean()) * 100


# creation of the model, that predicts y as a function of X
def train_model(model, x, y):
    model.fit(x, y)


def evaluate_model(model, x, y, error_function):
    return error_function(y, model.predict(x))  # reshape to make a row vector


df = pd.read_excel('files/solar_cleared_data.xlsx')

df = df.dropna()
train, test = train_test_split(df, test_size=0.2)

x_train = train.iloc[:, :-1].values
y_train = train.iloc[:, -1].values

x_test = test.iloc[:, :-1].values
y_test = test.iloc[:, -1].values

model = GradientBoostingRegressor()

train_model(model, x_train, y_train)

print("Train MAE = {:.2f}".format(evaluate_model(model, x_train, y_train, calc_mae)))
print("Train nMAE = {:.2f}".format(evaluate_model(model, x_train, y_train, calc_nmae)))
print("Train RMSE = {:.2f}".format(evaluate_model(model, x_train, y_train, calc_rmse)))
