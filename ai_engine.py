import requests
import pandas as pd
import json

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

    # 🔥 BOS / CHoCH
    prev_high = df["high"].iloc[-5]
    prev_low = df["low"].iloc[-5]

    bos = "NONE"
    if last["high"] > prev_high:
        bos = "BOS UP"
    elif last["low"] < prev_low:
        bos = "BOS DOWN"

    # 🔥 ORDER BLOCK (oddiy)
    ob = "NONE"
    if last["close"] > last["open"]:
        ob = "Bullish OB"
    elif last["close"] < last["open"]:
        ob = "Bearish OB"

    # 🔥 FVG
    fvg = "NONE"
    if df["low"].iloc[-2] > df["high"].iloc[-4]:
        fvg = "FVG UP"
    elif df["high"].iloc[-2] < df["low"].iloc[-4]:
        fvg = "FVG DOWN"

    # 🔥 FINAL SIGNAL
    signal = "WAIT"

    if bos == "BOS UP" and fvg == "FVG UP":
        signal = "BUY"
    elif bos == "BOS DOWN" and fvg == "FVG DOWN":
        signal = "SELL"

    return signal, bos, ob, fvg

# TIMEFRAMES
h1, bos1, ob1, fvg1 = analyze("1h")
h4, bos4, ob4, fvg4 = analyze("4h")
d1, bosD, obD, fvgD = analyze("1d")

signals = {
    "h1": h1,
    "h4": h4,
    "d1": d1,

    "bos_h1": bos1,
    "bos_h4": bos4,
    "bos_d1": bosD,

    "ob_h1": ob1,
    "ob_h4": ob4,
    "ob_d1": obD,

    "fvg_h1": fvg1,
    "fvg_h4": fvg4,
    "fvg_d1": fvgD,

    "price": round(price,2)
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)

print(signals)
