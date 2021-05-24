from qiskit.finance.data_providers import RandomDataProvider
import datetime
import numpy as np
import yfinance as yf
import math 

def get_random_stock_market_data_final(num_assets_total):
    data= RandomDataProvider([0]*num_assets_total,
    start=datetime.datetime(2016,1,1),
    end=datetime.datetime(2016,1,30))
    data.run() 
    mu = np.array(data.get_period_return_mean_vector())
    sigma =data.get_period_return_covariance_matrix()
    return mu,sigma

def check_no_data(stocks,mu):
    no_data_tickers = []
    for i in range(len(stocks)):
        if math.isnan(mu[i]):
            no_data_tickers.append(stocks[i]) 
    if no_data_tickers:
        raise NoDataAvailable("No data for tickers: " + ''.join(no_data_tickers))

class IncompatibleArguments(Exception):
    pass

class NoDataAvailable(Exception):
    pass

