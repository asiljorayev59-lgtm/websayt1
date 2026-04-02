import requests
import pandas as pd
import json

price = requests.get("https://api.gold-api.com/price/XAU").json()["price"]

def analyze(tf):

    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={tf}&limit=200"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:,0:6]
    df.columns = ["time","open","high","low","close","volume"]

    df = df.astype(float)

    # EMA
    df["ema50"] = df["close"].ewm(span=50).mean()
    df["ema200"] = df["close"].ewm(span=200).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100/(1+rs))

    last = df.iloc[-1]

    # 🔥 BOS
    bos = "NONE"
    if last["high"] > df["high"].iloc[-5]:
        bos = "BOS UP"
    elif last["low"] < df["low"].iloc[-5]:
        bos = "BOS DOWN"

    # 🔥 ORDER BLOCK (eng kuchli candle)
    ob_price = df["close"].iloc[-3]

    # 🔥 LIQUIDITY ZONE
    resistance = df["high"].tail(20).max()
    support = df["low"].tail(20).min()

    # 🔥 ENTRY LOGIC (AI)
    signal = "WAIT"
    entry = price
    tp = 0
    sl = 0

    if (
        bos == "BOS UP" and
        last["ema50"] > last["ema200"] and
        last["rsi"] > 55
    ):
        signal = "BUY"
        tp = entry + 50
        sl = entry - 30

    elif (
        bos == "BOS DOWN" and
        last["ema50"] < last["ema200"] and
        last["rsi"] < 45
    ):
        signal = "SELL"
        tp = entry - 50
        sl = entry + 30

    return {
        "signal": signal,
        "bos": bos,
        "ob": round(ob_price,2),
        "res": round(resistance,2),
        "sup": round(support,2),
        "entry": round(entry,2),
        "tp": round(tp,2),
        "sl": round(sl,2)
    }

h1 = analyze("1h")
h4 = analyze("4h")
d1 = analyze("1d")

signals = {
    "price": round(price,2),

    "h1": h1["signal"],
    "h4": h4["signal"],
    "d1": d1["signal"],

    "bos_h4": h4["bos"],
    "ob_h4": h4["ob"],
    "resistance": h4["res"],
    "support": h4["sup"],

    "entry": h4["entry"],
    "tp": h4["tp"],
    "sl": h4["sl"]
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)
