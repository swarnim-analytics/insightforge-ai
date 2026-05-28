import yfinance as yf
import pandas as pd
import ta


def analyze_stock(ticker):

    df = yf.download(
        ticker,
        period="3mo",
        interval="1d"
    )

    if df.empty:

        return "No data found."

    close = df["Close"].squeeze()

    latest_price = round(close.iloc[-1], 2)

    rsi = ta.momentum.RSIIndicator(
        close.squeeze()
    ).rsi().iloc[-1]

    sma20 = close.rolling(20).mean().iloc[-1]

    trend = (
        "Bullish"
        if latest_price > sma20
        else "Bearish"
    )

    result = f"""
📈 STOCK ANALYSIS

Ticker: {ticker}

Current Price: {latest_price}

RSI: {round(float(rsi), 2)}

20-Day SMA: {round(float(sma20), 2)}

Trend: {trend}
"""

    return result


if __name__ == "__main__":

    print(
        analyze_stock("RELIANCE.NS")
    )