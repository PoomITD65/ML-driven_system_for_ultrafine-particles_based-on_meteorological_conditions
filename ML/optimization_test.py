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

df = (pd.read_csv(
    r"D:\!!WORK\!!WU-ITD\3\1-67\!--- PROJECT ---!\test\!!combine_CSV\try\data\data_combine\all\resamp\resampling_pm_drop_nan.csv",
    encoding="utf8"))

cv = 5
n = 10

df = df[['pm0_1_center_', 'pm2_5_center_',
         'temperature_c_dht22_', 'humidity_dht22_',
         'door_wind_speed']]

# df = df.sample(frac=0.01)
print(df.keys())
# df['Month'] = LabelEncoder().fit_transform(df['Month'])
# print(df[['pm0_1_center_', 'pm2_5_center_', 'pm10_center_', 'door_center_',
#           'window_1_under_air_center_', 'window_2_center_', 'incense_sticks_center_',
#           'temperature_c_dht22_', 'humidity_dht22_', 'door_wind_speed',
#           'window_wind_speed']].describe().to_string())

# Select features and target variable
selected_features = ['pm2_5_center_',
                     'temperature_c_dht22_', 'humidity_dht22_',
                     'door_wind_speed']
# df = df[~df.Year.isin([2022, 2023])]
x = df[selected_features]
y = df[['pm0_1_center_']]

x = pd.DataFrame(x)
y = pd.DataFrame(y)

y = y.values.ravel()

