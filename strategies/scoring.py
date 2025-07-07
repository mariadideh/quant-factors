from scipy.stats import zscore
import pandas as pd

def normalize_factors(factor_df):
    """Z-score normalization by date"""
    return factor_df.groupby(level='date').transform(zscore)

def combine_factors(factor_dict, weights):
    """
    Combine factors with weights
    
    Args:
        factor_dict: {'factor_name': DataFrame}
        weights: {'factor_name': weight_value}
    """
    combined = pd.DataFrame(index=factor_dict[list(factor_dict.keys())[0]].index)
    
    for factor, df in factor_dict.items():
        if factor in weights:
            combined[factor] = df * weights[factor]
    
    return combined.sum(axis=1).to_frame('combined_score')

def rank_assets(scores, top_n=50):
    """Rank assets and select top N"""
    return scores.groupby('date').apply(
        lambda x: x.nlargest(top_n, 'combined_score')
    ).reset_index(level=0, drop=True)