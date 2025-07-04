import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import pickle
import os

# Create pickle directory if it doesn't exist
if not os.path.exists('realpickle'):
    os.makedirs('realpickle')

# Load data
df = pd.read_csv(
    r"D:\!!WORK\!!WU-ITD\3\1-67\!--- PROJECT ---!\test\!!combine_CSV\try\data\data_combine\all\resamp\resampling_pm_drop_nan.csv",
    encoding="utf8"
)

df = df[['pm0_1_center_', 'pm2_5_center_',
         'temperature_c_dht22_', 'humidity_dht22_',
         'door_wind_speed']]

selected_features = ['pm2_5_center_', 'temperature_c_dht22_', 'humidity_dht22_', 'door_wind_speed']
X = df[selected_features]
y = df[['pm0_1_center_']]

y = y.values.ravel()

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Define models with specific parameters
models = {
    "LightGBM": LGBMRegressor(learning_rate=0.1, max_depth=8, n_estimators=400, num_leaves=16, subsample=0.1),
    "XGB": XGBRegressor(subsample=0.7, n_estimators=500, max_depth=6, learning_rate=0.1, colsample_bytree=1.0),
    "GradientBoosting": GradientBoostingRegressor(subsample=0.7, n_estimators=900, max_depth=5, learning_rate=0.1),
    "AdaBoost": AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=3), n_estimators=600, learning_rate=0.3),
    "CatBoost": CatBoostRegressor(subsample=0.1, n_estimators=300, max_depth=7, learning_rate=0.3, colsample_bylevel=0.6, verbose=0)
}

results = {}

# Train and evaluate each model
for name, model in models.items():
    model_results = {'NAME': [], 'MAE': [], 'RMSE': [], 'R^2': []}
    for fold in range(10):
        print(f"Training {name} - Fold {fold}...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=fold)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        test_mae = mean_absolute_error(y_test, y_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        test_r2 = r2_score(y_test, y_pred)
        print(f"Fold {fold}: MAE={test_mae:.4f}, RMSE={test_rmse:.4f}, R^2={test_r2:.4f}")
        model_results['NAME'].append(name)
        model_results['MAE'].append(round(test_mae, 4))
        model_results['RMSE'].append(round(test_rmse, 4))
        model_results['R^2'].append(round(test_r2, 4))

    avg_results = {
        'MAE': np.mean(model_results['MAE']),
        'RMSE': np.mean(model_results['RMSE']),
        'R^2': np.mean(model_results['R^2']),
    }
    results[name] = avg_results

    model_filename = os.path.join('realpickle', f"vali_{name.replace(' ', '_')}_model.pkl")
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model {name} saved to {model_filename}")

results_df = pd.DataFrame(results).T
print("Average Results:")
print(results_df)
