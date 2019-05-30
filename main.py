"""
-*- coding: utf-8 -*-
========================
Python YouTube v3 API
========================

Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com

========================
"""

import sys
import argparse
from youtube.videos_channelid import channelVideo
from youtube.search_keyword import searchVideo

def main():
    parser = argparse.ArgumentParser()

    if str(sys.argv[1]) == "--s":
        
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
        parser.add_argument("--search", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return", default=10)
        parser.add_argument("--key", help="Required API key")
        args = parser.parse_args()

        sv = searchVideo(args.search, args.max, args.r, args.key)
        sv.get_channel_videos()

    elif str(sys.argv[1]) == "--sc":
        parser.add_argument("--channelid", help="channel id", required=True)
        parser.add_argument("--max", help="number of results to return", default=10)
        parser.add_argument("--key", help="Required API key", required=True)
        args = parser.parse_args()

        cv = channelVideo(args.channelid, args.max, args.key)
        cv.get_channel_videos()
    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --sc to list vidoes based on channel id")

if __name__ == '__main__':
    main()
