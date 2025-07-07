import numpy as np

def calculate_metrics(returns):
    """Compute key performance metrics"""
    cumulative = (1 + returns).cumprod()
    
    metrics = {
        'cagr': (cumulative.iloc[-1] ** (252/len(returns))) - 1,
        'sharpe': returns.mean() / returns.std() * np.sqrt(252),
        'max_drawdown': (cumulative / cumulative.cummax() - 1).min(),
        'turnover': None  # Placeholder for actual calculation
    }
    return metrics