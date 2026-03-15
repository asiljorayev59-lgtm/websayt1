def ema_strategy(df):

    df["ema50"]=df["close"].ewm(span=50).mean()
    df["ema200"]=df["close"].ewm(span=200).mean()

    if df["ema50"].iloc[-1] > df["ema200"].iloc[-1]:
        return "BUY"

    if df["ema50"].iloc[-1] < df["ema200"].iloc[-1]:
        return "SELL"

    return "WAIT"
