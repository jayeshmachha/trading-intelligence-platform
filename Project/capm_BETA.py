import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def app():
    """CAPM Beta Calculator Page - Fixed Version"""
    
    st.title("📈 CAPM Beta Calculator")
    st.markdown("""
    ### Calculate Beta Coefficient for Any Stock
    Beta measures the volatility of a stock relative to the market.
    
    **Interpretation:**
    - **β > 1**: Stock is more volatile than the market
    - **β = 1**: Stock moves with the market
    - **β < 1**: Stock is less volatile than the market
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        stock_symbol = st.text_input("Stock Symbol", "AAPL", key="beta_stock").upper()
        period = st.selectbox("Time Period", ["1y", "2y", "3y", "5y"], key="beta_period")
    
    with col2:
        market_options = {
            "^GSPC": "S&P 500",
            "^IXIC": "NASDAQ",
            "^DJI": "Dow Jones",
            "^FTSE": "FTSE 100"
        }
        market_choice = st.selectbox(
            "Market Index",
            list(market_options.keys()),
            format_func=lambda x: f"{x} ({market_options[x]})",
            key="beta_market"
        )
        calculate = st.button("📊 Calculate Beta", type="primary", key="beta_calc")
    
    if calculate:
        if not stock_symbol:
            st.error("Please enter a stock symbol")
            return
        
        try:
            with st.spinner(f"Fetching data for {stock_symbol}..."):
                # Download data with progress=False to avoid warnings
                stock_data = yf.download(stock_symbol, period=period, progress=False, auto_adjust=False)
                market_data = yf.download(market_choice, period=period, progress=False, auto_adjust=False)
                
                # Check if data is empty
                if stock_data.empty:
                    st.error(f"No data found for {stock_symbol}. Please check the symbol.")
                    return
                
                if market_data.empty:
                    st.error(f"No data found for {market_choice}. Please check the symbol.")
                    return
                
                # Extract closing prices - FIXED: Handle different column names
                # For stock data
                if 'Adj Close' in stock_data.columns:
                    stock_close = stock_data['Adj Close']
                elif 'Close' in stock_data.columns:
                    stock_close = stock_data['Close']
                else:
                    # Try to get the first column
                    stock_close = stock_data.iloc[:, 0]
                
                # For market data
                if 'Adj Close' in market_data.columns:
                    market_close = market_data['Adj Close']
                elif 'Close' in market_data.columns:
                    market_close = market_data['Close']
                else:
                    market_close = market_data.iloc[:, 0]
                
                # Ensure they are Series
                if isinstance(stock_close, pd.DataFrame):
                    stock_close = stock_close.iloc[:, 0]
                if isinstance(market_close, pd.DataFrame):
                    market_close = market_close.iloc[:, 0]
                
                # Remove NaN values
                stock_close = stock_close.dropna()
                market_close = market_close.dropna()
                
                if len(stock_close) < 10 or len(market_close) < 10:
                    st.error("Not enough data points. Please try a different time period.")
                    return
                
                # Calculate daily returns
                stock_returns = stock_close.pct_change().dropna()
                market_returns = market_close.pct_change().dropna()
                
                # Align the data
                combined = pd.DataFrame({
                    'stock': stock_returns,
                    'market': market_returns
                }).dropna()
                
                if len(combined) < 10:
                    st.error("Not enough overlapping data points. Please try a different time period.")
                    return
                
                # Calculate Beta
                covariance = np.cov(combined['stock'], combined['market'])[0][1]
                variance = np.var(combined['market'])
                
                if variance == 0:
                    st.error("Market variance is zero. Cannot calculate beta.")
                    return
                
                beta = covariance / variance
                
                # Calculate Alpha (annualized)
                stock_annual_return = combined['stock'].mean() * 252
                market_annual_return = combined['market'].mean() * 252
                alpha = stock_annual_return - beta * market_annual_return
                
                # Calculate Correlation
                correlation = combined['stock'].corr(combined['market'])
                r_squared = correlation ** 2
                
                # Calculate Volatility
                stock_volatility = combined['stock'].std() * np.sqrt(252)
                market_volatility = combined['market'].std() * np.sqrt(252)
                
                # Display Results
                st.success("✅ Beta Calculation Complete!")
                
                # Main Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Beta (β)", f"{beta:.4f}")
                    if beta > 1.2:
                        st.error("🔴 High Risk")
                    elif beta > 0.8:
                        st.warning("🟡 Moderate Risk")
                    else:
                        st.success("🟢 Low Risk")
                
                with col2:
                    st.metric("Alpha (α)", f"{alpha:.4%}")
                
                with col3:
                    st.metric("Correlation", f"{correlation:.4f}")
                
                with col4:
                    st.metric("R-Squared", f"{r_squared:.4f}")
                
                # Beta Interpretation
                st.markdown("---")
                st.subheader("📊 Beta Interpretation")
                
                if beta > 1.5:
                    st.error(f"""
                    **{stock_symbol} is a VERY HIGH VOLATILITY stock**
                    - Beta: {beta:.3f}
                    - {beta:.2f}× more volatile than the market
                    - Expect large price swings
                    """)
                elif beta > 1.0:
                    st.warning(f"""
                    **{stock_symbol} is a HIGH VOLATILITY stock**
                    - Beta: {beta:.3f}
                    - {beta:.2f}× more volatile than the market
                    - Stock amplifies market movements
                    """)
                elif beta > 0.8:
                    st.info(f"""
                    **{stock_symbol} has MODERATE volatility**
                    - Beta: {beta:.3f}
                    - Moves roughly in line with the market
                    """)
                elif beta > 0.5:
                    st.success(f"""
                    **{stock_symbol} is a LOW VOLATILITY stock**
                    - Beta: {beta:.3f}
                    - {(1-beta)*100:.0f}% less volatile than market
                    """)
                else:
                    st.success(f"""
                    **{stock_symbol} is a VERY LOW VOLATILITY stock**
                    - Beta: {beta:.3f}
                    - {(1-beta)*100:.0f}% less volatile than market
                    - Defensive stock
                    """)
                
                # Price Chart
                st.subheader("📈 Price Comparison")
                
                # Normalize prices
                stock_norm = stock_close / stock_close.iloc[0]
                market_norm = market_close / market_close.iloc[0]
                
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=stock_norm.index,
                    y=stock_norm,
                    mode='lines',
                    name=stock_symbol,
                    line=dict(color='blue', width=2)
                ))
                fig1.add_trace(go.Scatter(
                    x=market_norm.index,
                    y=market_norm,
                    mode='lines',
                    name=market_choice,
                    line=dict(color='red', width=2, dash='dash')
                ))
                fig1.update_layout(
                    title=f"{stock_symbol} vs Market (Normalized)",
                    xaxis_title="Date",
                    yaxis_title="Normalized Price (Base = 100%)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig1, use_container_width=True, key="beta_price_chart")
                
                # Returns Scatter Plot
                st.subheader("📊 Returns Scatter Plot")
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=combined['market'],
                    y=combined['stock'],
                    mode='markers',
                    name='Daily Returns',
                    marker=dict(size=5, color='blue', opacity=0.6)
                ))
                
                # Add regression line
                x_line = np.array([combined['market'].min(), combined['market'].max()])
                y_line = alpha/252 + beta * x_line  # Convert alpha back to daily
                fig2.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode='lines',
                    name=f'Regression (β = {beta:.3f})',
                    line=dict(color='red', width=2, dash='dash')
                ))
                
                fig2.update_layout(
                    title=f"{stock_symbol} vs Market Returns",
                    xaxis_title=f"{market_choice} Daily Returns",
                    yaxis_title=f"{stock_symbol} Daily Returns",
                    height=400,
                    hovermode='closest'
                )
                st.plotly_chart(fig2, use_container_width=True, key="beta_scatter_chart")
                
                # Volatility Metrics
                st.subheader("📊 Volatility Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(f"{stock_symbol} Annual Volatility", f"{stock_volatility:.2%}")
                    st.metric("Daily VaR (95%)", f"{np.percentile(combined['stock'], 5):.2%}")
                
                with col2:
                    st.metric(f"{market_choice} Annual Volatility", f"{market_volatility:.2%}")
                    st.metric("Information Ratio", f"{(stock_annual_return - market_annual_return) / stock_volatility:.2f}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please check:")
            st.write("1. Stock ticker symbol is correct (e.g., AAPL, TSLA, MSFT)")
            st.write("2. Market index symbol is valid (e.g., ^GSPC for S&P 500)")
            st.write("3. Your internet connection is active")
            st.write(f"Error details: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    app()