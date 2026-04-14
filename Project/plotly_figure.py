import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dateutil.relativedelta
import datetime
import pandas_ta as pta

def plotly_table(dataframe):
    """Create a styled Plotly table"""
    try:
        headcolor = "grey"
        rowEvenColor = "#f8fafd"
        rowOddColor = "#e1efff"
        
        # Handle empty dataframe
        if dataframe.empty:
            return go.Figure()
        
        # Convert index to list for display
        index_values = [str(i)[:10] for i in dataframe.index]
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=["<b>Index</b>"] + ["<b>" + str(col) + "</b>" for col in dataframe.columns],
                line_color="#0078ff",
                fill_color='#0078ff',
                align='center',
                font=dict(color="white", size=15),
                height=35,
            ),
            cells=dict(
                values=[index_values] + [dataframe[col].round(3) for col in dataframe.columns],
                fill_color=[[rowOddColor, rowEvenColor]],
                align='left',
                line_color=['white'],
                font=dict(color=["black"], size=12)
            )
        )])
        
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        return fig
        
    except Exception as e:
        print(f"Error creating table: {e}")
        return go.Figure()

def filter_data(dataframe, num_period):
    """Filter dataframe based on time period"""
    try:
        if dataframe.empty:
            return dataframe
        
        today = dataframe.index[-1]
        
        if num_period == '5d':
            date = today - datetime.timedelta(days=5)
        elif num_period == '1mo':
            date = today - dateutil.relativedelta.relativedelta(months=1)
        elif num_period == '6mo':
            date = today - dateutil.relativedelta.relativedelta(months=6)
        elif num_period == '1y':
            date = today - dateutil.relativedelta.relativedelta(years=1)
        elif num_period == '5y':
            date = today - dateutil.relativedelta.relativedelta(years=5)
        elif num_period == 'ytd':
            date = datetime.date(today.year, 1, 1)
        else:
            date = dataframe.index[0]
        
        # Ensure we have datetime objects
        if not isinstance(date, pd.Timestamp):
            date = pd.Timestamp(date)
        
        # Filter dataframe
        filtered_df = dataframe[dataframe.index >= date]
        return filtered_df
        
    except Exception as e:
        print(f"Error filtering data: {e}")
        return dataframe

def close_chart(dataframe, num_period=False):
    """Create close price chart with OHLC lines"""
    try:
        if num_period:
            dataframe = filter_data(dataframe, num_period)
        
        if dataframe.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['Open'], 
            mode='lines',
            name='Open', 
            line=dict(width=2, color='#5ab7ff')
        ))
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['Close'], 
            mode='lines',
            name='Close', 
            line=dict(width=2, color='black')
        ))
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['High'], 
            mode='lines',
            name='High', 
            line=dict(width=2, color='#0078ff')
        ))
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['Low'], 
            mode='lines',
            name='Low', 
            line=dict(width=2, color='red')
        ))
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            height=500, 
            margin=dict(l=0, r=20, t=20, b=0), 
            plot_bgcolor='white', 
            paper_bgcolor='#e1efff', 
            legend=dict(yanchor='top', xanchor='right')
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating close chart: {e}")
        return go.Figure()

def candlestick(dataframe, num_period):
    """Create candlestick chart"""
    try:
        dataframe = filter_data(dataframe, num_period)
        
        if dataframe.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Candlestick(
            x=dataframe.index,
            open=dataframe['Open'],
            high=dataframe['High'],
            low=dataframe['Low'],
            close=dataframe['Close'],
            name='Candlestick'
        )])
        
        fig.update_layout(
            showlegend=False, 
            height=500, 
            margin=dict(l=0, r=20, t=20, b=0),
            plot_bgcolor='white', 
            paper_bgcolor='#e1efff'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating candlestick chart: {e}")
        return go.Figure()

def RSI(dataframe, num_period):
    """Create RSI indicator chart"""
    try:
        # Calculate RSI
        dataframe['RSI'] = pta.rsi(dataframe['Close'], length=14)
        
        if num_period:
            dataframe = filter_data(dataframe, num_period)
        
        if dataframe.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # RSI line
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['RSI'], 
            name='RSI', 
            marker_color='orange', 
            line=dict(width=2, color='orange')
        ))
        
        # Overbought line (70)
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=[70] * len(dataframe), 
            name='Overbought (70)', 
            marker_color='red', 
            line=dict(width=2, color='red', dash='dash')
        ))
        
        # Oversold line (30)
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=[30] * len(dataframe), 
            name='Oversold (30)', 
            marker_color='green', 
            line=dict(width=2, color='green', dash='dash')
        ))
        
        fig.update_layout(
            yaxis_range=[0, 100],
            height=200, 
            plot_bgcolor='white', 
            paper_bgcolor='#e1efff', 
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='right', x=1)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating RSI chart: {e}")
        return go.Figure()

