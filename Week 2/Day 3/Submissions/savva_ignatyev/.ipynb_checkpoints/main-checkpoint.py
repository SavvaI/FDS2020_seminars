#!/usr/bin/env python

from __future__ import print_function

import os
import numpy as np
import pandas as pd
import tarfile
import urllib.request
import zipfile
import argparse
from sklearn.ensemble import GradientBoostingRegressor
from dask.distributed import Client



from src.data_loading import prepare_flights
from src.ml import hyperparametr_search

# data_dir = 'data'

def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str,
                       default="https://storage.googleapis.com/dask-tutorial-data/nycflights.tar.gz",
                       help='url to download data from')
    parser.add_argument('--data_dir', type=str,
                        default='data', help='location to store downloaded data')
    parser.add_argument('--num_rows', type=int,
                        default=10000, help='number of rows from dataframe to use')
     
    args = parser.parse_args()
    return args
    
features = ['Year', 'Month', 'DayOfWeek', 'DepDelay', 'UniqueCarrier', 'Origin', 'Dest']

def run():
    client = Client(threads_per_worker=5,
    n_workers=5, memory_limit='1GB')
    params = {'max_depth': [1, 2, 3], 'n_estimators': [1, 2, 3]}
    metric, best_estimator = src.ml.hyperparametr_search(GradientBoostingRegressor(random_state=42), params, x_train, x_test, y_train, y_test)
    return metric, best_estimator
    
def main():
    args = set_args()  
    params = {'max_depth': [1, 2, 3], 'n_estimators': [1, 2, 3]}
    
    print("Setting up data directory")
    print("-------------------------")

    prepare_flights(args.url, args.data_dir, args.num_rows)
    metric, best_estimator = run()
    

    print('Finished!')


if __name__ == '__main__':
    main()
