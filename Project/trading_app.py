import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Trading App",
    page_icon="📊",
    layout="wide"
)

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import pages - only import what exists
try:
    from pages import stock_analysis
    from pages import stock_prediction
    stock_analysis_exists = True
    stock_prediction_exists = True
except ImportError as e:
    st.warning(f"Some pages not found: {e}")
    stock_analysis_exists = False
    stock_prediction_exists = False



# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "CAPM Return", "CAPM Beta", "Stock Analysis", "Stock Prediction"]
)

# Home page
if page == "Home":
    st.title("Trading Guide App :bar_chart:")
    st.header("We Provide the Greatest platform for you to collect all information prior to investing in stocks.")

    # Image
    image_path = os.path.join(current_dir, "trading.image.webp")
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("⚠️ Image not found")
    
    st.markdown("## We Provide the following services:")
    st.markdown("1. Stock Information")
    st.write("Through this page, you can get all the information about the stock.")

    st.markdown("2. Stock Prediction")
    st.write("Explore predicted closing prices for the next 30 days based on historical data.")

    st.markdown("3. CAPM Return")
    st.write("Discover how CAPM calculates expected return of different stocks based on risk.")
    
    st.markdown("4. CAPM Beta")
    st.write("Calculates the Beta and expected return for individual stocks.")

