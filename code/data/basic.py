from qiskit.finance.data_providers import YahooDataProvider
import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

def get_data_qiskit_yahoo(tickers,start,end):
    data= YahooDataProvider(tickers,start,end)
    data.run() 
    mu = np.array(data.get_period_return_mean_vector())
    sigma =data.get_period_return_covariance_matrix()
    return mu,sigma    

def get_data_pd(tickers,start,end):
    returns = []
    sectors = []
    for ticker in tickers:
        returns.append(web.DataReader(ticker,'yahoo',start,end)['Close'])
        """ stock =yf.Ticker(ticker)
        print(stock.sustainability) """
    returns = pd.concat(returns,axis=1)
    returns.columns = tickers


    log_returns = np.log(returns/returns.shift(1)) #log(P_t/P_{t-1})
    log_returns = log_returns.iloc[1:] #Remove nan line
    log_returns_anual = log_returns*252
    mean_log_returns = 250*log_returns.mean() #get mean
    sigma = 250*log_returns.cov().to_numpy()
    mu = mean_log_returns.to_numpy()
    mu = mu#252*mu
    #sigma = (sigma/2)#2.52*((100*sigma/2)**(1/2))
    return mu,sigma

def get_data(tickers=None, start =None ,end = None):
    data = get_data_pd(tickers,start,end)
    
    return data

