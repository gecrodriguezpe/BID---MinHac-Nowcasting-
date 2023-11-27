import time
import os
main = f"{os.getcwd()}\../"

import pandas as pd
f = pd.read_excel(f"{main}inputs/inputs_gtrends.xlsx", header=0)

from pytrends.request import TrendReq

pytrends = TrendReq(tz=360, timeout=(10,25))
df = pd.DataFrame()
count = 0

for index, row in f.iterrows():
    print(f"Buscando: {row['palabra']}")
    
    t = "all"
    pytrends.build_payload([row["palabra"]], cat=0, timeframe=t, geo=row["origen"])
    
    data = pd.DataFrame(pytrends.interest_over_time())
    data.drop("isPartial", axis=1, inplace=True)
    df = pd.merge(df, data, how='outer', left_index=True, right_index=True)
    
    df.to_csv(f"{main}/raw/GTrends.csv")
    
    # Para evitar problemas de RateLimit, hacemos un "sleep" cada 5 palabras.
    count = count+1
    if count==5 : print("Sleeping 60 segs"); time.sleep(60); count=0