import requests
import pandas as pd
import json

# 🔥 REAL GOLD PRICE
price_data = requests.get("https://api.gold-api.com/price/XAU").json()
price = price_data["price"]

# 🔥 FUNCTION (TIMEFRAME DATA)
def get_data(interval):
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={interval}&limit=200"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:,0:6]
    df.columns = ["time","open","high","low","close","volume"]

    df["close"] = df["close"].astype(float)

    # EMA
    df["ema50"] = df["close"].ewm(span=50).mean()
    df["ema200"] = df["close"].ewm(span=200).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100/(1+rs))

    last = df.iloc[-1]

    # 🔥 SIGNAL
    if last["ema50"] > last["ema200"] and last["rsi"] > 55:
        sig = "BUY"
    elif last["ema50"] < last["ema200"] and last["rsi"] < 45:
        sig = "SELL"
    else:
        sig = "WAIT"

    return sig, round(last["ema50"],2), round(last["rsi"],2)

# 🔥 3 TIMEFRAME
h1, ema1, rsi1 = get_data("1h")
h4, ema4, rsi4 = get_data("4h")
d1, emaD, rsiD = get_data("1d")

signals = {
    "h1": h1,
    "h4": h4,
    "d1": d1,
    "price": round(price,2),
    "ema50": ema4,
    "rsi": rsi4
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)

print(signals)
