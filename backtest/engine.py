import pandas as pd

class Backtester:
    def __init__(self, data_handler, rebalance_freq='M'):
        self.data = data_handler
        self.rebalance_freq = rebalance_freq
    
    def run_backtest(self, strategy, initial_capital=1000000):
        # Get rebalance dates
        all_dates = pd.date_range(
            start=self.data.prices.index.min(),
            end=self.data.prices.index.max(),
            freq=self.rebalance_freq
        )
        
        portfolio = pd.Series(index=all_dates, dtype=object)
        capital = initial_capital
        
        for date in all_dates:
            # Get strategy signals
            weights = strategy.generate_signals(date)
            
            # Execute trades
            prices = self.data.get_prices(date)
            position_size = capital * weights / prices
            
            # Track portfolio
            portfolio.at[date] = position_size
            
            # Update capital (simulate holding until next rebalance)
            next_date = all_dates[all_dates > date][0] if any(all_dates > date) else all_dates[-1]
            returns = self.data.get_returns(date, next_date)
            capital = (position_size * (1 + returns)).sum()
        
        return portfolio