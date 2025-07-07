import streamlit as st
import plotly.express as px
import pandas as pd
from strategies.scoring import combine_factors

# Load precomputed results
backtest_results = pd.read_parquet('data/processed/backtest_results.parquet')
factor_data = pd.read_parquet('data/processed/factor_scores.parquet')

st.title("Multi-Factor Quant Dashboard")

# Factor weight controls
weights = {}
cols = st.columns(5)
with cols[0]: weights['momentum'] = st.slider("Momentum", 0.0, 1.0, 0.2)
with cols[1]: weights['value'] = st.slider("Value", 0.0, 1.0, 0.2)
with cols[2]: weights['quality'] = st.slider("Quality", 0.0, 1.0, 0.2)
with cols[3]: weights['volatility'] = st.slider("Volatility", 0.0, 1.0, 0.2)
with cols[4]: weights['size'] = st.slider("Size", 0.0, 1.0, 0.2)

# Re-run scoring with new weights
combined_score = combine_factors(factor_data, weights)

# Performance comparison
st.subheader("Performance vs Benchmark")
fig = px.line(backtest_results, x='date', y=['portfolio', 'SPY'], 
              title="Cumulative Returns")
st.plotly_chart(fig)

# Factor correlation heatmap
st.subheader("Factor Correlation")
corr_matrix = factor_data.groupby('date').corr().groupby(level=1).mean()
fig = px.imshow(corr_matrix, text_auto=True)
st.plotly_chart(fig)

# Portfolio holdings
st.subheader("Current Portfolio")
top_holdings = combined_score.nlargest(20).reset_index()
st.dataframe(top_holdings)

# Download report
st.download_button("Download Report", 
                   data=backtest_results.to_csv().encode('utf-8'),
                   file_name='factor_report.csv')