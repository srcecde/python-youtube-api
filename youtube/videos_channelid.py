#-*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import os

from collections import defaultdict
import json
import pandas as pd
from utils.helper import openURL
from config import YOUTUBE_SEARCH_URL, SAVE_PATH


class channelVideo:
    def __init__(self, channelid, maxResults, key, save_folder=None):
        self.videos = defaultdict(list)
        if save_folder:
            self.save_folder = save_folder + "/"
        else:
            self.save_folder = ""
        self.params = {
                   'part': 'id,snippet',
                   'channelId': channelid, 
                   'maxResults': maxResults,
                   'key': key
               }

    def load_channel_videos(self, search_response):
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos["title"].append(search_result["snippet"]["title"])
                self.videos["description"].append(search_result["snippet"]["description"])
                self.videos["publishedAt"].append(search_result["snippet"]["publishedAt"])
                self.videos["videoId"].append(search_result["id"]["videoId"])
                self.videos["liveBroadcastContent"].append(search_result["snippet"]["liveBroadcastContent"])

    def get_channel_videos(self):
        url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_channel_videos(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_channel_videos(url_response)

        self.create_df()

    def create_df(self):
        if os.path.exists(SAVE_PATH+self.save_folder) == False:
            os.makedirs(SAVE_PATH+self.save_folder)

        df = pd.DataFrame().from_dict(self.videos)
        df.to_csv(SAVE_PATH+self.save_folder+"search_channel_id.csv")

