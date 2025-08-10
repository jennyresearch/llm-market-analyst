# This is a market analyst module that provides functions to fetch stock prices and historical data.

import yfinance as yf
from typing import Tuple
import pandas as pd
import datetime as datetime

def get_stock_info(ticker: str) -> Tuple[str, str, str]:
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    name = info.get("longName", "")
    sector = info.get("sector", "")
    industry = info.get("industry", "")
    return name, sector, industry
def get_stock_price(ticker: str):
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    currency = info.get("currency", "")
    return price, currency

def historical_prices(ticker: str):
    # Download historical stock prices for the given ticker
    df = yf.download(ticker, period="2y", interval="1d")
    df.reset_index(inplace=True)
    # convert from multi-index to single index
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    # round float values to 2 digits
    df = df.round(2)
    
    # Calculate indicators
    # --- 1. Calculate Moving Averages (20‑day & 50‑day) ---
    df["SMA_20"] = df[f"Close {ticker}"].rolling(window=20).mean()
    df["SMA_50"] = df[f"Close {ticker}"].rolling(window=50).mean()

    # --- 2. Calculate RSI (14‑period) ---
    delta = df[f"Close {ticker}"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    # --- 3. Calculate MACD (12,26,9) ---
    ema12 = df[f"Close {ticker}"].ewm(span=12, adjust=False).mean()
    ema26 = df[f"Close {ticker}"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    df = df.round(2)

    return df

# promt definition: ticker analysis
from langchain_ollama.llms import OllamaLLM
def ticker_analysis(ticker, current_price, price_history):

    # Load the model
    #llm = OllamaLLM(model="llama3.2")  # Adjust the model name as needed, for example "deepseek-r1:7b" or "mistral"
    llm = OllamaLLM(model="gemma3n") 
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    
    # Prepare the prompt
    prompt = f'''
    You are a stock analysis expert who specializes in using technical indicators to analyze {ticker} buying and selling price levels.
    Indicators: moving averages, RSI, and MACD. 
    Your analysis needs to based on the historical date of {ticker} I provided you in {historical_prices}
    You are given data: 
    - current price in USD of {ticker} as {current_price} 
    - the historical price data from {price_history} with 2 years history and ordering from olderest to latest information.
    - moving averages in 20 days and 50 days is in columns 'SMA_20', 'SMA_50' in {price_history}.
    - RSI is the 14-day relative strength index is in columns 'RSI_14' in {price_history}.
    - MACD is the moving average convergence divergence in columns 'MACD', 'MACD_Signal','MACD_Hist' in {price_history}.
    Your answer: 
    - print out the lastest {ticker} price in USD information from {price_history} and with the Date information.
    - analyze the current price in relation to the historical data.
    - provide a recommendation on whether to "buy", "sell", or "hold" the stock based on your analysis.
    - explain your reasoning briefly, focusing on technical indicators and market trends.
    - answer is straightforward and concise, using simple language, and not too long.
    - in the end, you need to tell, the recommendation is provided on {today_date}.
        '''
    result = llm.invoke(prompt)

    return result

# indicator description
def indicator_description():
    # Indicator descriptions
    return """
    # Indicator descriptions
    ## 📊 1. Moving Average (MA)
    A moving average smooths out price data by calculating the average price of a stock over a specific number of days. It helps you see the trend more clearly by filtering out day-to-day price noise.

    🧮 Example:
    5-day MA: average of the last 5 closing prices
    50-day MA: shows the medium-term trend
    200-day MA: long-term trend indicator

    📈 How it's used:
    If the short-term MA (e.g. 20-day) crosses above the long-term MA (e.g. 50-day), that’s a bullish signal ("Golden Cross").
    If it crosses below, that’s a bearish signal ("Death Cross").

    ## 🔄 2. RSI (Relative Strength Index)
    RSI is a momentum indicator that measures how strongly a stock is moving in either direction. It ranges from 0 to 100.

    🧮 Interpretation:
    RSI > 70 = Overbought (might fall soon)
    RSI < 30 = Oversold (might rise soon)
    RSI = 50 = Neutral

    📈 How it's used:
    Traders look for reversals when RSI hits extreme levels (30 or 70).
    A stock that keeps rising despite a high RSI might indicate strong bullish momentum.                    

    ## 📉 3. MACD (Moving Average Convergence Divergence)
    MACD tracks the relationship between two moving averages: the 12-day EMA and the 26-day EMA (exponential moving averages). It also includes a Signal Line (usually 9-day EMA of the MACD).

    🧮 Formula:
    MACD = 12-day EMA - 26-day EMA
    Signal Line = 9-day EMA of MACD

    📈 How it's used:
    MACD crosses above Signal Line = Bullish signal
    MACD crosses below Signal Line = Bearish signal
    Traders also watch the MACD histogram, which shows the gap between MACD and Signal Line
    """
