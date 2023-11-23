import pandas as pd
import urllib.parse
import math

data = pd.read_csv("csvs/finalSorted.csv", sep=";")
uris = "spotify:track:" + data["Id"]

start = 0
for i in range(1, 1 + math.ceil(len(uris) / 100)):
    set = uris[start : (min(len(uris), i * 100))]
    start = i * 100
    df = pd.DataFrame(set)
    df.to_csv(
        "uris/uriSet" + str(i) + ".csv",
        index=False,
    )
