import numpy as np
import pandas as pd
import dask 
import dask.array as da
import dask.dataframe as dd
from dask.distributed import Client
import dask_xgboost
import sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import joblib
from dask.distributed import Client


def prepare_data(df, y_name, train_test_ratio=0.15):
    df = pd.DataFrame(df)
    df = df.dropna()
    y = df[y_name]
    del df[y_name]
    df = pd.get_dummies(df)
    x = df.to_numpy()
    y = y.to_numpy()
    return train_test_split(x, y, test_size=train_test_ratio, random_state=42)
    
    
def hyperparametr_search(model, param_dict, x_train, x_test, y_train, y_test):
    search_cv = GridSearchCV(model,  cv=StratifiedKFold(n_splits=4, random_state=42),
                     n_jobs=-1, param_grid=param_dict, scoring='neg_mean_squared_error')
    
    name = type(model).__name__
    
    with joblib.parallel_backend("dask"):
        search_cv.fit(x_train, y_train)
        
    y_test_ = search_cv.best_estimator_.predict(X_test)
    metric = mean_squared_error(y_test, y_test_)
    return metric, search_cv.best_estimator_