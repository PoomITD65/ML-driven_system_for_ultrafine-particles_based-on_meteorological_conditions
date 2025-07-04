from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from skopt import BayesSearchCV
from sklearn.tree import DecisionTreeRegressor
from collections import OrderedDict
import time

# Load dataset
df = (pd.read_csv(
    r"D:\!!WORK\!!WU-ITD\3\1-67\!--- PROJECT ---!\test\!!combine_CSV\try\data\data_combine\all\resamp\resampling_pm_drop_nan.csv",
    encoding="utf8"))

# Configuration
cv = 5
n = 10

# Data preparation
df = df[['pm0_1_center_', 'pm2_5_center_',
         'temperature_c_dht22_', 'humidity_dht22_',
         'door_wind_speed', 'window_wind_speed']]

# df = df.sample(frac=0.01, random_state=42)
print("Dataset Columns:", df.keys())
print(df.describe().to_string())

# Feature selection
selected_features = ['pm2_5_center_',
                     'temperature_c_dht22_', 'humidity_dht22_',
                     'door_wind_speed']

X = df[selected_features]
y = df[['pm0_1_center_']].values.ravel()  # Converts y to a 1D array

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.7, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Model results storage
model_results = {'NAME': [], 'MAE': [], 'RMSE': [], 'R^2': [], 'TIME': []}
best_para = []


# Function to record the best parameters
def record_best_params(name, model, elapsed_time):
    print(f"Model: {name}")
    print(f"Best Score: {model.best_score_}, Best Parameters: {model.best_params_}")
    params = dict(model.best_params_) if isinstance(model.best_params_, OrderedDict) else model.best_params_
    best_para.append({'NAME': name, 'PARAMS': params, 'SCORE': model.best_score_, 'TIME': elapsed_time})


# Hyperparameter grids
param_grids = {
    #  "xgb": {
    #     'n_estimators': (100, 200, 300),
    #     'max_depth': (3, 5, 7),
    #     'learning_rate': (0.1, 0.3, 0.5),
    #     'subsample': (0.5, 0.7, 1.0),
    #     'colsample_bytree': (0.5, 0.7, 1.0),
    # },
    # "gradientboosting": {
    #     'n_estimators': (100, 200, 300),
    #     'max_depth': (3, 5, 7),
    #     'subsample': (0.5, 0.7, 1.0),
    #     'learning_rate': (0.1, 0.3, 0.5),
    # },
    # "adaboost": {
    #     'n_estimators': (100, 200, 300),
    #     'learning_rate': (0.1, 0.3, 0.5),
    #     'base_estimator': [DecisionTreeRegressor(max_depth=d) for d in (1, 2, 3)],
    # },
    # "catboost": {
    #     'n_estimators': (100, 200, 300),
    #     'learning_rate': (0.1, 0.3, 0.5),
    #     'subsample': (0.5, 0.7, 1.0),
    #     'colsample_bylevel': (0.5, 0.7, 1.0),
    #     'max_depth': (3, 5, 7),
    # },
    "lightgbm": {
        'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
        'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
        'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9),
        'subsample': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
        'num_leaves': (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024),
    },
}

# Model initialization
models = {
    # "XGB": XGBRegressor(),
    # "GradientBoosting": GradientBoostingRegressor(),
    # "AdaBoost": AdaBoostRegressor(),
    # "CatBoost": CatBoostRegressor(),
    "LightGBM": LGBMRegressor(verbose=-1),
}

# Tuning loop
for name, model in models.items():
    param_grid = param_grids[name.lower()]
    # RandomizedSearchCV
    rand_search = RandomizedSearchCV(model, param_grid, cv=cv, n_iter=n, random_state=42)
    start_time = time.time()
    rand_search.fit(X_val, y_val)
    elapsed_time = time.time() - start_time
    record_best_params(f"Randomized {name}", rand_search, elapsed_time)

    # BayesSearchCV
    bayes_search = BayesSearchCV(model, param_grid, cv=cv, n_iter=n, random_state=42)
    start_time = time.time()
    bayes_search.fit(X_val, y_val)
    elapsed_time = time.time() - start_time
    record_best_params(f"Bayesian {name}", bayes_search, elapsed_time)

# Display best parameters for each model
print("\nBest Parameters Summary:")
for record in best_para:
    print(record)
