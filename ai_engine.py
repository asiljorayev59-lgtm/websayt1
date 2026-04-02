import requests
import pandas as pd
import json

# 🔥 REAL GOLD PRICE
price_data = requests.get("https://api.gold-api.com/price/XAU").json()
price = price_data["price"]

def analyze(tf):

    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={tf}&limit=200"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:,0:6]
    df.columns = ["time","open","high","low","close","volume"]

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

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

    # 🔥 BREAKOUT (oxirgi 20 candle)
    resistance = df["high"].tail(20).max()
    support = df["low"].tail(20).min()

    breakout = "NONE"

    if last["close"] > resistance:
        breakout = "UP"
    elif last["close"] < support:
        breakout = "DOWN"

    # 🔥 SMC (simple liquidity logic)
    liquidity = "NO"

    if last["high"] > resistance:
        liquidity = "LIQUIDITY TAKEN (BUY)"
    elif last["low"] < support:
        liquidity = "LIQUIDITY TAKEN (SELL)"

    # 🔥 FINAL SIGNAL
    signal = "WAIT"

    if breakout == "UP" and last["ema50"] > last["ema200"] and last["rsi"] > 55:
        signal = "BUY"

    elif breakout == "DOWN" and last["ema50"] < last["ema200"] and last["rsi"] < 45:
        signal = "SELL"

    return signal, breakout, liquidity, round(resistance,2), round(support,2)

# 🔥 TIMEFRAMES
h1, b1, l1, r1, s1 = analyze("1h")
h4, b4, l4, r4, s4 = analyze("4h")
d1, bD, lD, rD, sD = analyze("1d")

signals = {
    "h1": h1,
    "h4": h4,
    "d1": d1,

    "breakout_h1": b1,
    "breakout_h4": b4,
    "breakout_d1": bD,

    "liquidity_h1": l1,
    "liquidity_h4": l4,
    "liquidity_d1": lD,

    "resistance": r4,
    "support": s4,

    "price": round(price,2)
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)

print(signals)
