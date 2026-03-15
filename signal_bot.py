import json
import time

from data_fetch import get_candles
from strategies import ema_signal,rsi_signal,macd_signal
from ai_engine import ai_signal


while True:

    df=get_candles()

    ema=ema_signal(df)
    rsi=rsi_signal(df)
    macd=macd_signal(df)

    ai=ai_signal([ema,rsi,macd])

    data={
        "symbol":"BTCUSDT",
        "signals":{
            "ema":ema,
            "rsi":rsi,
            "macd":macd,
            "ai":ai
        },
        "price":float(df["close"].iloc[-1])
    }

    with open("data/signals.json","w") as f:
        json.dump(data,f)

    try:
        history=json.load(open("data/history.json"))
    except:
        history=[]

    history.append({
        "time":time.strftime("%H:%M"),
        "signal":ai
    })

    history=history[-50:]

    json.dump(history,open("data/history.json","w"))

    time.sleep(60)
