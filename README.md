<h3>Python YouTube API</h3>

A basic Python YouTube v3 API to fetch data from YouTube using public API-Key without OAuth

It fetch comments, perform search and return videos, channels and playlist in categorized form.

You are required to get the API key from Google API console in order to use this script

<h3>How to use</h3>

<i>Pass --c after file name for calling Video Comment function</i>
<i>Pass --s after file name for calling Search by Keyword</i>
<i>Pass --sc after file name for calling Search videos by YouTube ChannelId</i>
<br><b>It is mandatory to pass any of the above argument after file name</b>

<h2>Video Comments</h2>
<ul>
<li>python youtube_api_cmd.py --max --videourl --key </li>
<li>--max parameter for defining the maximum result you want (maxlimit = 100, default=20)</li>
<li>--videourl parameter for defining the youtube URL</li>
<li>--key parameter for defining your developer API key</li>
<li>--videourl and --key parameter is mandatory. --max parameter is optional</li>
</ul>

<h2>Search by Keyword</h2>
<ul>
<li>python youtube_api_cmd.py --search --max --key</li>
<li>--max parameter for defining the maximum result you want (maxlimit = 100, default=20)</li>
<li>--search parameter for giving the keyword</li>
<li>--r parameter for defining region (Country) For ex. --r=IN (Parameter should be a country code)</li>
<li>--key parameter for defining your developer API key <i><b>Mandatory</b></i></li>
<li>It will return Videos, Channel and Playlist in the respective category</li>
</ul>

<h2>Search Videos by YouTube ChannelId</h2>
<ul>
<li>python youtube_api_cmd.py --channelid --max --key</li>
<li>--max parameter for defining the maximum result you want (maxlimit = 100, default=20)</li>
<li>--channelid parameter for defining channel id <i><b>Mandatory</b></i></li>
<li>--key parameter for defining your developer API key <i><b>Mandatory</b></i></li>
<li>It will list of Videos from the defined YouTube ChannelId</li>
</ul>

<h3>YouTube API v3</h3>
<ul>
<li><a href="https://developers.google.com/youtube/v3/">YouTube API v3 Docs</a></li>
<li><a href="http://code.google.com/apis/console">Obtain API Key</a></li>
</ul>
