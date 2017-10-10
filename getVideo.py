import argparse
import csv
from unidecode import unidecode
from urllib2 import urlopen
from urllib import urlencode
import json

DEVELOPER_KEY = "AIzaSyCfkJCXWirc5Wk8dV1sb3Rjv7eoZKdDNnU"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


def openURL(url, parms):
    """
    This function returns a dataset that matches values in parms.
    """
    f = urlopen(url+"?"+urlencode(parms))
    data = f.read()
    f.close()
    matched_data = data.decode("utf-8")
    return matched_data

def youtube_search(options):
    
    parms = {
        "q": options.q, # Specify the query.
        "part": "id, snippet", 
        "maxResults": options.max_results, 
        "key": DEVELOPER_KEY,
        "type": "video"
        }

    match_result = openURL(YOUTUBE_SEARCH_URL, parms)
    search_response = json.loads(match_result)
    
    # Get next page's token.
    nextPageToken = search_response.get("nextPageToken")

    # Begin to write the data to a csv file.
    csvFile = open("video_result.csv", "w")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["title","videoId","viewCount","likeCount","dislikeCount","commentCount","favoriteCount"])

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode(title)
            videoId = search_result["id"]["videoId"]

            video_parms = {"id": videoId, "part": "statistics", "key": DEVELOPER_KEY}
            video_match_result = openURL(YOUTUBE_VIDEO_URL, video_parms)
            video_response = json.loads(video_match_result)

            for video_result in video_response.get("items",[]):
                viewCount = video_result["statistics"]["viewCount"]
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                if 'favoriteCount' not in video_result["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_result["statistics"]["favoriteCount"]
                   
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount])

    page_count = 0
    
    # Begin to parse next page's content.
    while page_count <= options.page_num:
        parms.update({"PageToken": nextPageToken})
        match_result = openURL(YOUTUBE_SEARCH_URL, parms)
        search_response = json.loads(match_result)
        nextPageToken = search_response.get("nextPageToken")
        
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                title = search_result["snippet"]["title"]
                title = unidecode(title)
                videoId = search_result["id"]["videoId"]

                video_parms = {"id": videoId, "part": "statistics", "key": DEVELOPER_KEY}
                video_match_result = openURL(YOUTUBE_VIDEO_URL, video_parms)
                video_response = json.loads(video_match_result)

                for video_result in video_response.get("items",[]):
                    viewCount = video_result["statistics"]["viewCount"]
                    if 'likeCount' not in video_result["statistics"]:
                        likeCount = 0
                    else:
                        likeCount = video_result["statistics"]["likeCount"]
                    if 'dislikeCount' not in video_result["statistics"]:
                        dislikeCount = 0
                    else:
                        dislikeCount = video_result["statistics"]["dislikeCount"]
                    if 'commentCount' not in video_result["statistics"]:
                        commentCount = 0
                    else:
                        commentCount = video_result["statistics"]["commentCount"]
                    if 'favoriteCount' not in video_result["statistics"]:
                        favoriteCount = 0
                    else:
                        favoriteCount = video_result["statistics"]["favoriteCount"]
                       
                csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount])

        page_count+=1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Search on YouTube")

    # Parse the search term.
    parser.add_argument("--q", help = "Search term", default = "Google")

    # Parse maximum results.
    parser.add_argument("--max-results", help = "Max results", default = 50)

    # Parse number of pages to be crawled.
    parser.add_argument("--page-num", help = "Number of pages to be pulled", default = 20)
    
    args = parser.parse_args()
    youtube_search(args)

