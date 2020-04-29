import os
import tarfile
import urllib.request
import zipfile
from glob import glob
import pandas as pd

def parse_url(url):
    tarname = url.split('/')[-1]
    flightname = tarname.split('.')[0]
    return tarname, flightname
    
def download_and_extract(url, data_dir):
    flights_raw = os.path.join(data_dir, parse_url(url)[0])
    flightdir = os.path.join(data_dir, parse_url(url)[1])

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        
    if not os.path.exists(flights_raw):
        print("- Downloading NYC Flights dataset... ", end='', flush=True)
        print(url)
#        url = "https://storage.googleapis.com/dask-tutorial-data/nycflights.tar.gz"
        urllib.request.urlretrieve(url, flights_raw)
        print("done", flush=True)
  
    if not os.path.exists(flightdir):
        print("- Extracting flight data... ", end='', flush=True)
        tar_path = os.path.join(data_dir, parse_url(url)[0])
        with tarfile.open(tar_path, mode='r:gz') as flights:
            flights.extractall(data_dir)
        print("done", flush=True)
        
def create_json(data_dir, flightname, num_rows):
    jsondir = os.path.join(data_dir, 'flightjson')
    
    if not os.path.exists(jsondir):
        print("- Creating json data... ", end='', flush=True)
        os.mkdir(jsondir)
        for path in glob(os.path.join(data_dir, flightname, '*.csv')):
            prefix = os.path.splitext(os.path.basename(path))[0]
            # Just take the first 10000 rows for the demo
            df = pd.read_csv(path).iloc[:num_rows]
            df.to_json(os.path.join(data_dir, 'flightjson', prefix + '.json'),
                       orient='records', lines=True)
        print("done", flush=True)    
        
def prepare_flights(url, data_dir, num_rows):
    download_and_extract(url, data_dir)
    create_json(data_dir, parse_url(url)[1], num_rows)
    print("** Finished! **")
    
    
    
# def flights(url, data_dir, num_rows):
#     flights_raw = os.path.join(data_dir, 'nycflights.tar.gz')
#     flightdir = os.path.join(data_dir, 'nycflights')
#     jsondir = os.path.join(data_dir, 'flightjson')

#     if not os.path.exists(data_dir):
#         os.mkdir(data_dir)

#     if not os.path.exists(flights_raw):
#         print("- Downloading NYC Flights dataset... ", end='', flush=True)
# #        url = "https://storage.googleapis.com/dask-tutorial-data/nycflights.tar.gz"
#         urllib.request.urlretrieve(url, flights_raw)
#         print("done", flush=True)

#     if not os.path.exists(flightdir):
#         print("- Extracting flight data... ", end='', flush=True)
#         tar_path = os.path.join('data', 'nycflights.tar.gz')
#         with tarfile.open(tar_path, mode='r:gz') as flights:
#             flights.extractall('data/')
#         print("done", flush=True)

#     if not os.path.exists(jsondir):
#         print("- Creating json data... ", end='', flush=True)
#         os.mkdir(jsondir)
#         for path in glob(os.path.join('data', 'nycflights', '*.csv')):
#             prefix = os.path.splitext(os.path.basename(path))[0]
#             # Just take the first 10000 rows for the demo
#             df = pd.read_csv(path).iloc[:num_rows]
#             df.to_json(os.path.join('data', 'flightjson', prefix + '.json'),
#                        orient='records', lines=True)
#         print("done", flush=True)

#     print("** Finished! **")