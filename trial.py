import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

pio.renderers.default = "browser"

def draw(ticker):
    ticker = ticker.strip().upper()

    df = yf.download(ticker, period="1y", interval="1d", progress=False)

    # ✅ Flatten MultiIndex columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ticker, axis=1, level=1)

    # Clean
    df = df.dropna()
    df[["Open","High","Low","Close"]] = df[["Open","High","Low","Close"]].astype(float)

    # Matplotlib line plot (optional)
    plt.figure()
    plt.plot(df.index, df["Close"])
    plt.title(f"{ticker} Closing Prices – 1 Year")
    plt.tight_layout()
    plt.show()

    # Plotly candlestick
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])

    fig.update_layout(
        title=f"{ticker} Candlestick Chart – 1 Year",
        yaxis=dict(type="linear"),
        xaxis_rangeslider_visible=False
    )

    fig.show()

ticker = input("Enter stock ticker: ")
draw(ticker)
