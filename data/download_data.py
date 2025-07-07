import yfinance as yf
import pandas as pd
import numpy as np

def download_data(tickers, start_date, end_date):
    prices = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    fundamentals = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        # Get fundamental data (simplified)
        pe = stock.info.get('trailingPE', np.nan)
        pb = stock.info.get('priceToBook', np.nan)
        roe = stock.info.get('returnOnEquity', np.nan)
        debt_equity = stock.info.get('debtToEquity', np.nan)
        mcap = stock.info.get('marketCap', np.nan)
        
        fundamentals[ticker] = {
            'pe_ratio': pe,
            'pb_ratio': pb,
            'roe': roe,
            'debt_to_equity': debt_equity,
            'market_cap': mcap
        }
    
    return prices, pd.DataFrame(fundamentals).T