def moving_average_chart(dataframe, num_period=False):
    """Create chart with moving averages"""
    try:
        if num_period:
            dataframe = filter_data(dataframe, num_period)
        
        if dataframe.empty:
            return go.Figure()
        
        # Calculate moving averages
        dataframe['SMA_20'] = dataframe['Close'].rolling(window=20).mean()
        dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()
        dataframe['SMA_200'] = dataframe['Close'].rolling(window=200).mean()
        
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['Close'], 
            mode='lines',
            name='Close Price', 
            line=dict(width=2, color='black')
        ))
        
        # Moving averages
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['SMA_20'], 
            mode='lines',
            name='SMA 20', 
            line=dict(width=1.5, color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['SMA_50'], 
            mode='lines',
            name='SMA 50', 
            line=dict(width=1.5, color='orange')
        ))
        
        fig.add_trace(go.Scatter(
            x=dataframe.index, 
            y=dataframe['SMA_200'], 
            mode='lines',
            name='SMA 200', 
            line=dict(width=1.5, color='red')
        ))
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            height=500, 
            margin=dict(l=0, r=20, t=20, b=0), 
            plot_bgcolor='white', 
            paper_bgcolor='#e1efff', 
            legend=dict(yanchor='top', xanchor='right')
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating moving average chart: {e}")
        return go.Figure()

def MACD_chart(dataframe, num_period):
    """Create MACD indicator chart"""
    try:
        # Calculate MACD
        macd_data = pta.macd(dataframe['Close'])
        
        if macd_data is not None:
            dataframe["MACD"] = macd_data.iloc[:, 0]  # MACD line
            dataframe["MACD Signal"] = macd_data.iloc[:, 1]  # Signal line
            dataframe["MACD Hist"] = macd_data.iloc[:, 2]  # Histogram
        
        if num_period:
            dataframe = filter_data(dataframe, num_period)
        
        if dataframe.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # MACD line
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['MACD'],
            name='MACD',
            marker_color='orange',
            line=dict(width=2, color='orange')
        ))
        
        # Signal line
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['MACD Signal'],
            name='Signal Line',
            marker_color='red',
            line=dict(width=2, color='red', dash='dash')
        ))
        
        # Histogram
        colors = ['red' if val < 0 else 'green' for val in dataframe['MACD Hist']]
        
        fig.add_trace(go.Bar(
            x=dataframe.index,
            y=dataframe['MACD Hist'],
            name='MACD Histogram',
            marker_color=colors,
            opacity=0.5
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='#e1efff',
            margin=dict(l=0, r=20, t=20, b=0),
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating MACD chart: {e}")
        return go.Figure()

def moving_average_forecast(dataframe):
    """Create forecast chart with moving averages"""
    try:
        fig = go.Figure()
        
        # Actual Close Price
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['Close'],
            name='Actual Price',
            line=dict(color='blue', width=2)
        ))
        
        # 20-Day Moving Average
        dataframe['MA20'] = dataframe['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['MA20'],
            name='20-Day MA',
            line=dict(color='orange', width=2)
        ))
        
        # 50-Day Moving Average
        dataframe['MA50'] = dataframe['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=dataframe.index,
            y=dataframe['MA50'],
            name='50-Day MA',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # 200-Day Moving Average if data is long enough
        if len(dataframe) > 200:
            dataframe['MA200'] = dataframe['Close'].rolling(window=200).mean()
            fig.add_trace(go.Scatter(
                x=dataframe.index,
                y=dataframe['MA200'],
                name='200-Day MA',
                line=dict(color='purple', width=2, dash='dot')
            ))
        
        fig.update_layout(
            title='Moving Average Forecast',
            xaxis_title='Date',
            yaxis_title='Price',
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='#e1efff',
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating moving average forecast: {e}")
        return go.Figure()

# Alias for backward compatibility
def Moving_average_forecast(dataframe):
    """Alias for moving_average_forecast"""
    return moving_average_forecast(dataframe)