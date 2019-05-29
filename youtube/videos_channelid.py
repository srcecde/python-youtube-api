"""
-*- coding: utf-8 -*-
========================
Python YouTube v3 API
========================

Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com

========================
"""

import json
import requests
import pandas as pd
from config import YOUTUBE_SEARCH_URL, SAVE_PATH


class channelVideo:
    def __init__(self, channelid, maxResults, key):
        self.videos = []
        self.params = {
                   'part': 'id,snippet',
                   'channelId': channelid,
                   'maxResults': maxResults,
                   'key': key
               }

    def openURL(self, URL, params):
        r = requests.get(URL + "?", params=params)
        return r.text

    def load_channel_videos(self, search_response):
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos.extend([[search_result["snippet"]["title"],  
                                    search_result["snippet"]["description"], 
                                    search_result["snippet"]["publishedAt"],
                                    search_result["id"]["videoId"],
                                    search_result["snippet"]["liveBroadcastContent"]
                                    ]])

    def get_channel_videos(self):
        url_response = json.loads(self.openURL(YOUTUBE_SEARCH_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_channel_videos(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(self.openURL(YOUTUBE_SEARCH_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_channel_videos(url_response)

        self.create_df()

    def create_df(self):
        columns = ["title", "description", "published", "video_id", "live_broadcast"]
        df = pd.DataFrame(self.videos, columns=columns)
        df.to_csv(SAVE_PATH+"search_channel_id.csv")
