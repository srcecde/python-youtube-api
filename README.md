<h2>Python YouTube API</h2>

A basic Python YouTube v3 API to fetch data from YouTube using public API-Key without OAuth.

It can fetch video comments for a given video URL, keyword based search (returns videos, playlist, channel) and return videos data for a given channelId. It store the data into output directory in CSV files.

You are required to get the API key from Google API console in order to use this script

<h2>How to use</h2>

<ul>
<li>Pass <b>--c</b> after file name for fetching comments from videos</li>
<li>Pass <b>--s</b> after file name for fetching results based on search keyword</li>
<li>Pass <b>--sc</b> after file name for fetching videos based on YouTube ChannelId</li>
</ul>
<br><b>It is mandatory to pass any of the above argument after file name</b>

<h2>Video Comments</h2>
<ul>
<li><b>--max</b> argument for defining the maximum result to return (default=10)</li>
<li><b>--videourl</b> argument for defining the youtube URL <i><b>Mandatory</b></i></li>
<li><b>--key</b> argument for defining API key <i><b>Mandatory</b></i></li>
</ul>
<b>Example: <i>python3 main.py --c --max 10 --videourl https://www.youtube.com/watch?v=y_j-r8x1FtI --key AAAAAAA</i></b>

<h2>Search by Keyword</h2>
<ul>
<li><b>--max</b> argument for defining the maximum result to return (default=10)</li>
<li><b>--search</b> argument for giving the keyword</li> 
<li><b>--r</b> argument for defining region (Country) For ex. --r=IN (Argument should be a country code)</li>
<li><b>--key</b> argument for defining your developer API key <i><b>Mandatory</b></i></li>
</ul>
<b>Example: <i>python3 main.py --s --search "srce cde" --max 10 --key AAAAAAA</i></b>

<h2>Search Videos by YouTube ChannelId</h2>
<ul>
<li><b>--max</b> argument for defining the maximum result to return (default=10)</li>
<li><b>--channelid</b> argument for defining channel id <i><b>Mandatory</b></i></li>
<li><b>--key</b> argument for defining your developer API key <i><b>Mandatory</b></i></li>
</ul>
<b>Example: <i>python3 main.py --sc --channelid UCwDlyuX3Fkg5WNBufLnH6dw --max 10 --key AAAAAAA</i></b>

<h4>Video example: https://youtu.be/ooZ98n-ZDUA</h4>

<h3>YouTube API v3</h3>
<ul>
<li><a href="https://developers.google.com/youtube/v3/">YouTube API v3 Docs</a></li>
<li><a href="http://code.google.com/apis/console">Obtain API Key</a></li>
</ul>
