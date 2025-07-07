import pandas as pd

class MultiFactorStrategy:
    def __init__(self, factor_weights, top_n=50):
        self.weights = factor_weights
        self.top_n = top_n
        
    def generate_signals(self, date, factor_data):
        # Get latest factor values
        current_factors = factor_data.xs(date, level='date')
        
        # Normalize and combine factors
        normalized = current_factors.groupby('date').transform(
            lambda x: (x - x.mean()) / x.std()
        )
        combined = (normalized * pd.Series(self.weights)).sum(axis=1)
        
        # Select top assets
        selected = combined.nlargest(self.top_n)
        
        # Equal weight portfolio
        return selected / selected.sum()