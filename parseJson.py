import pandas as pd
import os


def trimDates(date):
    return date[0:10]


songdf = pd.DataFrame()

for file in sorted(os.listdir("data/songJsons"), key=len):
    data = pd.read_json("data/songJsons/" + file)
    data = pd.json_normalize(data["items"])
    extract = data[
        ["snippet.title", "snippet.videoOwnerChannelTitle", "snippet.publishedAt"]
    ]
    songdf = pd.concat([songdf, extract], ignore_index=True)

# rename columns
songdf = songdf.rename(
    columns={
        "snippet.title": "Title",
        "snippet.videoOwnerChannelTitle": "Channel",
        "snippet.publishedAt": "DateAdded",
    }
)

# remove deleted or private videos
songdf = songdf.dropna()
songdf = songdf.reset_index(drop=True)

# trim the ISO Date to only be YYYY-MM-DD.
col = songdf["DateAdded"]
col = col.apply(trimDates)
songdf["DateAdded"] = col

# select and parse songs that are generated by Youtube Music
ytMusicSongs = songdf[songdf["Channel"].str.match("(.+) - Topic")]
ytMusicArtists = ytMusicSongs["Channel"].str.extract("(.[^-]+)")
ytMusicSongs["Artists"] = ytMusicArtists

# select and parse songs uploaded by music channels
songsToParse = songdf[
    (songdf["Title"].str.match(r"^(.+) - (.+)$"))
    & (songdf["Channel"] != "NoCopyrightSounds")
    & (songdf["Channel"] != "Monstercat Uncaged")
]
split = songsToParse["Title"].str.extract(r"(?P<Artist>.+) [-] (?P<Title>.+)")
songsToParse["Artists"] = split["Artist"]
songsToParse["Title"] = split["Title"]

monsterCatSongs = songdf[songdf["Channel"] == "Monstercat Uncaged"]
split = monsterCatSongs["Title"].str.extract(r"(?P<Artist>.+) - (?P<Title>.+)")
# Change songs which have the genre preceding in the title
split["Title"] = split["Title"].str.extract(r"(?P<First>(.+) (?=\[)|(?!(.+ \[)).+\))")[
    "First"
]
split["ArtistParsed"] = split["Artist"].str.extract(r"(?P<Names>(?<=- ).+|^[^\[\]]*$)")[
    "Names"
]
monsterCatSongs["Title"] = split["Title"]
monsterCatSongs["Artist"] = split["ArtistParsed"]

ncs = songdf[songdf["Channel"] == "NoCopyrightSounds"]
split = ncs["Title"].str.extract(r"^(?P<Artist>.+) - (?P<Title>.+)$")
detailedSongs = split[split["Title"] == "Copyright Free Music"]
detailedSongs = detailedSongs["Artist"].str.extract(
    r"^(?P<Artist>.+) - (?P<Title>[^\|]+)"
)
split[split["Title"] == "Copyright Free Music"] = detailedSongs
split["Title"] = split["Title"].str.extract(r"^([^\[]+)")
ncs["Title"] = split["Title"]
ncs["Artist"] = split["Artist"]

# write to csv preserving non-English characters correctly
songdf.to_csv("data/songCSVs/initial.csv", encoding="utf-8-sig")

query = songdf[
    ~(songdf["Title"].str.match(r"^(.+) - (.+)$"))
    & ~(songdf["Title"].str.match(r"(.+) – (.+)"))
    & (songdf["Channel"] != "NoCopyrightSounds")
    & (songdf["Channel"] != "Monstercat Uncaged")
    & ~(songdf["Channel"].str.match("(.+) - Topic"))
]
