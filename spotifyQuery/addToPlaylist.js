require('dotenv').config();
const axios = require('axios');
const fs = require('fs');
const csvParser = require("csv-parser");
const express = require("express")
const qs = require('qs');

const clientId = process.env.SPOTIFY_CLIENT_ID;
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;
const playlistId = process.env.PLAYLIST_ID;


async function getToken(code, redirectUri) {
  const authToken = Buffer.from(`${clientId}:${clientSecret}`, 'utf-8').toString('base64');
  try {
    //make post request to SPOTIFY API for access token, sending relavent info
    const tokenUrl = 'https://accounts.spotify.com/api/token';
    const data = qs.stringify({ 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirectUri });

    const response = await axios.post(tokenUrl, data, {
      headers: {
        'Authorization': `Basic ${authToken}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data.access_token;
  } catch (error) {
    console.log(error);
  }
}

async function addSongsToPlaylist(urls, token) {
  const add = await axios({
    method: 'POST',
    url: `https://api.spotify.com/v1/playlists/${playlistId}/tracks?uris=${urls}`,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': "application/json"
    },
    data: JSON.stringify({ uris: urls }),
  })
}

async function addSongs(queryPath, token) {
  urls = []
  fs.createReadStream(queryPath)
    .pipe(csvParser())
    .on("data", (data) => {
      urls.push(data["Id"])
    })
    .on("end", async () => {
      addSongsToPlaylist((urls), token)
    });
}


const app = express()
var redirectUri = 'http://localhost:8888/callback';

app.listen(8888, () => {
  console.log("App is listening on port 8888!\n");
});

app.get('/login', function (req, res) {

  var scope = 'playlist-modify-public';

  res.redirect('https://accounts.spotify.com/authorize?' +
    qs.stringify({
      response_type: 'code',
      client_id: clientId,
      scope: scope,
      redirect_uri: redirectUri,
    }));
});

app.get('/callback', async function (req, res) {
  var code = req.query.code
  var newToken = await getToken(code, redirectUri)
  addSongs("uris/uriSet8.csv", newToken)
});

