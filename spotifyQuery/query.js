require('dotenv').config();
const axios = require('axios');
const qs = require('qs');
const fs = require('fs');
const Fuse = require('fuse.js')
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
    return response.data.access_token;
    //console.log(response.data.access_token);   
  } catch (error) {
    console.log(error);
  }
}

async function getSongIds(q, qArtist, qTitle) {
  const token = await getToken()
  const response = await axios({
    method: 'get',
    url: 'https://api.spotify.com/v1/search?q=' + q,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }).then((result) => {
    spotifyResponse = result.data
    res = []
    for (let i = 0; i < spotifyResponse.tracks.items.length; i++) {
      let songId = spotifyResponse.tracks.items[i].id
      let songName = spotifyResponse.tracks.items[i].name
      let artistData = spotifyResponse.tracks.items[i].artists
      artists = ""
      for (let j = 0; j < artistData.length; j++) {
        artists = artists + " " + (artistData[j].name)
      }
      res.push({ title: songName, artist: artists, id: songId })
    }
    const fuse = new Fuse(res, {
      keys: [{ name: 'title' }, { name: 'artist' }],
      includeScore: true,
      includeMatches: true,
      threshold: 0.4,
      shouldSort: true,
    })
    searchTerm = qTitle + " " + qArtist
    const fuseRes = fuse.search(searchTerm)
    console.log(fuseRes[0])
    return fuseRes[0]
  })
  return response
}

incorrect = []
correctSongIds = []

var result = [];
fs.createReadStream("./queries.csv")
  .pipe(csvParser())
  .on("data", (data) => {
    result.push(data);
  })
  .on("end", async () => {
    for (let i = 0; i < 2; i++) {
      data = result[i]
      const res = await getSongIds(data.url, data.Artist, data.Title)
      console.log(res)
    }
  });


