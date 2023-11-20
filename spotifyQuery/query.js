require('dotenv').config();
const axios = require('axios');
const qs = require('qs');
const fs = require('fs');
const Fuse = require('fuse.js');
const tqdm = require('tqdm');
const csvParser = require("csv-parser");

const clientId = process.env.SPOTIFY_CLIENT_ID;
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

const authToken = Buffer.from(`${clientId}:${clientSecret}`, 'utf-8').toString('base64');

async function getToken() {
  try {
    //make post request to SPOTIFY API for access token, sending relavent info
    const tokenUrl = 'https://accounts.spotify.com/api/token';
    const data = qs.stringify({ 'grant_type': 'client_credentials' });

    const response = await axios.post(tokenUrl, data, {
      headers: {
        'Authorization': `Basic ${authToken}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    // console.log(response.data.access_token);
    return response.data.access_token;
  } catch (error) {
    console.log(error);
  }
}

async function getSongIds(q, qArtist, qTitle, qFeatured) {
  const token = await getToken()
  const response = await axios({
    method: 'get',
    url: 'https://api.spotify.com/v1/search?q=' + q,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }).then((result) => {
    spotifyResponse = result.data
    // console.log(spotifyResponse.tracks)
    res = []
    for (let i = 0; i < spotifyResponse.tracks.items.length; i++) {
      let songId = spotifyResponse.tracks.items[i].id
      let songName = spotifyResponse.tracks.items[i].name
      let artistData = spotifyResponse.tracks.items[i].artists
      artists = ""
      for (let j = 0; j < artistData.length; j++) {
        artists = artists + " " + (artistData[j].name)
      }
      res.push({ title: songName, artist: artists.trim(), id: songId })
    }
    if (qFeatured != "") {
      artistStr = qArtist + " " + qFeatured
    } else {
      artistStr = qArtist
    }
    const fuse = new Fuse(res, {
      keys: [{ name: 'title' }, { name: 'artist' }],
      includeScore: true,
      includeMatches: true,
      shouldSort: true,
    })
    const fuseRes = fuse.search({ $and: [{ title: qTitle }, { artist: artistStr }] })
    // console.log(fuseRes)
    return fuseRes
  })
  return response
}

incorrect = []
matchedSongs = []
notExact = []

var result = [];
fs.createReadStream("./queries.csv")
  .pipe(csvParser())
  .on("data", (data) => {
    result.push(data);
  })
  .on("end", async () => {
    for (let i of tqdm([...Array(result.length).keys()])) {
      // for (let i of tqdm([...Array(50).keys()])) {
      // let i = 38
      data = result[i]
      const res = await getSongIds(data.url, data.Artist, data.Title, data.FeaturedArtist)
      if (res.length == 0) {
        incorrect.push(i + ": " + data.Artist + "|" + data.Title)
      } else if (res[0].score > 0.05) {
        notExact.push({ index: i, query: data.Artist + "|" + data.Title, response: res[0] })
      } else {
        matchedSongs.push({ index: i, query: data.Artist + "|" + data.Title, response: res[0] })
      }
    }
    for (let inc of incorrect) {
      console.log(inc)
    }
    console.log("number incorrect: " + incorrect.length)
    console.log("-------")
    console.log("number not exactly matching: " + notExact.length)
    const csvString = [
      [
        "Index",
        "Query",
        "Title",
        "Artist",
        "Score"
      ],
      ...notExact.map(item =>
        [
          item.index,
          item.query,
          item.response.item.title,
          item.response.item.artist,
          item.response.score,
        ])
    ]
      .map(entry => entry.join(";"))
      .join("\n")

    fs.writeFile("./csvs/notExact4.csv", csvString, function (err) {
      if (err) {
        return console.log(err);
      }
      console.log("The file was saved!");
    });

    const songsString = [
      [
        "Index",
        "Query",
        "Title",
        "Artist",
        "Score",
        "Id"
      ],
      ...matchedSongs.map(item =>
        [
          item.index,
          item.query,
          item.response.item.title,
          item.response.item.artist,
          item.response.score,
          item.response.item.id
        ])
    ]
      .map(entry => entry.join(";"))
      .join("\n")

    fs.writeFile("./csvs/exactMatches4.csv", songsString, function (err) {
      if (err) {
        return console.log(err);
      }
      console.log("The file was saved!");
    });
  });


