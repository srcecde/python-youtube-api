<h3>Python YouTube API</h3>

A basic Python YouTube v3 API to fetch data from YouTube using public API-Key without OAuth

It fetches comments and some other information in a pandas DataFrame. Forked from srcecde and altered to fit my own data science pipelines.

You are required to get the API key from Google API console in order to use this script

<h3>How to use</h3>
<ul>
<li>y = YouTubeAPI()
  
  data = y.get_video_comment(vid='dQw4w9WgXcQ', key='*YOUTUBE API KEY*'
  
<li> max_return parameter for defining the maximum result you want (maxlimit = 100, default=20)</li>
<li> vid parameter for defining the youtube ID</li>
<li> key parameter for defining your developer API key</li>
<li> videourl and --key parameter is mandatory. --max parameter is optional</li>
</ul>


<h3>YouTube API v3</h3>
<ul>
<li><a href="https://developers.google.com/youtube/v3/">YouTube API v3 Docs</a></li>
<li><a href="http://code.google.com/apis/console">Obtain API Key</a></li>
</ul>
