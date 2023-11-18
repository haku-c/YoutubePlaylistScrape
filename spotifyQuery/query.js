const axios = require('axios');
const qs = require('qs');
require('dotenv').config();

const clientId = process.env.SPOTIFY_CLIENT_ID;
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

const authToken = Buffer.from(`${clientId}:${clientSecret}`, 'utf-8').toString('base64');

const getToken = async () => {
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

const getSongIds = async (q) => {
  const token = await getToken()
  const response = await axios({
    method: 'get',
    url: 'https://api.spotify.com/v1/search?q=' + q,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }).then((result) => {
    spotifyResponse = result.data
    let songId = spotifyResponse.tracks.items[0].id
    let songName = spotifyResponse.tracks.items[0].name
    let album = spotifyResponse.tracks.items[0].album.name
    let albumId = spotifyResponse.tracks.items[0].album.id
    let duration = spotifyResponse.tracks.items[0].duration_ms
    let release = spotifyResponse.tracks.items[0].album.release_date
    let artists = []
    let artistId = []
    artistData = spotifyResponse.tracks.items[0].artists
    for (let i = 0; i < artistData.length; i++) {
      artists.push(artistData[i].name)
      console.log(artistData[i].name)

    }
    console.log(songName + ", " + album + ", " + artists[0])

  })
}

getSongIds('q%3Dtrack%3AInto%20Youartist%3AAriana%20Grande%20&type=track&limit=3')
