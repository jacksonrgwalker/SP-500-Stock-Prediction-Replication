# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 02:50:39 2020

@author: zhong
"""
###############################################################################
'load api data'
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
assert load_dotenv(), "Failed to load .env file"
##########################################
import json
import time
from tqdm import tqdm
##################################
import sys, os
from pathlib import Path
project_dir = Path.cwd()
os.chdir(project_dir)
sys.path.append(os.getcwd())
#os.chdir('change to the mother working directory')

save_file_path = Path('data/1-ticker_name_list.json')
with open(save_file_path, 'r') as fp:
    _stock = json.load(fp)
tickers = list( _stock.keys() )

###############################################################################
ts = TimeSeries()

stock_data_AV = {}
#stock_data_AV  = json.loads(open('data\\stock_data_AV.json').read())

'load individual stock data for companies on list'
for stock in tqdm( tickers ):
    if stock not in stock_data_AV.keys():
        _data, _meta_data = ts.get_daily_adjusted(symbol = stock, outputsize = 'full')
        stock_data_AV[stock] = _data        
        time.sleep(1)

'save data'
save_file_path = Path('data/stock_data_AV.json')
with open(save_file_path, 'w') as fp:
    json.dump(stock_data_AV, fp)



