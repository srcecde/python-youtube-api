
#!/usr/bin/env python3

"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================
Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com
"""
import json
import jsonlines
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen
import jsonlines

saved_ids = []
with jsonlines.open('../filtered_domains.jsonl', 'r') as reader:
  for video in reader:
    saved_ids.append(video["vid"])


YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

class YouTubeApi():

    def get_video_comment(self, vid):
        print(vid)
        def load_comments(self, vid):
          
          for item in mat["items"]:              
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]                
                with jsonlines.open('comments.jsonl', 'a') as writer:                  
                    writer.write(
                      {
                        "vID": vid,
                        "cID": str(comment["id"]),
                        "author": str(author),
                        "comment": str(text)
                        
                      }      
                    )                
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        

                        rauthor = reply['snippet']['authorDisplayName']
                        rtext = reply["snippet"]["textDisplay"]                        
                                                            
                    with jsonlines.open('comments.jsonl', 'a') as writer:
                        writer.write(
                          {
                            "vid": vid,
                            "cid": str(reply["id"]),
                            "author": str(rauthor),
                            "comment": str(rtext)

                          }      
                        )
                    

        parser = argparse.ArgumentParser()
        mxRes = 20
        
        parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return")
        parser.add_argument("--videourl", help="Required URL for which comments to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes


        if not args.key:
            exit("Please specify API key using the --key=parameter.")


        parms = {
                    'part': 'snippet,replies',
                    'maxResults': args.max,
                    'videoId': vid,
                    'textFormat': 'plainText',
                    'key': args.key
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")
            load_comments(self, vid)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                if i > 10:
                  sys.exit()
                print("\nPage : ", i)
                print("------------------------------------------------------------------")

                load_comments(self, vid)

                i += 1
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def search_keyword(self):

        def load_search_res(self):
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

        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
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
                    'regionCode': args.r,
                    'key': args.key
                }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)
            i = 2

            nextPageToken = search_response.get("nextPageToken")

            videos = []
            channels = []
            playlists = []
            print("\nPage : 1 --- Region : {}".format(args.r))
            print("------------------------------------------------------------------")
            load_search_res(self)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                search_response = json.loads(matches)
                nextPageToken = search_response.get("nextPageToken")
                print("Page : {} --- Region : {}".format(i, args.r))
                print("------------------------------------------------------------------")

                load_search_res(self)

                i += 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def channel_videos(self):

        def load_channel_vid(self):

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    videos.append("{} ({})".format(search_result["snippet"]["title"],
                                             search_result["id"]["videoId"]))

            print("###Videos:###\n", "\n".join(videos), "\n")

        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--sc", help="calls the search by channel by keyword function", action='store_true')
        parser.add_argument("--channelid", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.channelid:
            exit("Please specify channelid using the --channelid= parameter.")

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                   'part': 'id,snippet',
                   'channelId': args.channelid,
                   'maxResults': args.max,
                   'key': args.key
               }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)

            videos = []
            i = 2

            nextPageToken = search_response.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")

            load_channel_vid(self)

            while nextPageToken:
                      
                    parms.update({'pageToken': nextPageToken})
                    matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                    search_response = json.loads(matches)
                    nextPageToken = search_response.get("nextPageToken")
                    if i > 10:                      
                      sys.exit()
                    print("Page : ", i)
                    print("------------------------------------------------------------------")

                    load_channel_vid(self)

                    i += 1

        except KeyboardI3nterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches


def main():
    y = YouTubeApi()

    if str(sys.argv[1]) == "--s":
        y.search_keyword()
    elif str(sys.argv[1]) == "--c":
      for vid in saved_ids:
        y.get_video_comment(vid)
    elif str(sys.argv[1]) == "--sc":
        y.channel_videos()
    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --c to list comments after the filename\nAdd --sc to list vidoes based on channel id")


if __name__ == '__main__':
    main()
