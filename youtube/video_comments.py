# -*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import os
from collections import defaultdict
import json
import logging
from utils.helper import openURL, create_df
from config import YOUTUBE_COMMENT_URL, SAVE_PATH

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class VideoComment:
    def __init__(self, maxResults, videoId, key):
        self.save_path = f"{SAVE_PATH}/video-comments-csv"
        self.comments = defaultdict(list)
        self.replies = defaultdict(list)
        self.params = {
            "part": "snippet,replies",
            "maxResults": maxResults,
            "videoId": videoId,
            "textFormat": "plainText",
            "key": key,
        }
        os.makedirs(self.save_path, exist_ok=True)

    def load_comments(self, mat):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            self.comments["id"].append(comment["id"])
            self.comments["comment"].append(comment["snippet"]["textDisplay"])
            self.comments["author"].append(comment["snippet"]["authorDisplayName"])
            self.comments["likecount"].append(comment["snippet"]["likeCount"])
            self.comments["publishedAt"].append(comment["snippet"]["publishedAt"])

            if "replies" in item.keys():
                for reply in item["replies"]["comments"]:
                    self.replies["parentId"].append(reply["snippet"]["parentId"])
                    self.replies["authorDisplayName"].append(
                        reply["snippet"]["authorDisplayName"]
                    )
                    self.replies["replyComment"].append(reply["snippet"]["textDisplay"])
                    self.replies["publishedAt"].append(reply["snippet"]["publishedAt"])
                    self.replies["likeCount"].append(reply["snippet"]["likeCount"])

    def get_video_comments(self):
        logger.info("Fetching data")
        url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        try:
            if "error" in url_response:
                logger.error(f"{url_response['error']['message']}")
                raise Exception("The request cannot be completed!")
        except Exception as e:
            logger.error(e)
            return False
        self.load_comments(url_response)

        if nextPageToken:
            logger.info("Found paginated response")
            logger.info("Fetching paginated response & parsing")
            while nextPageToken:
                self.params.update({"pageToken": nextPageToken})
                url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
                nextPageToken = url_response.get("nextPageToken")
                self.load_comments(url_response)
        logger.info(f"Saving data as CSV at {self.save_path}")
        self.save_data()
        logger.info("Saved data successfully")

    def save_data(self):
        create_df(self.comments, f"{self.save_path}/parent_video_comment.csv")
        create_df(self.replies, f"{self.save_path}/comment_reply.csv")
