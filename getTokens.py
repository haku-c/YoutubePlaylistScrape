# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
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

    pageTokens = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=PLAYLIST_ID,
        maxResults=50,
    )
    response = request.execute()
    nextPageToken = response.get("nextPageToken")
    pageTokens.append(nextPageToken)

    while nextPageToken is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=nextPageToken,
        )
        response = request.execute()
        nextPageToken = response.get("nextPageToken")
        if nextPageToken is not None:
            pageTokens.append(nextPageToken)

    with open("tokens.csv", "w") as f:
        for token in pageTokens:
            f.write(f"{token},\n")


if __name__ == "__main__":
    main()