# CAPM Return page
elif page == "CAPM Return":
    st.title("💰 CAPM Expected Return Calculator")
    st.markdown("### Calculate Expected Returns using CAPM")
    st.markdown("**Formula:** Expected Return = Risk-Free Rate + β × (Market Return - Risk-Free Rate)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        beta = st.number_input("Beta (β)", value=1.2, step=0.05, format="%.2f")
        risk_free_rate = st.number_input("Risk-Free Rate (%)", value=2.5, step=0.1) / 100
    
    with col2:
        market_return = st.number_input("Expected Market Return (%)", value=8.0, step=0.5) / 100
        calculate_btn = st.button("Calculate Expected Return", type="primary")
    
    if calculate_btn:
        expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
        
        st.success(f"### Expected Return: **{expected_return:.2%}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Premium", f"{expected_return - risk_free_rate:.2%}")
        with col2:
            st.metric("Market Risk Premium", f"{market_return - risk_free_rate:.2%}")

# CAPM Beta page - Built-in calculator (no external file needed)
elif page == "CAPM Beta":
    st.title("📈 CAPM Beta Calculator")
    st.markdown("""
    ### Calculate Beta Coefficient
    Beta measures stock volatility relative to the market.
    
    **Interpretation:**
    - **β > 1**: Stock is more volatile than the market
    - **β = 1**: Stock moves with the market
    - **β < 1**: Stock is less volatile than the market
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        stock_symbol = st.text_input("Stock Symbol", "AAPL").upper()
        period = st.selectbox("Time Period", ["1y", "2y", "3y", "5y"])
    
    with col2:
        market_symbol = st.text_input("Market Index", "^GSPC")
        calculate = st.button("📊 Calculate Beta", type="primary")
    
    if calculate:
        if not stock_symbol:
            st.error("Please enter a stock symbol")
        else:
            try:
                with st.spinner(f"Fetching data for {stock_symbol}..."):
                    # Download data
                    stock_data = yf.download(stock_symbol, period=period, progress=False, auto_adjust=False)
                    market_data = yf.download(market_symbol, period=period, progress=False, auto_adjust=False)
                    
                    if stock_data.empty:
                        st.error(f"No data found for {stock_symbol}")
                        st.stop()
                    
                    if market_data.empty:
                        st.error(f"No data found for {market_symbol}")
                        st.stop()
                    
                    # Get closing prices
                    if 'Close' in stock_data.columns:
                        stock_close = stock_data['Close']
                    else:
                        stock_close = stock_data.iloc[:, 0]
                    
                    if 'Close' in market_data.columns:
                        market_close = market_data['Close']
                    else:
                        market_close = market_data.iloc[:, 0]
                    
                    # Calculate returns
                    stock_returns = stock_close.pct_change().dropna()
                    market_returns = market_close.pct_change().dropna()
                    
                    # Align data
                    min_len = min(len(stock_returns), len(market_returns))
                    stock_returns = stock_returns.iloc[-min_len:]
                    market_returns = market_returns.iloc[-min_len:]
                    
                    # Calculate beta
                    covariance = np.cov(stock_returns, market_returns)[0][1]
                    variance = np.var(market_returns)
                    
                    if variance == 0:
                        st.error("Cannot calculate beta - market variance is zero")
                        st.stop()
                    
                    beta = covariance / variance
                    
                    # Calculate alpha
                    stock_annual_return = stock_returns.mean() * 252
                    market_annual_return = market_returns.mean() * 252
                    alpha = stock_annual_return - beta * market_annual_return
                    
                    # Calculate correlation
                    correlation = stock_returns.corr(market_returns)
                    
                    # Display results
                    st.success("✅ Beta Calculation Complete!")
                    
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
                        st.metric("R-Squared", f"{correlation**2:.4f}")
                    
                    # Interpretation
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
                        - Defensive stock that may hold up better in downturns
                        """)
                    
                    # Price Chart
                    st.subheader("📈 Price Comparison")
                    
                    # Normalize prices
                    stock_norm = stock_close / stock_close.iloc[0]
                    market_norm = market_close / market_close.iloc[0]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=stock_norm.index,
                        y=stock_norm,
                        mode='lines',
                        name=stock_symbol,
                        line=dict(color='blue', width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=market_norm.index,
                        y=market_norm,
                        mode='lines',
                        name=market_symbol,
                        line=dict(color='red', width=2, dash='dash')
                    ))
                    fig.update_layout(
                        title=f"Price Comparison (Normalized)",
                        xaxis_title="Date",
                        yaxis_title="Normalized Price (Base = 100%)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Risk Metrics
                    st.subheader("📊 Risk Metrics")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(f"{stock_symbol} Volatility (Annual)", f"{stock_returns.std() * np.sqrt(252):.2%}")
                        st.metric(f"Value at Risk (95%)", f"{np.percentile(stock_returns, 5):.2%}")
                    
                    with col2:
                        st.metric(f"{market_symbol} Volatility (Annual)", f"{market_returns.std() * np.sqrt(252):.2%}")
                        st.metric(f"Sharpe Ratio (Est.)", f"{(stock_annual_return - 0.025) / (stock_returns.std() * np.sqrt(252)):.2f}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write("Please check your internet connection and ticker symbols.")

# Stock Analysis page
elif page == "Stock Analysis":
    if stock_analysis_exists:
        try:
            stock_analysis.app()
        except Exception as e:
            st.error(f"Error loading Stock Analysis: {e}")
            st.info("Please make sure stock_analysis.py has an 'app()' function")
    else:
        st.error("Stock Analysis page not found. Please create pages/stock_analysis.py")

# Stock Prediction page
elif page == "Stock Prediction":
    if stock_prediction_exists:
        try:
            stock_prediction.app()
        except Exception as e:
            st.error(f"Error loading Stock Prediction: {e}")
            st.info("Please make sure stock_prediction.py has an 'app()' function")
    else:
        st.error("Stock Prediction page not found. Please create pages/stock_prediction.py")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("📊 **Trading App v1.0**\n\nData provided by Yahoo Finance")


with st.sidebar:
    st.markdown("# 📊 Time Series Analysis")
    st.markdown("---")
    
    # Project Info Section
    with st.expander("ℹ️ About Project", expanded=True):
        st.markdown("""
        **Project:** Time Series Forecasting & Analysis
        
        **Objective:** Analyze historical time series data and forecast future values with confidence intervals
        
        **Key Features:**
        - Interactive time series visualization
        - Automatic model selection
        - Future predictions with customizable horizons
        - Download forecast results
        """)
    
    
    # Feature Engineering Section
    with st.expander("⚙️ Feature Engineering"):
        st.markdown("""
        **Time-Based Features:**
        - Year, Month, Day, Quarter
        - Day of week, Week of year
        - Is weekend, Is holiday
        - Lag features (1,2,3,7,14,30 days)
        - Rolling statistics (mean, std, min, max)
        
        **Advanced Features:**
        - Fourier terms for seasonality
        - Calendar effects
        - External regressors
        """)
    
    
    # Developer Info Section
    with st.expander("👨‍💻 About the Developer"):
        st.markdown("""
        **👤 Jayesh Machha**  
        Data Scientist | Machine Learning | Data Analyst

        **Built with:**
        - Python, Pandas, NumPy
        - Statsmodels, Prophet
        - Scikit-learn for preprocessing
        - Streamlit for web interface
        - Jupyter Notebook for model development

        **📈 Time Series Project Features:**
        - Trend, seasonality, and residual decomposition
        - Stationarity testing (ADF test, KPSS test)
        - Auto-correlation analysis (ACF/PACF plots)
        - Models implemented:
          - ARIMA/SARIMA models
          - Facebook Prophet
          - Exponential Smoothing (Holt-Winters)
          - LSTM for deep learning approach
        - Model evaluation metrics: MAE, RMSE, MAPE
        - Future forecasting with confidence intervals

        **🔗 Connect with me:**
        - [LinkedIn](https://www.linkedin.com/in/jayesh-machha-166aa42b3/)
        - [GitHub](https://github.com/jayeshmachha)
        - 📧 machhajayesh@gmail.com
        """)

    st.markdown("---")
    st.caption("✨ Built with Streamlit | Time Series Analysis v1.0")
