import json
import random
from datetime import datetime

signals = ["BUY","SELL","WAIT"]

data = {
    "trend_m5": random.choice(signals),
    "trend_m15": random.choice(signals),
    "trend_h1": random.choice(signals),
    "scalp_m1": random.choice(signals),
    "scalp_m5": random.choice(signals),
    "sm_m15": random.choice(signals),
    "sm_h1": random.choice(signals),
    "sm_h4": random.choice(signals),
    "ai": random.randint(40,90),
    "time": str(datetime.now())
}

with open("../signals.json","w") as f:
    json.dump(data,f,indent=2)
