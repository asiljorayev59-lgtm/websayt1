def ai_signal(signals):

    buy=signals.count("BUY")
    sell=signals.count("SELL")

    if buy > sell:
        return "BUY"

    if sell > buy:
        return "SELL"

    return "WAIT"
