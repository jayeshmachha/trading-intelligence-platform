import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def interactive_plot(df):
    """
    Create an interactive plotly line chart for multiple columns
    
    Parameters:
    df (pd.DataFrame): DataFrame with 'Date' column and price columns
    
    Returns:
    plotly.graph_objects.Figure: Interactive line chart
    """
    try:
        fig = go.Figure()
        
        # Check if Date column exists
        if 'Date' not in df.columns:
            # If no Date column, use index
            x_values = df.index
        else:
            x_values = df['Date']
        
        # Add traces for each column except Date
        for i in df.columns:
            if i != 'Date':
                fig.add_trace(go.Scatter(
                    x=x_values,
                    y=df[i],
                    mode='lines',
                    name=i,
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            width=450,
            margin=dict(l=20, t=50, r=20, b=20),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            plot_bgcolor='white',
            hovermode='x unified'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating interactive plot: {e}")
        return go.Figure()

def normalize(df):
    """
    Normalize prices based on initial price (first value = 1)
    
    Parameters:
    df (pd.DataFrame): DataFrame with date and price columns
    
    Returns:
    pd.DataFrame: Normalized DataFrame
    """
    try:
        df_normalized = df.copy()
        
        # Normalize each column except Date
        for i in df_normalized.columns:
            if i != 'Date' and i != 'date':
                if df_normalized[i].iloc[0] != 0:
                    df_normalized[i] = df_normalized[i] / df_normalized[i].iloc[0]
                else:
                    # Handle zero initial value
                    df_normalized[i] = df_normalized[i]
        
        return df_normalized
        
    except Exception as e:
        print(f"Error normalizing data: {e}")
        return df

def daily_return(df):
    """
    Calculate daily returns for each column
    
    Parameters:
    df (pd.DataFrame): DataFrame with price columns
    
    Returns:
    pd.DataFrame: DataFrame with daily returns
    """
    try:
        df_daily_return = df.copy()
        
        # Calculate returns for each column except Date
        for col in df_daily_return.columns:
            if col != 'Date' and col != 'date':
                # Calculate percentage change
                df_daily_return[col] = df_daily_return[col].pct_change()
                # Fill NaN values with 0
                df_daily_return[col] = df_daily_return[col].fillna(0)
        
        return df_daily_return
        
    except Exception as e:
        print(f"Error calculating daily returns: {e}")
        return df

def calculate_beta(stock_daily_return, stock):
    """
    Calculate beta coefficient for a stock relative to S&P 500
    
    Parameters:
    stock_daily_return (pd.DataFrame): DataFrame with daily returns including 'sp500'
    stock (str): Column name of the stock to calculate beta for
    
    Returns:
    tuple: (beta, alpha) where beta is the slope and alpha is the intercept
    """
    try:
        # Check if required columns exist
        if 'sp500' not in stock_daily_return.columns:
            raise ValueError("'sp500' column not found in DataFrame")
        
        if stock not in stock_daily_return.columns:
            raise ValueError(f"'{stock}' column not found in DataFrame")
        
        # Remove any NaN values
        valid_data = stock_daily_return[['sp500', stock]].dropna()
        
        if len(valid_data) < 2:
            raise ValueError("Not enough data points to calculate beta")
        
        # Calculate beta using polyfit (linear regression)
        # b = beta (slope), a = alpha (intercept)
        b, a = np.polyfit(valid_data['sp500'], valid_data[stock], 1)
        
        # Calculate additional metrics
        # Correlation
        correlation = valid_data['sp500'].corr(valid_data[stock])
        
        # R-squared
        r_squared = correlation ** 2
        
        # Annualized alpha and beta (if needed)
        # Note: Returns should already be daily returns
        # For annualized: multiply daily returns by 252
        
        return b, a, correlation, r_squared
        
    except Exception as e:
        print(f"Error calculating beta: {e}")
        return None, None, None, None

def calculate_beta_simple(stock_returns, market_returns):
    """
    Simple beta calculation using numpy
    
    Parameters:
    stock_returns (np.array): Array of stock returns
    market_returns (np.array): Array of market returns
    
    Returns:
    float: Beta coefficient
    """
    try:
        # Remove NaN values
        mask = ~(np.isnan(stock_returns) | np.isnan(market_returns))
        stock_returns_clean = stock_returns[mask]
        market_returns_clean = market_returns[mask]
        
        if len(stock_returns_clean) < 2:
            return None
        
        # Calculate covariance and variance
        covariance = np.cov(stock_returns_clean, market_returns_clean)[0][1]
        variance = np.var(market_returns_clean)
        
        if variance == 0:
            return None
        
        beta = covariance / variance
        return beta
        
    except Exception as e:
        print(f"Error calculating beta simple: {e}")
        return None

def calculate_expected_return(beta, risk_free_rate, market_return):
    """
    Calculate expected return using CAPM formula
    
    Parameters:
    beta (float): Stock beta
    risk_free_rate (float): Risk-free rate (e.g., 0.025 for 2.5%)
    market_return (float): Expected market return (e.g., 0.08 for 8%)
    
    Returns:
    float: Expected return
    """
    try:
        expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
        return expected_return
        
    except Exception as e:
        print(f"Error calculating expected return: {e}")
        return None

def calculate_portfolio_beta(weights, betas):
    """
    Calculate portfolio beta from individual stock betas
    
    Parameters:
    weights (list): List of weights for each stock (should sum to 1)
    betas (list): List of beta values for each stock
    
    Returns:
    float: Portfolio beta
    """
    try:
        if len(weights) != len(betas):
            raise ValueError("Weights and betas must have same length")
        
        portfolio_beta = sum(w * b for w, b in zip(weights, betas))
        return portfolio_beta
        
    except Exception as e:
        print(f"Error calculating portfolio beta: {e}")
        return None

def get_stock_data_for_capm(stock_data, market_data):
    """
    Prepare stock and market data for CAPM analysis
    
    Parameters:
    stock_data (pd.Series): Stock price series
    market_data (pd.Series): Market index price series
    
    Returns:
    dict: Dictionary containing returns, beta, etc.
    """
    try:
        # Align data by date
        combined = pd.DataFrame({
            'stock': stock_data,
            'market': market_data
        }).dropna()
        
        # Calculate daily returns
        stock_returns = combined['stock'].pct_change().dropna()
        market_returns = combined['market'].pct_change().dropna()
        
        # Align returns
        returns_df = pd.DataFrame({
            'stock_returns': stock_returns,
            'market_returns': market_returns
        }).dropna()
        
        # Calculate beta
        beta = calculate_beta_simple(
            returns_df['stock_returns'].values,
            returns_df['market_returns'].values
        )
        
        # Calculate alpha (intercept)
        if beta is not None:
            alpha = returns_df['stock_returns'].mean() - beta * returns_df['market_returns'].mean()
        else:
            alpha = None
        
        # Calculate correlation
        correlation = returns_df['stock_returns'].corr(returns_df['market_returns'])
        
        return {
            'returns_df': returns_df,
            'beta': beta,
            'alpha': alpha,
            'correlation': correlation,
            'stock_volatility': returns_df['stock_returns'].std() * np.sqrt(252),
            'market_volatility': returns_df['market_returns'].std() * np.sqrt(252)
        }
        
    except Exception as e:
        print(f"Error preparing CAPM data: {e}")
        return None

def plot_security_market_line(beta, expected_return, market_beta=1, market_return=None, risk_free_rate=None):
    """
    Plot Security Market Line (SML)
    
    Parameters:
    beta (float): Stock beta
    expected_return (float): Expected return for the stock
    market_beta (float): Market beta (default 1)
    market_return (float): Market return (optional)
    risk_free_rate (float): Risk-free rate (optional)
    
    Returns:
    plotly.graph_objects.Figure: SML plot
    """
    try:
        fig = go.Figure()
        
        # Create SML line from beta=0 to beta=2
        beta_range = np.linspace(0, 2, 100)
        
        if risk_free_rate is not None and market_return is not None:
            # Calculate SML using CAPM
            sml_returns = risk_free_rate + beta_range * (market_return - risk_free_rate)
            
            # Add SML line
            fig.add_trace(go.Scatter(
                x=beta_range,
                y=sml_returns,
                mode='lines',
                name='Security Market Line',
                line=dict(color='blue', width=2)
            ))
            
            # Add market point
            fig.add_trace(go.Scatter(
                x=[market_beta],
                y=[market_return],
                mode='markers',
                name='Market',
                marker=dict(size=12, color='green', symbol='star')
            ))
            
            # Add stock point
            fig.add_trace(go.Scatter(
                x=[beta],
                y=[expected_return],
                mode='markers',
                name='Stock',
                marker=dict(size=12, color='red', symbol='circle')
            ))
            
            fig.update_layout(
                title='Security Market Line (SML)',
                xaxis_title='Beta (β)',
                yaxis_title='Expected Return',
                plot_bgcolor='white',
                hovermode='closest',
                showlegend=True
            )
        
        return fig
        
    except Exception as e:
        print(f"Error plotting SML: {e}")
        return go.Figure()
    
    