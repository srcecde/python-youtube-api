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


class ChannelVideo:
    def __init__(self, channelid, maxResults, key):
        self.save_path = f"{SAVE_PATH}/video-channel-csv"
        self.videos = defaultdict(list)
        self.params = {
            "part": "id,snippet",
            "channelId": channelid,
            "maxResults": maxResults,
            "key": key,
        }
        os.makedirs(self.save_path, exist_ok=True)

    def load_channel_videos(self, search_response):
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos["title"].append(search_result["snippet"]["title"])
                self.videos["description"].append(
                    search_result["snippet"]["description"]
                )
                self.videos["publishedAt"].append(
                    search_result["snippet"]["publishedAt"]
                )
                self.videos["videoId"].append(search_result["id"]["videoId"])
                self.videos["liveBroadcastContent"].append(
                    search_result["snippet"]["liveBroadcastContent"]
                )

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
        self.load_channel_videos(url_response)

        if nextPageToken:
            logger.info("Found paginated response")
            logger.info("Fetching paginated response & parsing")
            while nextPageToken:
                self.params.update({"pageToken": nextPageToken})
                url_response = json.loads(openURL(YOUTUBE_SEARCH_URL, self.params))
                nextPageToken = url_response.get("nextPageToken")
                self.load_channel_videos(url_response)
        logger.info(f"Saving data as CSV at {self.save_path}")
        self.save_data()
        logger.info("Saved data successfully")

    def save_data(self):
        create_df(self.videos, f"{self.save_path}/search_channel_id.csv")
