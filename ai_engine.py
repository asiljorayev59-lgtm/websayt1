import requests
import pandas as pd
import json

# 🔥 H4 data (FOREX API yoki boshqa)
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=200"
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
prev = df.iloc[-2]

signal = "WAIT"

# 🔥 FAqat candle yopilganda
if last["time"] != prev["time"]:

    if last["ema50"] > last["ema200"] and last["rsi"] > 50:
        signal = "BUY"

    elif last["ema50"] < last["ema200"] and last["rsi"] < 50:
        signal = "SELL"

result = {
    "trend_h4": signal,
    "ema50": round(last["ema50"],2),
    "ema200": round(last["ema200"],2),
    "rsi": round(last["rsi"],2),
    "price": last["close"]
}

with open("signals.json","w") as f:
    json.dump(result,f,indent=2)

print(result)
