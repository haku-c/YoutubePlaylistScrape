import pandas as pd
import urllib.parse
from config import SPOTIFY_KEY

data = pd.read_csv("data/songCSVS/parsed.csv")
queries = "q=track:" + data["Title"] + "artist:" + data["Artist"]
queries = list(map(urllib.parse.quote, queries))
queries = list(map(lambda q: q + "&type=track&limit=3", queries))

qdf = pd.DataFrame(queries, columns=["url"])
qdf = pd.concat([data["Title"], qdf], axis=1)
qdf = pd.concat([data["Artist"], qdf], axis=1)
qdf.to_csv(
    "spotifyQuery/queries.csv",
    index=False,
)
