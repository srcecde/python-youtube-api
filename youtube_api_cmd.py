"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================

Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com

========================
"""

import json
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen



YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'


class YouTubeApi():

    def get_video_comment(self):

        parser = argparse.ArgumentParser()
        mxRes = 20
        vid = str()
        parser.add_argument("--max", help="number of comments to return")
        parser.add_argument("--videourl", help="Required URL for which comments to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.videourl:
            exit("Please specify video URL using the --videourl= parameter.")

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        try:
            video_id = urlparse(str(args.videourl))
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet',
                    'maxResults': args.max,
                    'videoId': vid,
                    'key': args.key
                }

        try:
            f = urlopen(YOUTUBE_COMMENT_URL + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")

            mat = json.loads(matches)

            for item in mat["items"]:
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                print("Comment by {}: {}".format(author, text))

        except:
            print("Cannot Open URL or Fetch comments at a moment")


def main():
    y = YouTubeApi()
    y.get_video_comment()


if __name__ == '__main__':
    main()
