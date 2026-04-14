# 📈 Trading Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![YFinance](https://img.shields.io/badge/YFinance-Live%20Data-purple.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-orange.svg)

**Advanced Stock Analysis & Trading Decision Support System**

[Live Demo](#) • [Report Bug](#) • [Request Feature](#)

</div>

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Modules Explained](#-modules-explained)
- [Screenshots](#-screenshots)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**Trading Intelligence Platform** is a comprehensive stock analysis and trading decision support system built with Streamlit. It empowers investors with institutional-grade analytics including CAPM calculations, beta analysis, technical indicators, and price predictions.

### Why This Tool?
- ✅ **Real-time Data**: Live stock data via Yahoo Finance
- ✅ **Academic Foundation**: Built on CAPM (Nobel Prize-winning theory)
- ✅ **Risk Management**: Comprehensive volatility and risk metrics
- ✅ **User-Friendly**: No coding required - interactive web interface

---

## ✨ Key Features

### 1. 📊 **CAPM Expected Return Calculator**
- Calculate expected returns using Capital Asset Pricing Model
- Multi-stock comparison (up to 4 stocks simultaneously)
- Annualized market return calculations
- Security Market Line (SML) visualization

### 2. 📈 **Beta Coefficient Analysis**
- Calculate stock volatility relative to market
- Support for multiple indices (S&P 500, NASDAQ, Dow Jones, FTSE 100)
- Alpha, correlation, and R-squared metrics
- Risk classification (High/Moderate/Low risk)

### 3. 🔍 **Technical Stock Analysis**
- Candlestick charts with OHLC data
- Moving Averages (20, 50, 200-day)
- Trading volume analysis
- 52-week high/low tracking
- Volatility calculations (annualized)

### 4. 🤖 **Price Prediction Engine**
- 30-day price forecasting using linear regression
- Confidence intervals (95%)
- Buy/Hold/Sell recommendations
- Historical trend analysis

### 5. 📉 **Risk Metrics Dashboard**
- Value at Risk (VaR) calculation
- Sharpe ratio estimation
- Information ratio
- Daily and annualized volatility

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly |
| **Data Processing** | Pandas, NumPy |
| **Financial Data** | yfinance, pandas-datareader |
| **Statistical Models** | scikit-learn, statsmodels |
| **Technical Indicators** | pandas-ta |
| **Visualization** | Plotly Graph Objects |

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/trading-app-streamlit.git
cd trading-app-streamlit

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run trading_app.py


# 📈 Trading App

A multi-module financial analysis platform built with **Python** and **Streamlit**, offering CAPM-based return estimation, beta analysis, interactive stock charting, and ML-powered price prediction — all in one dashboard.

---

## 🚀 Quick Start

1. **Select a stock ticker** — e.g., `AAPL`, `TSLA`, `MSFT`, `NVDA`
2. **Choose an analysis period** — `1y`, `2y`, `3y`, or `5y`
3. **Navigate modules** using the sidebar

---

## 🗂️ Module Walkthrough

### 📍 Home
- Overview of all available features
- Platform introduction and navigation guide

---

### 💰 CAPM Return
1. Select 1–4 stocks from the dropdown
2. Set number of years for historical data
3. Adjust risk-free rate *(default: 2.5%)*
4. View beta values and expected returns
5. Analyze the **Security Market Line (SML)**

---

### 📈 CAPM Beta
1. Enter a stock symbol (e.g., `AAPL`)
2. Choose a market index benchmark
3. Select a time period
4. Get **beta**, **alpha**, and **correlation** metrics
5. View normalized price comparison charts

---

### 📊 Stock Analysis
1. Input a stock ticker
2. Set the date range
3. View interactive **candlestick charts**
4. Analyze **moving averages**
5. Check **volume patterns**

---

### 🤖 Stock Prediction
1. Enter a stock symbol
2. Select prediction horizon *(7–90 days)*
3. View forecast with **confidence intervals**
4. Get an **investment recommendation**

---

## 📚 Modules Explained

### CAPM — Capital Asset Pricing Model

$$E(R_i) = R_f + \beta_i \times (E(R_m) - R_f)$$

| Symbol | Meaning |
|--------|---------|
| `Rf` | Risk-free rate (10-year Treasury yield) |
| `β` (Beta) | Stock's sensitivity to market movements |
| `Rm` | Expected market return |

---

### Beta Interpretation

| Beta Range | Classification | Implication |
|------------|----------------|-------------|
| > 1.2 | 🔴 High Risk (Aggressive) | 20%+ more volatile than market |
| 0.8 – 1.2 | 🟡 Moderate Risk | Moves with the market |
| 0.5 – 0.8 | 🟢 Low Risk (Defensive) | Less volatile than market |
| < 0.5 | 🔵 Very Low Risk | Stable, defensive stock |

---

### Technical Indicators

| Indicator | Description |
|-----------|-------------|
| **RSI** | Relative Strength Index — momentum oscillator (0–100) |
| **MACD** | Trend-following momentum indicator |
| **Moving Averages** | SMA 20, SMA 50, SMA 200-day |
| **Bollinger Bands** | Volatility measurement tool |

---

## 🔌 API Reference

### Data Sources

| API | Endpoint | Purpose |
|-----|----------|---------|
| Yahoo Finance | `yfinance` | Real-time & historical stock data |
| FRED | `pandas-datareader` | S&P 500 historical data |
| Market Indices | `^GSPC`, `^IXIC`, `^DJI` | Benchmark index data |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Data | yfinance, pandas-datareader |
| Analysis | Pandas, NumPy, Scikit-learn |
| Visualization | Plotly, Matplotlib |
| Prediction | Linear Regression / Prophet |

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/jayeshmachha/<repo-name>.git
cd <repo-name>

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---
---

## 📸 Screenshots

| Module | Preview |
|--------|---------|
| Home Page | ![Home](https://via.placeholder.com/800x400?text=Trading+App+Home+Page) |
| CAPM Analysis | ![CAPM](https://via.placeholder.com/800x400?text=CAPM+Return+Calculator) |
| Beta Calculator | ![Beta](https://via.placeholder.com/800x400?text=Beta+Coefficient+Analysis) |
| Stock Charts | ![Charts](https://via.placeholder.com/800x400?text=Interactive+Candlestick+Charts) |
| Price Prediction | ![Prediction](https://via.placeholder.com/800x400?text=30-Day+Price+Forecast) |

---

## 👤 Author

**Jayesh Machha**  
B.Tech — Artificial Intelligence & Data Science  
Dr. Babasaheb Ambedkar Technological University, Mumbai

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/jayesh-machha-166aa42b3)
[![GitHub](https://img.shields.io/badge/GitHub-jayeshmachha-black?logo=github)](https://github.com/jayeshmachha)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE)
