import requests
import pandas as pd

def get_candles():

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":"BTCUSDT",
        "interval":"1m",
        "limit":200
    }

    data=requests.get(url,params=params).json()

    df=pd.DataFrame(data)

    df["close"]=df[4].astype(float)

    return df
