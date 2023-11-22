import pandas as pd

"""
# find songs which are not queried across any search
notMatched2 = pd.read_csv("csvs/notMatched2.txt", sep=":", names=["Index", "Query"])
notMatched3 = pd.read_csv("csvs/notMatched3.txt", sep=":", names=["Index", "Query"])
notMatched4 = pd.read_csv("csvs/notMatched4.txt", sep=":", names=["Index", "Query"])

intersection = set(notMatched2["Index"]).intersection(set(notMatched3["Index"]))

intersection = set(intersection).intersection(set(notMatched4["Index"]))
indices = list(intersection)
indices.sort()
data = pd.read_csv("./queries.csv")
# 68 songs
notFound = data.loc[indices]

exact2 = pd.read_csv("csvs/exactMatches2.csv", sep=";")
exact3 = pd.read_csv("csvs/exactMatches3.csv", sep=";")
exact4 = pd.read_csv("csvs/exactMatches4.csv", sep=";")

union = pd.concat([exact2, exact3, exact4], ignore_index=True)
union = union.drop_duplicates(ignore_index=True)
union.to_csv("csvs/unioned.csv", sep=";")
"""
data = pd.read_csv("../data/songCSVs/parsedSpotify.csv")
missing = pd.read_csv("csvs/final.csv", sep=";")
all = set(range(0, 762))
missingInd = all.difference(set(missing["Index"]))
missingInd = list(missingInd)
missingInd.sort()
notFound = data.loc[missingInd]
notFound.to_csv("../data/songCSVs/parsedNoMatches.csv")