X_train, X_temp, y_train, y_temp = train_test_split(x, y, test_size=0.7, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

model_results = {'NAME': [], 'MAE': [], 'RMSE': [], 'R^2': [], 'TIME': []}

best_para = []


def papam_optim(name, model, time):
    print("Model Characteristics")
    print("Best: %f using %s" % (model.best_score_, model.best_params_))
    print(type(model.best_params_))
    if type(model.best_params_) is OrderedDict:
        model.best_params_ = dict(model.best_params_)

    para = {}
    para['PARA'] = model.best_params_
    para['SCORE'] = model.best_score_
    para['TIME'] = round(time, 4)
    para['NAME'] = name
    # best_para.append(para)

    best_para.append(para)


# def model_performance(name, model, X_test, X_val, y_test, y_val, time):
#     # # Make predictions
#     print("Model Prediction")
#     train_predictions = model.predict(X_test)
#
#     # Calculate mean squared error
#     train_mse = mean_squared_error(y_test, train_predictions)
#     train_rmse = np.sqrt(train_mse)
#     print("Testing-based RMSE:", train_rmse)
#     #
#     train_mae = mean_absolute_error(y_test, train_predictions)
#     print("Training-based MAE:", train_mae)
#
#     train_r2 = r2_score(y_test, train_predictions)
#     print("Training-based R2:", train_r2)
#
#     print('\n------------------------------\n')
#     # Make predictions
#     val_predictions = model.predict(X_val)
#
#     # # Calculate mean squared error
#     val_mse = mean_squared_error(y_val, val_predictions)
#     val_rmse = np.sqrt(val_mse)
#     print("Validating-based RMSE:", val_rmse)
#
#     val_mae = mean_absolute_error(y_val, val_predictions)
#     print("Validating-based MAE:", val_mae)
#
#     test_r2 = r2_score(y_val, val_predictions)
#     print("Validating-based R2:", test_r2)
#
#     model_results['NAME'].append(name)
#     model_results['MAE'].append(round(val_mae, 4))
#     model_results['RMSE'].append(round(val_rmse, 4))
#     model_results['R^2'].append(round(test_r2, 4))
#     model_results['TIME'].append(round(time, 4))
#
#     print("-------------- \n")

print("-------XGB is being tuned-------\n")
xgb_param = {
    'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
    'max_depth': (2, 3, 4, 5, 6, 7, 8, 9),
    'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    'subsample': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    'colsample_bytree': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
}

# xgb_grid = XGBRegressor()
# xgb_grid_clf = GridSearchCV(xgb_grid, xgb_param, cv=cv)
# # start = time.time()
# xgb_grid_clf.fit(X_val, y_val)
# papam_optim("Grid XGB", xgb_grid_clf)
# # total_time = time.time() - start
# # model_performance("Grid XGB", xgb_grid_clf, X_test, X_val, y_test, y_val, total_time)

xgb_rand = XGBRegressor()
xgb_rand_clf = RandomizedSearchCV(xgb_rand, xgb_param, cv=cv, n_iter=n)
start = time.time()
xgb_rand_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Rand XGB", xgb_rand_clf, total_time)

# start = time.time()
# total_time = time.time() - start
# model_performance("Rand XGB", xgb_rand_clf, X_test, X_val, y_test, y_val, total_time)

xgb_bayes = XGBRegressor()
xgb_bayes_clf = BayesSearchCV(xgb_bayes, xgb_param, cv=cv, n_iter=n)
start = time.time()
xgb_bayes_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Bayes XGB", xgb_bayes_clf, total_time)
# total_time = time.time() - start
# model_performance("Bayes XGB", xgb_bayes_clf, X_test, X_val, y_test, y_val, total_time)


#
print("-------GradientBoosting is being tuned-------\n")
gradient_boosting_param = {
    'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
    'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9),
    'subsample': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
}
# gb_grid = GradientBoostingRegressor()
# gb_grid_clf = GridSearchCV(gb_grid, gradient_boosting_param, cv=cv)
# start = time.time()
# gb_grid_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Grid GradientBoosting", gb_grid_clf, X_test, X_val, y_test, y_val, total_time)

gb_rand = GradientBoostingRegressor()
gb_rand_clf = RandomizedSearchCV(gb_rand, gradient_boosting_param, cv=cv, n_iter=n)
start = time.time()
gb_rand_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Rand GradientBoosting", gb_rand_clf, total_time)
# start = time.time()
# gb_rand_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Rand GradientBoosting", gb_rand_clf, X_test, X_val, y_test, y_val, total_time)

gb_bayes = GradientBoostingRegressor()
gb_bayes_clf = BayesSearchCV(gb_bayes, gradient_boosting_param, cv=cv, n_iter=n)
start = time.time()
gb_bayes_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Bayes GradientBoosting", xgb_bayes_clf, total_time)

# gb_bayes_clf.fit(X_train, y_train)
# model_performance("Bayes GradientBoosting", gb_bayes_clf, X_test, X_val, y_test, y_val, total_time)
#


print("-------AdaBoost is being tuned-------\n")
adaboost_param = {
    'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
    'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    'base_estimator': (
        DecisionTreeRegressor(max_depth=1), DecisionTreeRegressor(max_depth=2), DecisionTreeRegressor(max_depth=3)),
}
# ab_grid = AdaBoostRegressor()
# ab_drid_clf = GridSearchCV(ab_grid, adaboost_param, cv=5)
# start = time.time()
# ab_drid_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Grid AdaBoost", ab_drid_clf, X_test, X_val, y_test, y_val, total_time)

ab_rand = AdaBoostRegressor()
ab_rand_clf = RandomizedSearchCV(ab_rand, adaboost_param, cv=cv, n_iter=n)
start = time.time()
ab_rand_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Randomized AdaBoost", ab_rand_clf, total_time)
# start = time.time()
# ab_rand_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Randomized AdaBoost", ab_rand_clf, X_test, X_val, y_test, y_val, total_time)

ab_bayes = AdaBoostRegressor()
ab_bayes_clf = BayesSearchCV(ab_bayes, adaboost_param, cv=cv, n_iter=n)
start = time.time()
ab_bayes_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Bayes AdaBoost", ab_bayes_clf, total_time)
# start = time.time()
# ab_bayes_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Bayes AdaBoost", ab_bayes_clf, X_test, X_val, y_test, y_val, total_time)
#


print("-------CatBoost is being tuned-------\n")
catboost_param = {
    'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
    'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    'subsample': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    'colsample_bylevel': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9),
}

# cb_grid = CatBoostRegressor()
# cb_drid_clf = GridSearchCV(cb_grid, catboost_param, cv=cv)
# start = time.time()
# cb_drid_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Grid CatBoost", cb_drid_clf, X_test, X_val, y_test, y_val, total_time)

