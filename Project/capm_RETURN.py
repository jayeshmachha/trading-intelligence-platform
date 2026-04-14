import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader as web
import sys
import os

# Add utils to path
utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Utils')
sys.path.insert(0, utils_path)

import capm_functions

def app():
    """CAPM Return Calculator Page"""
    
    st.title("💰 Capital Asset Pricing Model (CAPM) - Expected Return")
    st.markdown("""
    ### Calculate Expected Returns using CAPM
    **Formula:** Expected Return = Risk-Free Rate + Beta × (Market Return - Risk-Free Rate)
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        stock_list = st.multiselect(
            "Choose stocks for analysis",
            ('TSLA', 'META', 'AMZN', 'AAPL', 'NFLX', 'MSFT', 'NVDA', 'GOOGL', 'MGM', 'JPM', 'BAC', 'WMT'),
            help="Select up to 4 stocks"
        )
    
    with col2:
        year = st.number_input("Number of years for historical data", min_value=1, max_value=10, value=2, step=1)
        
    # Risk-free rate input
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        risk_free_rate = st.number_input(
            "Risk-Free Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.5,
            step=0.1,
            help="Typically 10-year Treasury bond yield"
        ) / 100
    
    # Validation
    if len(stock_list) == 0:
        st.warning("⚠️ Please select at least 1 stock to continue.")
        st.stop()
    
    if len(stock_list) > 4:
        st.warning("⚠️ Please select maximum 4 stocks only.")
        st.stop()
    
    try:
        with st.spinner("Fetching market data..."):
            end = datetime.date.today()
            start = datetime.date(
                datetime.date.today().year - int(year),
                datetime.date.today().month,
                datetime.date.today().day
            )
            
            # Fetch S&P 500 data
            st.info("📊 Fetching S&P 500 data...")
            SP500 = web.DataReader(['sp500'], 'fred', start, end)
            SP500 = SP500.rename(columns={SP500.columns[0]: 'sp500'})
            SP500['Date'] = SP500.index
            SP500.reset_index(drop=True, inplace=True)
            SP500['Date'] = pd.to_datetime(SP500['Date'])
            
            # Fetch stock data
            st.info(f"📈 Fetching data for {', '.join(stock_list)}...")
            data = yf.download(stock_list, period=f'{int(year)}y', progress=False)
            stock_df = data['Close'].reset_index()
            stock_df.columns.name = None
            stock_df['Date'] = pd.to_datetime(stock_df['Date'])
            
            # Merge data
            stock_df = pd.merge(stock_df, SP500, on='Date', how='inner')
            
            # Display data preview
            st.markdown("### 📊 Data Preview")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**First 5 rows**")
                st.dataframe(stock_df.head(), use_container_width=True)
            with col2:
                st.markdown("**Last 5 rows**")
                st.dataframe(stock_df.tail(), use_container_width=True)
            
            # Price charts
            st.markdown("### 📈 Stock Price Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Actual Prices**")
                st.plotly_chart(capm_functions.interactive_plot(stock_df), use_container_width=True)
            
            with col2:
                st.markdown("**Normalized Prices (Base = 1)**")
                normalized_df = capm_functions.normalize(stock_df)
                st.plotly_chart(capm_functions.interactive_plot(normalized_df), use_container_width=True)
            
            # Calculate daily returns
            st.markdown("### 📉 Returns Analysis")
            stock_daily_return = capm_functions.daily_return(stock_df)
            
            # Calculate beta for each stock
            beta_dict = {}
            alpha_dict = {}
            
            for stock in stock_list:
                if stock in stock_daily_return.columns:
                    # Use updated calculate_beta that returns 4 values
                    result = capm_functions.calculate_beta(stock_daily_return, stock)
                    
                    if result[0] is not None:
                        beta_dict[stock] = result[0]  # beta
                        alpha_dict[stock] = result[1]  # alpha
                    else:
                        beta_dict[stock] = None
                        alpha_dict[stock] = None
            
            # Calculate market return (annualized)
            market_return = stock_daily_return['sp500'].mean() * 252
            
            # Display beta values
            beta_df = pd.DataFrame(columns=['Stock', 'Beta Value', 'Risk Classification'])
            beta_df['Stock'] = list(beta_dict.keys())
            
            beta_values = []
            classifications = []
            
            for stock, beta_val in beta_dict.items():
                if beta_val is not None:
                    beta_values.append(f"{beta_val:.3f}")
                    # Classify beta
                    if beta_val > 1.2:
                        classifications.append("🔴 High Risk (Aggressive)")
                    elif beta_val > 0.8:
                        classifications.append("🟡 Moderate Risk")
                    elif beta_val > 0.5:
                        classifications.append("🟢 Low Risk (Defensive)")
                    else:
                        classifications.append("⚪ Very Low Risk")
                else:
                    beta_values.append("N/A")
                    classifications.append("⚠️ Unable to calculate")
            
            beta_df['Beta Value'] = beta_values
            beta_df['Risk Classification'] = classifications
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Calculated Beta Values")
                st.dataframe(beta_df, use_container_width=True)
                
                # Beta interpretation
                st.info("""
                **Beta Interpretation:**
                - **β > 1**: Stock is more volatile than market
                - **β = 1**: Stock moves with market
                - **β < 1**: Stock is less volatile than market
                """)
            
            # Calculate expected returns using CAPM
            expected_returns = []
            
            for stock, beta_val in beta_dict.items():
                if beta_val is not None:
                    expected_return = risk_free_rate + beta_val * (market_return - risk_free_rate)
                    expected_returns.append(f"{expected_return:.2%}")
                else:
                    expected_returns.append("N/A")
            
            return_df = pd.DataFrame()
            return_df['Stock'] = list(beta_dict.keys())
            return_df['Beta'] = beta_values
            return_df['Expected Return (CAPM)'] = expected_returns
            
            with col2:
                st.markdown("### 💰 Calculated Expected Returns (CAPM)")
                st.dataframe(return_df, use_container_width=True)
                
                # Display market metrics
                st.metric(
                    "Market Return (Annualized)",
                    f"{market_return:.2%}",
                    help=f"Based on S&P 500 {year}-year average return"
                )
                st.metric(
                    "Risk-Free Rate",
                    f"{risk_free_rate:.2%}",
                    help="Input rate"
                )
            
            # Detailed analysis for each stock
            st.markdown("### 📈 Detailed Stock Analysis")
            
            for stock in stock_list:
                if stock in beta_dict and beta_dict[stock] is not None:
                    with st.expander(f"🔍 {stock} - Detailed Analysis"):
                        beta_val = beta_dict[stock]
                        alpha_val = alpha_dict[stock]
                        expected_return = risk_free_rate + beta_val * (market_return - risk_free_rate)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Beta", f"{beta_val:.3f}")
                        with col2:
                            st.metric("Alpha", f"{alpha_val:.4%}" if alpha_val else "N/A")
                        with col3:
                            st.metric("Expected Return", f"{expected_return:.2%}")
                        with col4:
                            excess_return = expected_return - market_return
                            st.metric("vs Market", f"{excess_return:+.2%}")
                        
                        # Risk assessment
                        st.write("**Risk Assessment:**")
                        if beta_val > 1.2:
                            st.warning(f"⚠️ {stock} is an aggressive stock ({beta_val:.2f}× market volatility)")
                        elif beta_val > 0.8:
                            st.info(f"📊 {stock} has average market risk ({beta_val:.2f}× market volatility)")
                        else:
                            st.success(f"✅ {stock} is a defensive stock ({beta_val:.2f}× market volatility)")
                        
                        # Recommendation based on expected return
                        if expected_return > market_return * 1.2:
                            st.success(f"💡 **Recommendation:** STRONG BUY - Expected to outperform market significantly")
                        elif expected_return > market_return:
                            st.info(f"💡 **Recommendation:** BUY - Expected to outperform market")
                        elif expected_return > risk_free_rate:
                            st.warning(f"💡 **Recommendation:** HOLD - Expected to underperform market but beat risk-free rate")
                        else:
                            st.error(f"💡 **Recommendation:** AVOID - Expected to underperform risk-free rate")
            
            # Security Market Line Plot
            st.markdown("### 📊 Security Market Line (SML)")
            
            # Prepare data for SML
            sml_data = []
            for stock, beta_val in beta_dict.items():
                if beta_val is not None:
                    expected_return = risk_free_rate + beta_val * (market_return - risk_free_rate)
                    sml_data.append({
                        'Stock': stock,
                        'Beta': beta_val,
                        'Expected Return': expected_return
                    })
            
            if sml_data:
                sml_df = pd.DataFrame(sml_data)
                
                # Create SML plot
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                # SML line
                beta_range = [0, max(2, max(sml_df['Beta']) + 0.5)]
                return_range = [
                    risk_free_rate,
                    risk_free_rate + beta_range[1] * (market_return - risk_free_rate)
                ]
                
                fig.add_trace(go.Scatter(
                    x=beta_range,
                    y=return_range,
                    mode='lines',
                    name='Security Market Line',
                    line=dict(color='blue', width=2, dash='dash')
                ))
                
                # Market point
                fig.add_trace(go.Scatter(
                    x=[1],
                    y=[market_return],
                    mode='markers',
                    name='Market (S&P 500)',
                    marker=dict(size=15, color='green', symbol='star')
                ))
                
                # Stock points
                fig.add_trace(go.Scatter(
                    x=sml_df['Beta'],
                    y=sml_df['Expected Return'],
                    mode='markers+text',
                    name='Stocks',
                    text=sml_df['Stock'],
                    textposition='top center',
                    marker=dict(size=12, color='red', symbol='circle')
                ))
                
                fig.update_layout(
                    title="Security Market Line (SML)",
                    xaxis_title="Beta (β)",
                    yaxis_title="Expected Return",
                    xaxis=dict(tickmode='linear', tick0=0, dtick=0.5),
                    yaxis=dict(tickformat='.0%'),
                    hovermode='closest',
                    plot_bgcolor='white',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Disclaimer
            st.markdown("---")
            st.caption("""
            ⚠️ **Disclaimer:** This analysis is for educational purposes only. 
            Past performance does not guarantee future results. Always conduct your own research 
            before making investment decisions. CAPM has limitations and may not accurately predict 
            future returns.
            """)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check:")
        st.write("1. Your internet connection")
        st.write("2. Stock ticker symbols are correct")
        st.write("3. Date range is valid")
        st.write(f"Error details: {type(e).__name__}: {e}")

# For direct testing
if __name__ == "__main__":
    app()