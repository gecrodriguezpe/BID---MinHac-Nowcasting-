import time 
print("Baseline")

time.sleep(3)
print("3 segundos")

from pytrends.request import TrendReq

pytrends = TrendReq(tz=360, timeout=(10,25))

pytrends.build_payload( [ "Ministerio de Hacienda" ], cat=0, timeframe="today 5-y", geo="CO")

import pandas as pd
df = pd.DataFrame(pytrends.interest_over_time())
df

import matplotlib.pyplot as plt

df['Ministerio de Hacienda'].plot()
plt.show()