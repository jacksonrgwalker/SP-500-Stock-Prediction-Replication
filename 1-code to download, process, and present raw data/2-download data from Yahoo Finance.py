# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:06:53 2020

@author: zhong
"""

################################################
import sys, os
from pathlib import Path
project_dir = Path.cwd()
os.chdir(project_dir)
sys.path.append(os.getcwd())
# os.chdir('change to the mother working directory')'

import yfinance as yf
from tqdm import tqdm
import time
import json

ticker_names_file_path = Path('data/1-ticker_name_list.json')
with open(ticker_names_file_path, 'r') as fp:
    ticker_name_list = json.load(fp)
tickers = list(ticker_name_list.keys())

yf_save_file_path = Path('data/stock_data_YF.json')
# create file if it does not exist
if not yf_save_file_path.is_file():
    with open(yf_save_file_path, 'w') as fp:
        json.dump({}, fp)

# load file
with open(yf_save_file_path, 'r') as fp:
    stock_data_YF = json.load(fp)

fetches = 0
for ticker in tqdm( tickers ):

    # skip if already downloaded
    if ticker in stock_data_YF.keys():
        continue

    # fetch data
    stock = yf.Ticker(ticker)
    _closing_dat = stock.history(auto_adjust=False,back_adjust=False,rounding=False,period="max")   
    fetches += 1

    if len(_closing_dat) == 0:
        continue
    
    # can't write datetime to json, so convert to string
    _closing_dat.index = _closing_dat.index.strftime("%Y-%m-%d")
    stock_data_YF[ticker] = _closing_dat.T.to_dict()
    
    # save data to file
    # we do this every few fetches so that we
    # don't lose too much data if we get interrupted
    if fetches % 50 == 0:
        with open(yf_save_file_path, 'w') as fp:
            json.dump(stock_data_YF, fp)

    time.sleep(1)

with open(yf_save_file_path, 'w') as fp:
    json.dump(stock_data_YF, fp)




