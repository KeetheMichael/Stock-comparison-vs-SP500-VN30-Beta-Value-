import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import matplotlib.dates as mdates


def draw(ticker):
    ticker = ticker.upper().strip()
    df = yf.download(
        ticker,  # ticker
        period="1y",  # how much history
        interval="1d"  # timeframe
    )
    plt.figure()
    plt.plot(df.index, df["Close"])
    plt.title(f'{ticker} Closing Prices – 1 Year')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig("plot.png")
    plt.close()
    df = df.xs(ticker, axis=1, level=1)
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low",
                                               "Close"]].astype(float)
    fig = go.Figure(data=[
        go.Candlestick(x=df.index,
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'])
    ],
                    layout_title_text=f"{ticker} Candlestick Chart – 1 Year")
    fig.show()


def comptosp500(ticker):
    ticker = ticker.upper().strip()

    df = yf.download([ticker, "SPY"], period="5y", interval="1d")
    close = df["Close"]
    returns = close.pct_change().dropna()
    beta = returns[ticker].cov(returns["SPY"]) / returns["SPY"].var()

    if df.empty:
        print("No data found")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(close.index, close[ticker])
    axes[0].set_title(ticker)
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Price")

    #SPY
    axes[1].plot(close.index, close["SPY"])
    axes[1].set_title("SPY (S&P 500)")
    axes[1].set_xlabel("Date")
    for ax in axes:
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.text(0.5,
             0.02,
             f"Beta ({ticker} vs SPY): {beta:.2f}",
             ha="center",
             fontsize=12)
    plt.tight_layout()
    plt.show()


def comptovn30(ticker):
    ticker = ticker.upper().strip()

    df = yf.download([ticker, "FUESSV30.VN"], period="5y", interval="1d")
    close = df["Close"]
    returns = close.pct_change().dropna()
    beta = returns[ticker].cov(returns["FUESSV30.VN"]) / returns["FUESSV30.VN"].var()

    if df.empty:
        print("No data found")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(close.index, close[ticker])
    axes[0].set_title(ticker)
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Price")

    #SPY
    axes[1].plot(close.index, close["FUESSV30.VN"])
    axes[1].set_title("FUESSV30 (VN 30)")
    axes[1].set_xlabel("Date")
    for ax in axes:
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.text(0.5,
             0.02,
             f"Beta ({ticker} vs VN30): {beta:.2f}",
             ha="center",
             fontsize=12)
    plt.tight_layout()
    plt.show()


import sys

if __name__ == "__main__":
    command = input("Enter command (draw / comptosp500/comptovn30): ")
    ticker = input("Enter ticker: ")
    if command == "draw":
        draw(ticker)
    elif command == "comptosp500":
        comptosp500(ticker)
    elif command == "comptovn30":
        comptovn30(ticker)
    else:
        print("Unknown command")
