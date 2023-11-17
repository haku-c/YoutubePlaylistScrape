require('dotenv').config()
const axios = require('axios');
const qs = require('qs');

const clientId = process.env.SPOTIFY_CLIENT_ID
const clientSecret = process.env.SPOTIFY_SECRET_ID

const authToken = Buffer.from(`${clientId}:${clientSecret}`, 'utf-8').toString('base64');

const getToken = async () => {
  try {
    //make post request to SPOTIFY API for access token, sending relavent info
    const tokenUrl = 'https://accounts.spotify.com/api/token';
    const data = qs.q({ 'grant_type': 'client_credentials' });

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
    baseUrl: 'https://api.spotify.com/v1/search?q',
    url: q,
    headers: {
      'Authorization': token,
    }
  }).then((result) => {

  })
} 
