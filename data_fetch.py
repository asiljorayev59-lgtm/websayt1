import requests
import pandas as pd

def get_candles():

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":"BTCUSDT",
        "interval":"1m",
        "limit":200
    }

    r=requests.get(url,params=params)
    data=r.json()

    df=pd.DataFrame(data)

    df=df[[0,1,2,3,4,5]]

    df.columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    df["close"]=df["close"].astype(float)

    return df
