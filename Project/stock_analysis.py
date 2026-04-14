import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np 
import plotly.graph_objects as go
import datetime
import sys
import os

# Add utils to path
utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils')
sys.path.insert(0, utils_path)

try:
    from plotly_figure import plotly_table
except ImportError:
    def plotly_table(df):
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
            cells=dict(values=[df[col] for col in df.columns], fill_color='lavender', align='left')
        )])
        fig.update_layout(height=400)
        return fig

def app():
    """Main function for Stock Analysis page"""
    
    st.title("📊 Stock Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    today = datetime.date.today()
    
    with col1:
        ticker = st.text_input("Stock Ticker", "AAPL", key="stock_ticker").upper()
    with col2:
        start_date = st.date_input("Start Date", today - datetime.timedelta(days=180), key="start_date")
    with col3:
        end_date = st.date_input("End Date", today, key="end_date")
    
    if not ticker:
        st.warning("⚠️ Please enter a stock ticker")
        return
    
    st.subheader(f"📈 {ticker} Analysis")
    
    try:
        with st.spinner(f"Fetching data for {ticker}..."):
            # Download data
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            
            if data.empty:
                st.error(f"No data found for {ticker}. Please check the ticker symbol.")
                return
            
            # Handle multi-index columns
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # Display current price
            current_price = data['Close'].iloc[-1]
            prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
            price_change = current_price - prev_close
            price_change_pct = (price_change / prev_close) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"${current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
            with col2:
                st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
            with col3:
                st.metric("High (Today)", f"${data['High'].iloc[-1]:.2f}")
            with col4:
                st.metric("Low (Today)", f"${data['Low'].iloc[-1]:.2f}")
            
            # Company Info
            with st.expander("📄 Company Information", expanded=False):
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if info:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                        st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A'):,}" if info.get('fullTimeEmployees') else "N/A")
                    with col2:
                        st.write(f"**Market Cap:** ${info.get('marketCap', 0):,.0f}" if info.get('marketCap') else "N/A")
                        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                        st.write(f"**Beta:** {info.get('beta', 'N/A')}")
                    
                    st.write("**Business Summary:**")
                    st.write(info.get('longBusinessSummary', 'N/A')[:500] + "...")
            
            # Create Price Chart - FIXED
            st.subheader("📈 Price Chart")
            
            fig_price = go.Figure()
            
            # Add candlestick chart
            fig_price.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color='green',
                decreasing_line_color='red'
            ))
            
            fig_price.update_layout(
                title=f"{ticker} Stock Price",
                yaxis_title="Price (USD)",
                xaxis_title="Date",
                template="plotly_white",
                height=500,
                xaxis_rangeslider_visible=True,
                xaxis_rangeslider_thickness=0.05
            )
            
            st.plotly_chart(fig_price, use_container_width=True, key="price_chart")
            
            # Volume Chart - FIXED
            st.subheader("📊 Trading Volume")
            
            fig_volume = go.Figure()
            
            # Color volume bars based on price movement
            colors = ['green' if data['Close'].iloc[i] >= data['Open'].iloc[i] else 'red' 
                     for i in range(len(data))]
            
            fig_volume.add_trace(go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ))
            
            fig_volume.update_layout(
                title=f"{ticker} Trading Volume",
                yaxis_title="Volume",
                xaxis_title="Date",
                template="plotly_white",
                height=300
            )
            
            st.plotly_chart(fig_volume, use_container_width=True, key="volume_chart")
            
            # Moving Averages - FIXED
            st.subheader("📊 Moving Averages")
            
            # Calculate moving averages
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data['MA200'] = data['Close'].rolling(window=200).mean()
            
            fig_ma = go.Figure()
            
            # Add close price
            fig_ma.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='blue', width=2)
            ))
            
            # Add moving averages
            fig_ma.add_trace(go.Scatter(
                x=data.index,
                y=data['MA20'],
                mode='lines',
                name='20-day MA',
                line=dict(color='orange', width=1.5)
            ))
            
            fig_ma.add_trace(go.Scatter(
                x=data.index,
                y=data['MA50'],
                mode='lines',
                name='50-day MA',
                line=dict(color='red', width=1.5)
            ))
            
            if not data['MA200'].isna().all():
                fig_ma.add_trace(go.Scatter(
                    x=data.index,
                    y=data['MA200'],
                    mode='lines',
                    name='200-day MA',
                    line=dict(color='purple', width=1.5, dash='dash')
                ))
            
            fig_ma.update_layout(
                title=f"{ticker} Moving Averages",
                yaxis_title="Price (USD)",
                xaxis_title="Date",
                template="plotly_white",
                height=450,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_ma, use_container_width=True, key="ma_chart")
            
            # Historical Data Table - FIXED
            st.subheader("📋 Historical Data (Last 10 days)")
            
            last_10 = data.tail(10).sort_index(ascending=False)
            display_df = last_10.copy()
            
            # Format for display
            for col in ['Open', 'High', 'Low', 'Close']:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")
            
            display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:,.0f}")
            
            # Create table
            fig_table = go.Figure(data=[go.Table(
                header=dict(
                    values=list(display_df.columns),
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=12)
                ),
                cells=dict(
                    values=[display_df.index.strftime('%Y-%m-%d')] + [display_df[col] for col in display_df.columns],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=11)
                )
            )])
            
            fig_table.update_layout(height=400)
            st.plotly_chart(fig_table, use_container_width=True, key="data_table")
            
            # Statistics
            st.subheader("📊 Price Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Mean Price", f"${data['Close'].mean():.2f}")
                st.metric("Median Price", f"${data['Close'].median():.2f}")
            
            with col2:
                st.metric("Std Deviation", f"${data['Close'].std():.2f}")
                st.metric("Volatility (Annual)", f"{data['Close'].pct_change().std() * np.sqrt(252):.2%}")
            
            with col3:
                st.metric("52-Week High", f"${data['Close'].max():.2f}")
                st.metric("52-Week Low", f"${data['Close'].min():.2f}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.write("Please check your internet connection and ticker symbol.")

if __name__ == "__main__":
    app()