cb_rand = CatBoostRegressor()
cb_rand_clf = RandomizedSearchCV(cb_rand, catboost_param, cv=cv, n_iter=n)
start = time.time()
cb_rand_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Randomized CatBoost", cb_rand_clf, total_time)
# start = time.time()
# cb_rand_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Randomized CatBoost", cb_rand_clf, X_test, X_val, y_test, y_val, total_time)

cb_bayes = CatBoostRegressor()
cb_bayes_clf = BayesSearchCV(cb_bayes, catboost_param, cv=cv, n_iter=n)
start = time.time()
cb_bayes_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Bayes CatBoost", cb_bayes_clf, total_time)
# start = time.time()
# cb_bayes_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Bayes CatBoost", cb_bayes_clf, X_test, X_val, y_test, y_val, total_time)

print("-------LightGMB is being tuned-------\n")
light_gmb_param = {
    'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900),
    'learning_rate': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9),
    'subsample': (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    'num_leaves': (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024),
}
#
# print("-------LGBM is being tuned-------\n")
# lgbm_grid = LGBMRegressor()
# lgbm_drid_clf = GridSearchCV(lgbm_grid, light_gmb_param, cv=cv)
# start = time.time()
# lgbm_drid_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Grid LGBM", lgbm_drid_clf, X_test, X_val, y_test, y_val, total_time)
#
lgbm_rand = LGBMRegressor()
lgbm_rand_clf = RandomizedSearchCV(lgbm_rand, light_gmb_param, cv=cv, n_iter=n)
start = time.time()
lgbm_rand_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Randomized LGBM", lgbm_rand_clf, total_time)
# start = time.time()
# lgbm_rand_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Randomized LGBM", lgbm_rand_clf, X_test, X_val, y_test, y_val, total_time)

lgbm_bayes = LGBMRegressor()
lgbm_bayes_clf = BayesSearchCV(lgbm_bayes, light_gmb_param, cv=cv, n_iter=n)
start = time.time()
lgbm_bayes_clf.fit(X_val, y_val)
total_time = time.time() - start
papam_optim("Bayes LGBM", lgbm_bayes_clf, total_time)
# start = time.time()
# lgbm_bayes_clf.fit(X_train, y_train)
# total_time = time.time() - start
# model_performance("Bayes LGBM", lgbm_bayes_clf, X_test, X_val, y_test, y_val, total_time)

# results_df = pd.DataFrame(model_results)
# print(f'{results_df} \n')
#
print('\n'.join('{}'.format(item) for item in best_para))

# print("-------RandomForest is being tuned-------\n")
# random_forest_param = {'max_depth': (2, 3, 4, 5, 6, 7, 8, 9),
#                        'min_samples_leaf': (2, 3, 4, 5, 6, 7, 8, 9),
#                        'min_samples_split': (2, 3, 4, 5, 6, 7, 8, 9),
#                        'n_estimators': (100, 200, 300, 400, 500, 600, 700, 800, 900)
#                        }
#
# rf_grid = RandomForestRegressor()
# rf_grid_clf = GridSearchCV(rf_grid, random_forest_param, cv=cv)
# start = time.time()
# rf_grid_clf.fit(x, y)
# total_time = time.time() - start
# model_performance("Grid RandomForest", rf_grid_clf, X_train, X_test, y_train, y_test, total_time)

# rf_rand = RandomForestRegressor()
# rf_rand_clf = RandomizedSearchCV(rf_rand, random_forest_param, cv=cv, n_iter=n)
# start = time.time()
# rf_rand_clf.fit(x, y)
# total_time = time.time() - start
# model_performance("Rand RandomForest", rf_rand_clf, X_train, X_test, y_train, y_test, total_time)
#
# rf_bayes = RandomForestRegressor()
# rf_bayes_clf = BayesSearchCV(rf_bayes, random_forest_param, cv=cv, n_iter=n)
# start = time.time()
# rf_bayes_clf.fit(x, y)
# total_time = time.time() - start
# model_performance("Bayes RandomForest", rf_bayes_clf, X_train, X_test, y_train, y_test, total_time)
