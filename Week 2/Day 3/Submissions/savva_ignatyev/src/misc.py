import os
import pandas as pd

def list_files_dir(path):
    only_files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return only_files

def list_df_dir(path, num_rows=-1):
    list_files = list_files_dir(path)
    return [pd.read_csv(p).head(num_rows) for p in list_files_dir(path)]
    
def concat_df(ls):
    return pd.concat([pd.DataFrame(i) for i in ls], axis=0)