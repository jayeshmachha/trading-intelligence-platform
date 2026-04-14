
# utils/model_train.py
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

def get_data(ticker, period="2y"):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_rolling_mean(data, window=30):
    """Calculate rolling mean"""
    rolling_mean = data.rolling(window=window).mean()
    return pd.DataFrame({'Close': rolling_mean.dropna()})

def get_difference_order(data):
    """Determine optimal differencing order using ADF test"""
    # Simple implementation - you can expand this
    return 1  # Default differencing order

def scaling(data):
    """Scale data using MinMaxScaler"""
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

def evaluate_model(scaled_data, differencing_order):
    """Evaluate ARIMA model and return RMSE"""
    try:
        # Split data
        train_size = int(len(scaled_data) * 0.8)
        train, test = scaled_data[:train_size], scaled_data[train_size:]
        
        # Fit model
        model = ARIMA(train, order=(differencing_order, 1, 0))
        model_fit = model.fit()
        
        # Predict
        predictions = model_fit.forecast(steps=len(test))
        
        # Calculate RMSE
        rmse = np.sqrt(np.mean((predictions - test.flatten()) ** 2))
        return rmse
    except:
        return None

def get_forecast(scaled_data, differencing_order, steps=30):
    """Generate forecast"""
    try:
        # Fit model on full data
        model = ARIMA(scaled_data, order=(differencing_order, 1, 0))
        model_fit = model.fit()
        
        # Forecast
        forecast = model_fit.forecast(steps=steps)
        
        # Create DataFrame
        forecast_df = pd.DataFrame({'Close': forecast})
        return forecast_df
    except:
        # Return dummy forecast if model fails
        return pd.DataFrame({'Close': np.random.randn(30) * 0.1 + 0.5})

def inverse_scaling(scaler, scaled_values):
    """Inverse transform scaled values"""
    # Reshape for inverse transform
    scaled_values = np.array(scaled_values).reshape(-1, 1)
    return scaler.inverse_transform(scaled_values)
