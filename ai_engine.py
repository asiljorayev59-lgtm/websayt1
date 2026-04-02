import requests
import pandas as pd
import json

# 🔥 REAL GOLD PRICE
price = requests.get("https://api.gold-api.com/price/XAU").json()["price"]

# =========================
# 📊 TREND ANALYSIS (H1/H4/D1)
# =========================
def analyze(tf):

    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={tf}&limit=200"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:,0:6]
    df.columns = ["time","open","high","low","close","volume"]
    df = df.astype(float)

    df["ema50"] = df["close"].ewm(span=50).mean()
    df["ema200"] = df["close"].ewm(span=200).mean()

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100/(1+rs))

    last = df.iloc[-1]

    bos = "NONE"
    if last["high"] > df["high"].iloc[-5]:
        bos = "BOS UP"
    elif last["low"] < df["low"].iloc[-5]:
        bos = "BOS DOWN"

    resistance = df["high"].tail(20).max()
    support = df["low"].tail(20).min()

    signal = "WAIT"

    if bos=="BOS UP" and last["ema50"]>last["ema200"] and last["rsi"]>55:
        signal = "BUY"
    elif bos=="BOS DOWN" and last["ema50"]<last["ema200"] and last["rsi"]<45:
        signal = "SELL"

    return signal, bos, resistance, support

h1,_,_,_ = analyze("1h")
h4,bos,res,sup = analyze("4h")
d1,_,_,_ = analyze("1d")

# =========================
# ⚡ SCALPING (M1/M5)
# =========================
def scalp(tf):

    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={tf}&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:,0:6]
    df.columns = ["time","open","high","low","close","volume"]
    df = df.astype(float)

    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema21"] = df["close"].ewm(span=21).mean()

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100/(1+rs))

    last = df.iloc[-1]
    prev = df.iloc[-2]

    signal = "WAIT"

    if last["ema9"] > last["ema21"] and prev["ema9"] <= prev["ema21"] and last["rsi"] > 55:
        signal = "BUY"
    elif last["ema9"] < last["ema21"] and prev["ema9"] >= prev["ema21"] and last["rsi"] < 45:
        signal = "SELL"

    entry = price
    tp = entry + 10 if signal=="BUY" else entry - 10
    sl = entry - 7 if signal=="BUY" else entry + 7

    return signal, entry, tp, sl

m1,_,_,_ = scalp("1m")
m5,entry,tp,sl = scalp("5m")

# =========================
# 💾 SAVE JSON
# =========================
signals = {
    "price": round(price,2),

    "h1": h1,
    "h4": h4,
    "d1": d1,

    "bos_h4": bos,
    "resistance": round(res,2),
    "support": round(sup,2),

    "entry": round(price,2),
    "tp": round(price+50,2),
    "sl": round(price-30,2),

    "scalp_m1": m1,
    "scalp_m5": m5,
    "scalp_entry": round(entry,2),
    "scalp_tp": round(tp,2),
    "scalp_sl": round(sl,2)
}

with open("signals.json","w") as f:
    json.dump(signals,f,indent=2)

print(signals)
