#-*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

from collections import defaultdict
import json
import pandas as pd
from utils.helper import openURL
from config import YOUTUBE_SEARCH_URL, SAVE_PATH

class searchVideo:
    def __init__(self, searchTerm, maxResults, regionCode, key):
        self.videos = defaultdict(list)
        self.channels = defaultdict(list)
        self.playlists = defaultdict(list)
        self.params = {
                    'q': searchTerm,
                    'part': 'id,snippet',
                    'maxResults': maxResults,
                    'regionCode': regionCode,
                    'key': key
                }

    def load_search_res(self, search_response):
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos["title"].append(search_result["snippet"]["title"])
                self.videos["description"].append(search_result["snippet"]["description"])
                self.videos["publishedAt"].append(search_result["snippet"]["publishedAt"])
                self.videos["channelId"].append(search_result["snippet"]["channelId"])
                self.videos["videoId"].append(search_result["id"]["videoId"])
                self.videos["channelTitle"].append(search_result["snippet"]["channelTitle"])
                self.videos["liveBroadcastContent"].append(search_result["snippet"]["liveBroadcastContent"])
              
            elif search_result["id"]["kind"] == "youtube#channel":
                self.channels["title"].append(search_result["snippet"]["title"])
                self.channels["description"].append(search_result["snippet"]["description"])
                self.channels["publishedAt"].append(search_result["snippet"]["publishedAt"])
                self.channels["channelId"].append(search_result["snippet"]["channelId"])
              
            elif search_result["id"]["kind"] == "youtube#playlist":
                self.playlists["title"].append(search_result["snippet"]["title"])
                self.playlists["description"].append(search_result["snippet"]["description"])
                self.playlists["publishedAt"].append(search_result["snippet"]["publishedAt"])
                self.playlists["channelId"].append(search_result["snippet"]["channelId"])
                self.playlists["playlistId"].append(search_result["id"]["playlistId"])


    def get_channel_videos(self):
        url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_search_res(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_search_res(url_response)
        self.create_df()

    def create_df(self):
        df = pd.DataFrame().from_dict(self.videos)
        df.to_csv(SAVE_PATH+"search_term_videos.csv")

        df = pd.DataFrame().from_dict(self.channels)
        df.to_csv(SAVE_PATH+"search_term_channel.csv")

        df = pd.DataFrame().from_dict(self.playlists)
        df.to_csv(SAVE_PATH+"search_term_playlist.csv")

