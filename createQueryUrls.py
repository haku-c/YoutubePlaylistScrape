import pandas as pd
import urllib.parse
from config import SPOTIFY_KEY

data = pd.read_csv("data/songCSVS/parsedSpotify.csv")
data["Title"] = data["Title"].apply(lambda x: x.strip())
data["FeaturedArtist"] = data["FeaturedArtist"].fillna("")
data["FeaturedArtist"] = data["FeaturedArtist"].apply(lambda x: x.strip())
data["RemixArtist"] = data["RemixArtist"].fillna("")
data["RemixArtist"] = data["RemixArtist"].apply(lambda x: x.strip())
data["Artist"] = data["Artist"].apply(lambda x: x.strip())
queries = (
    "q=track: "
    + data["Title"]
    + " artist: "
    + data["Artist"]
    + " "
    + data["FeaturedArtist"]
)
queries = queries.apply(lambda x: x.strip())
queries = list(map(urllib.parse.quote, queries))
queries = list(map(lambda q: q + "&type=track&limit=10", queries))

qdf = pd.DataFrame(queries, columns=["url"])
qdf = pd.concat([data["Title"], qdf], axis=1)
qdf = pd.concat([data["Artist"], qdf], axis=1)
qdf = pd.concat([data["RemixArtist"], qdf], axis=1)
qdf = pd.concat([data["FeaturedArtist"], qdf], axis=1)
qdf.to_csv(
    "spotifyQuery/queries.csv",
    index=False,
)
