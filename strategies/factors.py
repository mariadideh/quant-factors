import numpy as np
import pandas as pd

def momentum_factor(prices, window=126):
    return prices.pct_change(periods=window)

def value_factor(fundamentals):
    pe = 1 / fundamentals['pe_ratio']
    pb = 1 / fundamentals['pb_ratio']
    return (pe.fillna(0) + pb.fillna(0)) / 2

def quality_factor(fundamentals):
    roe = fundamentals['roe']
    debt_equity = 1 / (1 + fundamentals['debt_to_equity'])
    return (roe.fillna(0) + debt_equity.fillna(0)) / 2

def volatility_factor(prices, window=63):
    return prices.pct_change().rolling(window).std()

def size_factor(market_cap):
    return np.log(market_cap).replace(-np.inf, np.nan)