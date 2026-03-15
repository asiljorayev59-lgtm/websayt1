import pandas as pd

def ema_signal(df):

    ema20=df["close"].ewm(span=20).mean()
    ema50=df["close"].ewm(span=50).mean()

    if ema20.iloc[-1] > ema50.iloc[-1]:
        return "BUY"

    if ema20.iloc[-1] < ema50.iloc[-1]:
        return "SELL"

    return "WAIT"


def rsi_signal(df):

    delta=df["close"].diff()

    gain=delta.clip(lower=0)
    loss=-delta.clip(upper=0)

    avg_gain=gain.rolling(14).mean()
    avg_loss=loss.rolling(14).mean()

    rs=avg_gain/avg_loss

    rsi=100-(100/(1+rs))

    r=rsi.iloc[-1]

    if r < 30:
        return "BUY"

    if r > 70:
        return "SELL"

    return "WAIT"


def macd_signal(df):

    ema12=df["close"].ewm(span=12).mean()
    ema26=df["close"].ewm(span=26).mean()

    macd=ema12-ema26

    signal=macd.ewm(span=9).mean()

    if macd.iloc[-1] > signal.iloc[-1]:
        return "BUY"

    if macd.iloc[-1] < signal.iloc[-1]:
        return "SELL"

    return "WAIT"
