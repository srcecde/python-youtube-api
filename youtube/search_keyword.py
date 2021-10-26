# -*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import os
from collections import defaultdict
import logging
import json
from utils.helper import openURL, create_df
from config import YOUTUBE_SEARCH_URL, SAVE_PATH

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SearchVideo:
    def __init__(self, searchTerm, maxResults, regionCode, key):
        self.save_path = f"{SAVE_PATH}/search-keyword-csv"
        self.videos = defaultdict(list)
        self.channels = defaultdict(list)
        self.playlists = defaultdict(list)
        self.params = {
            "q": searchTerm,
            "part": "id,snippet",
            "maxResults": maxResults,
            "regionCode": regionCode,
            "key": key,
        }
        os.makedirs(self.save_path, exist_ok=True)

    def load_search_res(self, search_response):
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos["title"].append(search_result["snippet"]["title"])
                self.videos["description"].append(
                    search_result["snippet"]["description"]
                )
                self.videos["publishedAt"].append(
                    search_result["snippet"]["publishedAt"]
                )
                self.videos["channelId"].append(search_result["snippet"]["channelId"])
                self.videos["videoId"].append(search_result["id"]["videoId"])
                self.videos["channelTitle"].append(
                    search_result["snippet"]["channelTitle"]
                )
                self.videos["liveBroadcastContent"].append(
                    search_result["snippet"]["liveBroadcastContent"]
                )

            elif search_result["id"]["kind"] == "youtube#channel":
                self.channels["title"].append(search_result["snippet"]["title"])
                self.channels["description"].append(
                    search_result["snippet"]["description"]
                )
                self.channels["publishedAt"].append(
                    search_result["snippet"]["publishedAt"]
                )
                self.channels["channelId"].append(search_result["snippet"]["channelId"])

            elif search_result["id"]["kind"] == "youtube#playlist":
                self.playlists["title"].append(search_result["snippet"]["title"])
                self.playlists["description"].append(
                    search_result["snippet"]["description"]
                )
                self.playlists["publishedAt"].append(
                    search_result["snippet"]["publishedAt"]
                )
                self.playlists["channelId"].append(
                    search_result["snippet"]["channelId"]
                )
                self.playlists["playlistId"].append(search_result["id"]["playlistId"])

    def get_channel_videos(self):
        logger.info("Fetching data")
        url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        try:
            if "error" in url_response:
                logger.error(f"{url_response['error']['message']}")
                raise Exception("The request cannot be completed!")
        except Exception as e:
            logger.error(e)
            return False
        logger.info("Parsing data")
        self.load_search_res(url_response)

        if nextPageToken:
            logger.info("Found paginated response")
            logger.info("Fetching paginated response & parsing")
            while nextPageToken:
                self.params.update({"pageToken": nextPageToken})
                url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
                nextPageToken = url_response.get("nextPageToken")
                self.load_search_res(url_response)
        logger.info(f"Saving data as CSV at {self.save_path}")
        self.save_data()
        logger.info("Saved data successfully")

    def save_data(self):
        create_df(self.videos, f"{self.save_path}/search_term_videos.csv")
        create_df(self.channels, f"{self.save_path}/search_term_channel.csv")
        create_df(self.playlists, f"{self.save_path}/search_term_playlist.csv")
