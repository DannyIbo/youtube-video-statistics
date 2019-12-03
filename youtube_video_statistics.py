#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from docs import youtube_data_module as ytd
import os

# Get your YouTube API.
YOUTUBE_API = os.getenv('YOUTUBE_API_KEY')

# Create credential object to use the YouTube API
youtube = ytd.youtubeAPIkey(YOUTUBE_API)

# Set the channel you want to get the video statistics for
# channelId = 'UCV9pZxcKWF6fZ1ZQzDWofgw'
# Set the channel Id hard coded...
channelId = ''
# ... or get the channel Id by user input
if not channelId:
    channelId = input('Please enter the channel Id you like to get video statistics for:')

# Get a list of video Ids that are publicly available on the given channel
try:
    video_id_list = ytd.videoIdList(youtube, channelId)
except:
    print('Error: This may not be a valid YouTube channel Id or there are no videos publicly available. \nPlease find a valid channel Id in the URL. For example: "UCV9pZxcKWF6fZ1ZQzDWofgw" is the channel Id in the URL "https://www.youtube.com/channel/UCV9pZxcKWF6fZ1ZQzDWofgw"')

# Get video statisics and several other figures and return a .json-file
video_snippets = ytd.video_snippets(youtube, video_id_list)

# Restructure the .json-file and extract only the needed data
video_snippet_dict = ytd.snippets_to_dict(video_snippets, yt_credentials=youtube)

# Create a pandas Data Frame
df = pd.DataFrame(video_snippet_dict).set_index('videoId')

# Write data frame to excel
df_excel = df.drop(columns=['date_data_created'])
df_excel.to_excel(f'output/youtube-video-statistics_channel_Id_{channelId}.xlsx')

print(f'Successfully downloaded YouTube video statistics for channel Id "{channelId}". \nPlease check the output folder for the final .xlsx-file.')
