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


## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/trading-app-streamlit.git
cd trading-app-streamlit
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run trading_app.py
```


## 📈 Trading App

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
| Home Page | <img width="1894" height="914" alt="image" src="https://github.com/user-attachments/assets/35dbce2d-f579-4436-a4a6-649766f1bd7a" />
 |
| CAPM RETURN | <img width="1890" height="860" alt="image" src="https://github.com/user-attachments/assets/90aae64e-48cd-487d-a280-296602390851" />

 |
| Beta Calculator | <img width="1894" height="846" alt="image" src="https://github.com/user-attachments/assets/67436c50-e962-4f96-a9af-733b5e4bd6d5" />
) |
| Stock Charts | <img width="1892" height="741" alt="image" src="https://github.com/user-attachments/assets/6c7fcbf4-74b1-421e-99c6-48f49eeebed6" />
 |
| Price Prediction | <img width="1893" height="883" alt="image" src="https://github.com/user-attachments/assets/b2d5a212-b0ee-4fd8-9d3e-07dfaa43c406" />
|

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
