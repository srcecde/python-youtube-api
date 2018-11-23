"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================
Forked from: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com
========================
Updated by: Fergus Boyd
Email: fergus.p.boyd@gmail.com

Returns a pandas DataFrame of youtube comments and replies, used for my data science pipelines.
"""

import json
import pandas as pd
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import urlopen

YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'

class YouTubeApi():

    def load_comments(self, mat):
        colNames = ['commentID', 'parentID', 'author', 'time', 'comment', 'likes']
        df = pd.DataFrame(columns=colNames)
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            cmID = comment['id']
            paID = None
            autr = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            time = comment["snippet"]["publishedAt"]
            like = comment["snippet"]["likeCount"]

            comment_df = pd.DataFrame([[cmID, paID, autr, time, text, like], ], columns=colNames)
            df = df.append(comment_df, ignore_index=True)

            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    rcmID = reply['id']
                    rpaID = reply["snippet"]["parentId"]
                    rautr = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]
                    rtime = reply["snippet"]["publishedAt"]
                    rlike = reply["snippet"]["likeCount"]

                    reply_df = pd.DataFrame([[rcmID, rpaID, rautr, rtime, rtext, rlike], ], columns=colNames)
                    df = df.append(reply_df, ignore_index=True)
        return df

    def get_video_comment(self, vid, key, max_return=20):
        parms = {
                    'part': 'snippet,replies',
                    'maxResults': max_return,
                    'videoId': vid,
                    'textFormat': 'plainText',
                    'key': key
                }

        try:
            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            all_comments = self.load_comments(mat)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")

                new_comments = self.load_comments(mat)
                all_comments = all_comments.append(new_comments, ignore_index=True)

            return all_comments
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches
