# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

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

    pageTokens = []

    with open("tokens.csv") as tokens:
        reader = csv.reader(tokens)
        for token in reader:
            pageTokens.append(token[0])

    i = 1
    for nextPageToken in pageTokens:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=nextPageToken,
            fields="items(snippet/publishedAt,snippet/channelId,snippet/title, snippet/videoOwnerChannelTitle, snippet/videoOwnerChannelId, contentDetails,contentDetails.note)",
        )
        response = request.execute()
        with open("data/songJsons/response" + str(i) + ".json", "w") as file:
            json.dump(response, file)
        i = i + 1


if __name__ == "__main__":
    main()
