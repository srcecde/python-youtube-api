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
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen


YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


class YouTubeApi():

    def get_video_comment(self):

        parser = argparse.ArgumentParser()
        mxRes = 20
        vid = str()
        parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return")
        parser.add_argument("--videourl", help="Required URL for which comments to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.videourl:
            exit("Please specify video URL using the --videourl=parameter.")

        if not args.key:
            exit("Please specify API key using the --key=parameter.")

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

    def search_keyword(self):

        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--search", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                    'q': args.search,
                    'part': 'id,snippet',
                    'maxResults': args.max,
                    'key': args.key
                }
        try:
            f = urlopen(YOUTUBE_SEARCH_URL + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")

            search_response = json.loads(matches)

            videos = []
            channels = []
            playlists = []

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                  videos.append("{} ({})".format(search_result["snippet"]["title"],
                                             search_result["id"]["videoId"]))
                elif search_result["id"]["kind"] == "youtube#channel":
                  channels.append("{} ({})".format(search_result["snippet"]["title"],
                                               search_result["id"]["channelId"]))
                elif search_result["id"]["kind"] == "youtube#playlist":
                  playlists.append("{} ({})".format(search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

            print("Videos:\n", "\n".join(videos), "\n")
            print("Channels:\n", "\n".join(channels), "\n")
            print("Playlists:\n", "\n".join(playlists), "\n")

        except:
            print("Cannot Open URL or Fetch comments at a moment")


def main():
    y = YouTubeApi()

    if str(sys.argv[1]) == "--s":
        y.search_keyword()
    elif str(sys.argv[1]) == "--c":
        y.get_video_comment()
    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --c to list comments after the filename")

if __name__ == '__main__':
    main()
