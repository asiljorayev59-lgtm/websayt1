import json
from data_fetch import get_candles
from strategies import ema_signal,rsi_signal,macd_signal
from ai_engine import ai_signal

df=get_candles()

ema=ema_signal(df)
rsi=rsi_signal(df)
macd=macd_signal(df)

signals=[ema,rsi,macd]

ai=ai_signal(signals)

data={

"symbol":"BTCUSDT",

"signals":{
"ema":ema,
"rsi":rsi,
"macd":macd,
"ai":ai
}

}

with open("signals.json","w") as f:
    json.dump(data,f)
