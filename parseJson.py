import pandas as pd
import os

pd.options.mode.chained_assignment = None


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

# select and parse songs that are generated by Youtube Music
ytMusicSongs = songdf[songdf["Channel"].str.match("(.+) - Topic")]
ytMusicArtists = ytMusicSongs["Channel"].str.extract("(.[^-]+)")
ytMusicSongs["Artist"] = ytMusicArtists

# select and parse songs uploaded by music channels
songsToParse = songdf[
    (songdf["Title"].str.match(r"^(.+) - (.+)$"))
    & (songdf["Channel"] != "NoCopyrightSounds")
    & (songdf["Channel"] != "Monstercat Uncaged")
]
split = songsToParse["Title"].str.extract(r"(?P<Artist>.+) [-] (?P<Title>.+)")
songsToParse["Artist"] = split["Artist"]
songsToParse["Title"] = split["Title"]

# artist specific fixes
ellisCovers = songsToParse[songsToParse["Title"] == "Cover"]
songsToParse.loc[songsToParse["Title"] == "Cover", "Title"] = ellisCovers["Title"]
songsToParse.loc[songsToParse["Title"] == "Cover", "Artist"] = "Lucy Ellis"

pinkzebra = songsToParse[songsToParse["Title"] == "Upbeat Song for Videos"]
songsToParse.loc[
    songsToParse["Title"] == "Upbeat Song for Videos", "Artist"
] = "Pinkzebra"
songsToParse.loc[
    songsToParse["Title"] == "Upbeat Song for Videos", "Title"
] = pinkzebra["Artist"].str.extract(r"^(?P<Artist2>\w+) (?P<Title2>.+)$")["Title2"]

songsToParse.loc[songsToParse["Artist"] == "【EDM】Eastside", "Artist"] = "Eastside"
songsToParse.loc[songsToParse["Artist"] == "Reboot", "Artist"] = songsToParse.loc[
    songsToParse["Artist"] == "Reboot"
]["Title"]
songsToParse.loc[
    songsToParse["Title"] == "Approaching Nirvana & BigGiantCircles", "Title"
] = "Reboot"

# some songs use an alternate hyphen
songsToParse2 = songdf[songdf["Title"].str.match(r"(.+) – (.+)")]
split = songsToParse2["Title"].str.extract(r"(?P<Artist>.+) – (?P<Title>.+)")
songsToParse2["Artist"] = split["Artist"]
songsToParse2["Title"] = split["Title"]

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

outliers = songdf[
    ~(songdf["Title"].str.match(r"^(.+) - (.+)$"))
    & ~(songdf["Title"].str.match(r"(.+) – (.+)"))
    & (songdf["Channel"] != "NoCopyrightSounds")
    & (songdf["Channel"] != "Monstercat Uncaged")
    & ~(songdf["Channel"].str.match("(.+) - Topic"))
]
outliers["Artist"] = outliers["Channel"]

parsed = pd.DataFrame()
parsed = pd.concat([parsed, ytMusicSongs])
parsed = pd.concat([parsed, songsToParse])
parsed = pd.concat([parsed, songsToParse2])
parsed = pd.concat([parsed, ncs])
parsed = pd.concat([parsed, monsterCatSongs])
parsed = pd.concat([parsed, outliers])

parsed = parsed.sort_values(by="DateAdded", ascending=False, ignore_index=True)

# trim the ISO Date to only be YYYY-MM-DD.
col = parsed["DateAdded"]
col = col.apply(trimDates)
parsed["DateAdded"] = col

# write to csv preserving non-English characters correctly
parsed.to_csv("data/songCSVs/parsed.csv", encoding="utf-8-sig")
