import requests
import pandas as pd
import json

# 🔥 REAL GOLD PRICE
price_data = requests.get("https://api.gold-api.com/price/XAU").json()
price = price_data["price"]

# 🔥 MARKET DATA (temporary BTC, keyin real XAU qo‘shamiz)
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=200"
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

# 🔥 SIGNAL LOGIC
def get_signal():
    if last["ema50"] > last["ema200"] and last["rsi"] > 55:
        return "BUY"
    elif last["ema50"] < last["ema200"] and last["rsi"] < 45:
        return "SELL"
    else:
        return "WAIT"

signals = {
    "h1": get_signal(),
    "h4": get_signal(),
    "d1": get_signal(),
    "price": round(price,2),
    "ema50": round(last["ema50"],2),
    "ema200": round(last["ema200"],2),
    "rsi": round(last["rsi"],2)
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)

print(signals)
