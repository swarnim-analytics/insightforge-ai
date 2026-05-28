import yfinance as yf
import pandas as pd
import ta


WATCHLIST = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]


def analyze_stock(ticker):

    df = yf.download(
        ticker,
        period="3mo",
        interval="1d",
        progress=False
    )

    if df.empty:

        return "No data found."

    close = df["Close"].squeeze()

    latest_price = round(
        float(close.iloc[-1]),
        2
    )

    rsi = ta.momentum.RSIIndicator(
        close
    ).rsi().iloc[-1]

    sma20 = close.rolling(
        20
    ).mean().iloc[-1]

    trend = (
        "Bullish 📈"
        if latest_price > sma20
        else "Bearish 📉"
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


def analyze_watchlist():

    results = []

    for ticker in WATCHLIST:

        try:

            df = yf.download(
                ticker,
                period="3mo",
                interval="1d",
                progress=False
            )

            if df.empty:
                continue

            close = df["Close"].squeeze()

            latest_price = close.iloc[-1]

            rsi = ta.momentum.RSIIndicator(
                close
            ).rsi().iloc[-1]

            sma20 = close.rolling(
                20
            ).mean().iloc[-1]

            if rsi > 70:
                signal = "Overbought ⚠️"

            elif rsi < 30:
                signal = "Oversold 🟢"

            elif latest_price > sma20:
                signal = "Bullish 📈"

            else:
                signal = "Bearish 📉"

            results.append(
                f"{ticker} → {signal}"
            )

        except Exception:
            continue

    return (
        "📊 WATCHLIST ANALYSIS\n\n"
        + "\n".join(results)
    )


if __name__ == "__main__":

    print(
        analyze_stock("RELIANCE.NS")
    )

    print("\n")

    print(
        analyze_watchlist()
    )