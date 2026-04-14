import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

def simple_forecast(data, days=30):
    """Simple linear regression forecast"""
    try:
        if len(data) < 30:
            return None
        
        # Create time index
        x = np.arange(len(data))
        y = data['Close'].values
        
        # Linear regression
        coeffs = np.polyfit(x, y, 1)
        p = np.poly1d(coeffs)
        
        # Forecast future
        future_x = np.arange(len(data), len(data) + days)
        forecast_values = p(future_x)
        
        # Create forecast dates
        last_date = data.index[-1]
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days, freq='B')
        
        # Calculate confidence intervals
        residuals = y - p(x)
        std_error = np.std(residuals)
        
        forecast_df = pd.DataFrame({
            'Close': forecast_values,
            'Lower Bound': forecast_values - 1.96 * std_error,
            'Upper Bound': forecast_values + 1.96 * std_error
        }, index=future_dates)
        
        return forecast_df
    except Exception as e:
        st.error(f"Forecast error: {e}")
        return None

def app():
    """Main function for Stock Prediction page"""
    
    st.title("🤖 Stock Price Prediction")
    st.markdown("Predict next 30 days closing prices using linear regression")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input('Stock Ticker', 'AAPL', key="pred_ticker").upper()
    
    with col2:
        days = st.slider('Days to Predict', 7, 90, 30, key="pred_days")
    
    predict_button = st.button('🚀 Predict Future Prices', type='primary', use_container_width=True)
    
    if not predict_button:
        st.info('👈 Enter a stock ticker and click "Predict Future Prices" to see the forecast')
        return
    
    try:
        with st.spinner(f'Fetching data for {ticker}...'):
            # Fetch historical data - 2 years for better trend
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365*2)
            
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            
            if data.empty:
                st.error(f'No data found for {ticker}. Please check the symbol.')
                return
            
            # Handle column names
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # Display current info
            current_price = data['Close'].iloc[-1]
            st.subheader(f'📈 {ticker} - Current Price: ${current_price:.2f}')
            
            # Historical Price Chart - FIXED
            st.subheader("Historical Price Data")
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Historical Price',
                line=dict(color='blue', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.1)'
            ))
            
            fig_hist.update_layout(
                title=f'{ticker} - Historical Price (Last 2 Years)',
                xaxis_title='Date',
                yaxis_title='Price (USD)',
                template='plotly_white',
                height=450,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_hist, use_container_width=True, key="hist_chart")
            
            # Generate forecast
            with st.spinner('Generating forecast...'):
                forecast_df = simple_forecast(data, days)
                
                if forecast_df is None:
                    st.error('Failed to generate forecast. Please try again.')
                    return
            
            # Display forecast metrics
            st.subheader(f'📊 Forecast for Next {days} Days')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Predicted Price (End)', f'${forecast_df["Close"].iloc[-1]:.2f}')
            with col2:
                expected_return = ((forecast_df["Close"].iloc[-1] - current_price) / current_price) * 100
                st.metric('Expected Return', f'{expected_return:+.2f}%')
            with col3:
                st.metric('Prediction Range', f'${forecast_df["Close"].min():.2f} - ${forecast_df["Close"].max():.2f}')
            
            # Forecast Chart - FIXED
            st.subheader("Price Forecast")
            
            fig_forecast = go.Figure()
            
            # Historical data (last 180 days for context)
            hist_period = min(180, len(data))
            hist_data = data.iloc[-hist_period:]
            
            fig_forecast.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['Close'],
                mode='lines',
                name='Historical Price',
                line=dict(color='blue', width=2)
            ))
            
            # Forecast data
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df.index,
                y=forecast_df['Close'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', width=2, dash='dash'),
                marker=dict(size=6, symbol='circle')
            ))
            
            # Confidence interval
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df.index.tolist() + forecast_df.index.tolist()[::-1],
                y=forecast_df['Upper Bound'].tolist() + forecast_df['Lower Bound'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)',
                line=dict(color='rgba(255, 255, 255, 0)'),
                name='95% Confidence Interval'
            ))
            
            fig_forecast.update_layout(
                title=f'{ticker} Price Forecast - Next {days} Days',
                xaxis_title='Date',
                yaxis_title='Price (USD)',
                template='plotly_white',
                height=500,
                hovermode='x unified',
                legend=dict(x=0, y=1, traceorder='normal')
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True, key="forecast_chart")
            
            # Forecast Table - FIXED
            st.subheader('📋 Forecast Data Table')
            
            # Create display table
            display_forecast = forecast_df.copy()
            display_forecast['Date'] = display_forecast.index.strftime('%Y-%m-%d')
            display_forecast['Close'] = display_forecast['Close'].apply(lambda x: f'${x:.2f}')
            display_forecast['Lower Bound'] = display_forecast['Lower Bound'].apply(lambda x: f'${x:.2f}')
            display_forecast['Upper Bound'] = display_forecast['Upper Bound'].apply(lambda x: f'${x:.2f}')
            
            # Show first 10 days
            st.dataframe(display_forecast[['Date', 'Close', 'Lower Bound', 'Upper Bound']].head(10), 
                        use_container_width=True)
            
            # Show full forecast in expander
            with st.expander("View Complete Forecast (30 days)"):
                st.dataframe(display_forecast[['Date', 'Close', 'Lower Bound', 'Upper Bound']], 
                            use_container_width=True)
            
            # Recommendation
            st.subheader('💡 Investment Recommendation')
            
            if expected_return > 15:
                st.success(f"""
                ### 🟢 STRONG BUY
                - Expected return: **{expected_return:.1f}%** in {days} days
                - Strong upward trend predicted
                - Consider adding to portfolio
                """)
            elif expected_return > 5:
                st.info(f"""
                ### 🔵 BUY
                - Expected return: **{expected_return:.1f}%** in {days} days
                - Moderate upward trend predicted
                - Good entry point
                """)
            elif expected_return > 0:
                st.warning(f"""
                ### 🟡 HOLD
                - Expected return: **{expected_return:.1f}%** in {days} days
                - Limited upside predicted
                - Wait for better entry point
                """)
            else:
                st.error(f"""
                ### 🔴 AVOID / SELL
                - Expected return: **{expected_return:.1f}%** in {days} days
                - Downward trend predicted
                - Consider selling or avoiding
                """)
            
            # Risk Warning
            st.markdown('---')
            st.warning("""
            ⚠️ **Risk Warning:** This is a simplified linear regression forecast for educational purposes.
            - Past performance does not guarantee future results
            - Actual market movements can differ significantly
            - Always conduct your own research before investing
            - Consider consulting with a financial advisor
            """)
            
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
        st.write('Please check:')
        st.write('1. Stock ticker symbol is correct (e.g., AAPL, TSLA, MSFT)')
        st.write('2. Your internet connection is active')
        st.write(f'Error details: {type(e).__name__}: {str(e)}')

if __name__ == '__main__':
    app()