import json
import time
from data_fetch import get_candles
from strategies import ema_strategy
from strategies import rsi_strategy
from strategies import macd_strategy

while True:

    df=get_candles()

    ema=ema_strategy(df)
    rsi=rsi_strategy(df)
    macd=macd_strategy(df)

    ai=ai_signal([ema,rsi,macd])

    data={
        "symbol":"BTCUSDT",
        "signals":{
            "ema":ema,
            "rsi":rsi,
            "macd":macd,
            "ai":ai
        }
    }

    with open("data/signals.json","w") as f:
        json.dump(data,f)

    time.sleep(60)
