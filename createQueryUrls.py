import pandas as pd
import urllib.parse

data = pd.read_csv("data/songCSVS/parsedSpotify.csv")
dataNoMatches = pd.read_csv("data/songCSVS/parsedNoMatches.csv")


def query(data, path, genQuery):
    data["Title"] = data["Title"].apply(lambda x: x.strip())
    data["FeaturedArtist"] = data["FeaturedArtist"].fillna("")
    data["FeaturedArtist"] = data["FeaturedArtist"].apply(lambda x: x.strip())
    data["RemixArtist"] = data["RemixArtist"].fillna("")
    data["RemixArtist"] = data["RemixArtist"].apply(lambda x: x.strip())
    data["Artist"] = data["Artist"].apply(lambda x: x.strip())
    queries = genQuery(data)
    queries = queries.apply(lambda x: x.strip())
    queries = list(map(urllib.parse.quote, queries))
    queries = list(map(lambda q: q + "&type=track&limit=20", queries))

    qdf = pd.DataFrame(queries, columns=["url"])
    qdf = pd.concat([data["Title"], qdf], axis=1)
    qdf = pd.concat([data["Artist"], qdf], axis=1)
    qdf = pd.concat([data["RemixArtist"], qdf], axis=1)
    qdf = pd.concat([data["FeaturedArtist"], qdf], axis=1)
    qdf = pd.concat([data["Index"], qdf], axis=1)
    qdf.to_csv(
        path,
        index=False,
    )


def quotesQuery(data):
    return (
        "track: "
        + data["Title"]
        + ' artist: "'
        + data["Artist"]
        + '" '
        + data["FeaturedArtist"]
    )


def noQuotesQuery(data):
    return (
        "q=track: "
        + data["Title"]
        + " artist: "
        + data["Artist"]
        + " "
        + data["FeaturedArtist"]
        + " "
        + data["RemixArtist"]
    )


def noqQuery(data):
    return "track: " + data["Title"] + " " + data["RemixArtist"]


# query(data, "spotifyQuery/queries.csv", quotesQuery)
# query(dataNoMatches, "spotifyQuery/queriesNone.csv", noQuotesQuery)
query(dataNoMatches, "spotifyQuery/queriesNone.csv", noqQuery)
