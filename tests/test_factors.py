import unittest
import pandas as pd
import numpy as np
from strategies.factors import momentum_factor

class TestFactors(unittest.TestCase):
    def setUp(self):
        prices = pd.Series([100, 105, 110, 115, 120], 
                          index=pd.date_range('2023-01-01', periods=5))
        self.prices = pd.DataFrame({'AAPL': prices})
        
    def test_momentum_factor(self):
        momentum = momentum_factor(self.prices, window=2)
        expected = pd.Series([np.nan, np.nan, 0.1, 0.0952, 0.0909], 
                             index=self.prices.index).round(4)
        pd.testing.assert_series_equal(momentum['AAPL'].round(4), expected)
        
    # Tests for other factors...

if __name__ == '__main__':
    unittest.main()