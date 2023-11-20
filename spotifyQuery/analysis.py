import pandas as pd

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

notExact2 = pd.read_csv("csvs/notExact2.csv", sep=";")
notExact3 = pd.read_csv("csvs/notExact3.csv", sep=";")
notExact4 = pd.read_csv("csvs/notExact4.csv", sep=";")

intersection = set(notExact2["Index"]).intersection(set(notExact3["Index"]))

intersection = set(intersection).intersection(set(notExact4["Index"]))
indices = list(intersection)
indices.sort()
# 33 songs
notExactMatched = data.loc[indices]

exact2 = pd.read_csv("csvs/exactMatches2.csv", sep=";")
exact3 = pd.read_csv("csvs/exactMatches3.csv", sep=";")
exact4 = pd.read_csv("csvs/exactMatches4.csv", sep=";")

union = pd.concat([exact2, exact3, exact4], ignore_index=True)
union = union.drop_duplicates(ignore_index=True)
union.to_csv("csvs/unioned.csv", sep=";")
