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
from config import YOUTUBE_COMMENT_URL, SAVE_PATH


class VideoComment:
    def __init__(self, maxResults, videoId, key, search_terms, save_folder=None):
        self.comments = defaultdict(list)
        self.replies = defaultdict(list)
        if save_folder:
            self.save_folder = save_folder + "/"
        else:
            self.save_folder = ""
        self.params = {
                    'part': 'snippet,replies',
                    'maxResults': maxResults, 
                    'videoId': videoId,
                    'textFormat': 'plainText',
                    'searchTerms': search_terms,
                    'key': key
                }

    def load_comments(self, mat):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            self.comments["videoId"].append(comment["id"])
            self.comments["comment"].append(comment["snippet"]["textDisplay"])
            self.comments["author"].append(comment["snippet"]["authorDisplayName"])
            self.comments["likecount"].append(comment["snippet"]["likeCount"])
            self.comments["publishedAt"].append(comment["snippet"]["publishedAt"])

            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    self.replies["parentId"].append(reply["snippet"]["parentId"])
                    self.replies["authorDisplayName"].append(reply['snippet']['authorDisplayName'])
                    self.replies["replyComment"].append(reply["snippet"]["textDisplay"])
                    self.replies["publishedAt"].append(reply["snippet"]["publishedAt"])
                    self.replies["likeCount"].append(reply["snippet"]["likeCount"])

    def get_video_comments(self):
        url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_comments(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_comments(url_response)
        self.create_df()


    def create_df(self):
        if os.path.exists(SAVE_PATH+self.save_folder) == False:
            os.makedirs(SAVE_PATH+self.save_folder)

            df = pd.DataFrame().from_dict(self.comments)
            df["videoId"] = self.params['videoId']
            df.to_csv(SAVE_PATH+self.save_folder+"parent_video_comment.csv")

            df = pd.DataFrame().from_dict(self.replies)
            df["videoId"] = self.params['videoId']
            df.to_csv(SAVE_PATH+self.save_folder+"comment_reply.csv")

        else:
            df_orig = pd.read_csv(SAVE_PATH+self.save_folder+"parent_video_comment.csv")
            df_new = pd.DataFrame().from_dict(self.comments)
            df_new["videoId"] = self.params['videoId']
            df_orig = pd.concat((df_orig, df_new)).reset_index(drop=True)
            df_orig.to_csv(SAVE_PATH+self.save_folder+"parent_video_comment.csv")

            df_orig = pd.read_csv(SAVE_PATH+self.save_folder+"comment_reply.csv")
            df_new = pd.DataFrame().from_dict(self.replies)
            df_new["videoId"] = self.params['videoId']
            df_orig = pd.concat((df_orig, df_new)).reset_index(drop=True)
            df_orig.to_csv(SAVE_PATH+self.save_folder+"comment_reply.csv")