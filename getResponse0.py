# used to retrieve the first page of results from playlist

import os
import json
import csv

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from config import CLIENT_ID, PLAYLIST_ID

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = CLIENT_ID

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=PLAYLIST_ID,
        maxResults=50,
        fields="items(snippet/publishedAt,snippet/channelId,snippet/title, snippet/videoOwnerChannelTitle, snippet/videoOwnerChannelId, contentDetails,contentDetails.note)",
    )
    response = request.execute()
    with open("data/songJsons/response0" + ".json", "w") as file:
        json.dump(response, file)


if __name__ == "__main__":
    main()
