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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channelid", help="channel id", required=True)
    parser.add_argument("--max", help="number of results to return", default=10)
    parser.add_argument("--key", help="Required API key", required=True)
    args = parser.parse_args()
    cv = channelVideo(args.channelid, args.max, args.key)
    cv.get_channel_videos()

if __name__ == '__main__':
    main()
