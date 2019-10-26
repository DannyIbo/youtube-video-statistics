#Explorer: https://developers.google.com/apis-explorer/#search/youtube/youtube/v3/youtube.search.list?part=snippet&channelId=UCSk9vb0Kc2WewD4IwvLJ9Iw&maxResults=50&_h=1&
#Documentation and source code: https://developers.google.com/youtube/v3/docs/search/list?apix=true

# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

#Imports for API Key:
import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import csv
import pandas as pd
import re
import datetime
import pytz

testtt = "test"

def videoCategories(youtube):
    '''Return a json file of categories and a dict, that is reduced to ids and titles'''
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="DE"
    )
    video_categories_response = request.execute()
    video_category_dict = {x['id']: x['snippet']['title'] for x in video_categories_response['items']}
    return video_category_dict

def youtubeAPIkey(DEVELOPER_KEY, OAUTHLIB_INSECURE_TRANSPORT = "1", api_service_name = "youtube", api_version = "v3"):
    '''Get YouTube Data API credentials via API Key\n
    Disable OAuthlib's HTTPS verification when running locally.\n
    *DO NOT* leave this option enabled in production.'''

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = OAUTHLIB_INSECURE_TRANSPORT #"1"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    return youtube

def youtubeSearchList(youtube, channelId=None, q=None, maxResults=50):
    '''
    Return a list of video snippets
    '''
    request = youtube.search().list(
        part="snippet"
        ,channelId=channelId
        #,channelType="any"
        #,eventType="completed"
        #,forContentOwner=True
        #,forDeveloper=True
        #,forMine=True
        #,location="string"
        #,locationRadius="string"
        ,maxResults=maxResults
        #,onBehalfOfContentOwner="string"
        #,order="date"
        #,pageToken=nextPageToken
        #,publishedAfter="string"
        #,publishedBefore="string"
        ,q=q
        #,regionCode="string"
        #,relatedToVideoId="string"
        #,relevanceLanguage="string"
        #,safeSearch="moderate"
        #,topicId="string"
        #,type="string"
        #,videoCaption="any"
        #,videoCategoryId="string"
        #,videoDefinition="any"
        #,videoDimension="any"
        #,videoDuration="any"
        #,videoEmbeddable="any"
        #,videoLicense="any"
        #,videoSyndicated="any"
        #,videoType="any"
        ,fields='items(id,snippet),nextPageToken'
        )
    responseSearchList = request.execute()
    return responseSearchList

def videoIdList(youtube, channelId):
    '''
    Return a list of all public video ids (in a specific channel)
    '''
    videoIdList = []
    
    requestChannelsList = youtube.channels().list(
        part="contentDetails"
        #,categoryId="string"
        #,forUsername="string"
        #,hl="string"
        ,id=channelId
        #,managedByMe=False
        #,maxResults=integer
        #,mine=False
        #,mySubscribers=False
        #,onBehalfOfContentOwner="string"
        #,pageToken="string"
        ,fields='items/contentDetails/relatedPlaylists/uploads'
    )
    responseChannelsList = requestChannelsList.execute()

    # Get upload playlist id from dictionary
    channelUploadPlaylistID = responseChannelsList.get('items')[0].get('contentDetails').get('relatedPlaylists').get('uploads')

    # Get items from upload playlist
    playlistNextPageToken = ''

    while playlistNextPageToken != None:

        requestPlaylistItems = youtube.playlistItems().list(
            part="snippet"
            #,id="string"
            ,maxResults=50
            #,onBehalfOfContentOwner="string"
            ,pageToken=playlistNextPageToken
            ,playlistId=channelUploadPlaylistID
            #,videoId="string"
            #,alt="json"
            #,fields="string"
            #,prettyPrint=True
            #,quotaUser="string"
            #,userIp="string"
            #,fields='items/snippet/resourceId/videoId,nextPageToken'
        )
        responsePlaylistItems = requestPlaylistItems.execute()

        # Append videos to Video List
        for video in responsePlaylistItems['items']:
            videoIdList.append(video['snippet']['resourceId']['videoId'])

        # Set nextPageToken
        playlistNextPageToken = responsePlaylistItems.get('nextPageToken')

    print('The channel', channelId, 'has', len(videoIdList), 'public videos')
    return videoIdList

def list_slice(input_list, n=50):
    '''Concatenate n list elements and return a new list of concatenations.\n
    Takes a list as input_list and an integer n for elements to concatenate.'''
    s = 0
    e = n
    list_slices = []
    while s < len(input_list):
        list_slices.append(','.join(input_list[s:e]))
        s = e
        e += n
    return list_slices

def videoSnippet(youtube, videoId, maxResults=50):
    '''
    Return a infos of a specific video\n
    Quota costs per video and info:\n
    snippet 2
    statistics 2
    contentDetails 2
    player 0
    recordingDetails ?
    status 2
    topicDetails 2
    '''
    requestSnippet = youtube.videos().list(
        part="snippet,statistics,contentDetails,player,status"
        #,chart="mostPopular"
        #,hl="string"
        ,id=videoId
        #,locale="string"
        #,maxHeight=integer
        #,maxResults=integer
        #,maxWidth=integer
        #,myRating="like"
        #,onBehalfOfContentOwner="string"
        #,pageToken="string"
        #,regionCode="string"
        #,videoCategoryId="string"
        #,alt="json"
        #,fields="nextPageToken,pageInfo,prevPageToken,tokenPagination,visitorId"
        #,prettyPrint=True
        #,quotaUser="string"
        #,userIp="string"
    )
    responseSnippet = requestSnippet.execute()
    return responseSnippet

def video_snippets(youtube, video_id_list, maxResults=50):
    '''
    Return a infos of a specific video\n
    Quota costs per video and info:\n
    snippet 2
    statistics 2
    contentDetails 2
    player 0
    recordingDetails ?
    status 2
    topicDetails 2
    '''
    
    video_id_chunks = list_slice(video_id_list, n=50)
    
    video_snippets =[]
    for chunk in video_id_chunks:
        responseSnippet = videoSnippet(youtube, chunk)
       # [i['date_data_created'] = datetime.datetime.now(tz=pytz.UTC) for i in responseSnippet['items']]
        [video_snippets.append(i) for i in responseSnippet['items']]
    
    return video_snippets
    

def youtubeOauth(scopes, api_service_name, api_version, client_secrets_file, OAUTHLIB_INSECURE_TRANSPORT):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = OAUTHLIB_INSECURE_TRANSPORT

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_analytics = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube_analytics

def csv_videolist(filename):    #open csv file and return content as object
    with open(filename, 'r') as wbs:
        content = csv.reader(wbs)
    return content

def to_int(string):
    '''Turn duration from text string such as 'PT1H23M09S' to an int'''
    return int(string[:-1]) if string else 0

def get_duration_sec(pt):
    '''Turn duration from text string such as 'PT1H23M09S' to an int'''
    pattern = 'PT(\d*H)?(\d*M)?(\d*S)?'
    timestamp = [to_int(x) for x in re.findall(pattern, pt)[0]]
    duration_sec = timestamp[0] * 3600 + timestamp[1] * 60 + timestamp[2]
    return duration_sec

def snippets_to_dict(video_snippet_list, yt_credentials=None):
    '''Return a dictionary from a given list of one or more video snippets.\
    The dictionary is optimized for creating a dataframe'''
    
    # Create an empty dictionary
    df_data = {'videoId': [], 
               'publishedAt': [],
               'channelId': [],
               'title': [],
               'description': [],
               'channelTitle': [],
               'tags': [],
               'categoryId': [],
               'category' : [],
               'liveBroadcastContent': [],
               'duration': [],
               'duration_sec': [],
               'dimension': [],
               'definition': [],
               'caption': [],
               'licensedContent': [],
               'projection': [],
               'privacyStatus': [],
               'license': [],
               'embeddable': [],
               'publicStatsViewable': [],
               'viewCount': [],
               'likeCount': [],
               'dislikeCount': [],
               'favoriteCount': [],
               'commentCount': [],
               'thumbnails_default': [],
               'date_data_created': []
              }
    
    if yt_credentials:
        video_category_dict = videoCategories(yt_credentials)    
    else:
        del df_data['category']
        
    for i in video_snippet_list:

        df_data['videoId'].append(i.get('id'))
        df_data['publishedAt'].append(i.get('snippet').get('publishedAt'))
        df_data['channelId'].append(i.get('snippet').get('channelId'))
        df_data['title'].append(i.get('snippet').get('title'))
        df_data['description'].append(i.get('snippet').get('description'))
        df_data['channelTitle'].append(i.get('snippet').get('channelTitle'))
        df_data['tags'].append(i.get('snippet').get('tags'))
        df_data['categoryId'].append(i['snippet'].get('categoryId'))
        
        if yt_credentials:
            df_data['category'] = video_category_dict[i['snippet'].get('categoryId')]
        
        df_data['liveBroadcastContent'].append(i['snippet'].get('liveBroadcastContent'))
        df_data['duration'].append(i['contentDetails'].get('duration'))

        duration_text = i['contentDetails'].get('duration')
        df_data['duration_sec'].append(get_duration_sec(duration_text))

        df_data['dimension'].append(i['contentDetails'].get('dimension'))
        df_data['definition'].append(i['contentDetails'].get('definition'))
        df_data['caption'].append(i['contentDetails'].get('caption'))
        df_data['licensedContent'].append(i['contentDetails'].get('licensedContent'))
        df_data['projection'].append(i['contentDetails'].get('projection'))
        df_data['privacyStatus'].append(i['status'].get('privacyStatus'))
        df_data['license'].append(i['status'].get('license'))
        df_data['embeddable'].append(i['status'].get('embeddable'))
        df_data['publicStatsViewable'].append(i['status'].get('publicStatsViewable'))

        df_data['viewCount'].append(int(i['statistics'].get('viewCount')))
        df_data['likeCount'].append(i['statistics'].get('likeCount'))
        df_data['dislikeCount'].append(i['statistics'].get('dislikeCount'))
        df_data['favoriteCount'].append(int(i['statistics']['favoriteCount']))
        df_data['commentCount'].append(i['statistics'].get('commentCount'))
        df_data['thumbnails_default'].append(i.get('snippet').get('thumbnails').get('default').get('url'))
        df_data['date_data_created'].append(datetime.datetime.now(tz=pytz.UTC))
        
    return df_data

def get_comments(youtube, videoId):
    '''Return a .json wit comments and meta data. Tae as input the youtube credential object and the videoId.'''
    request = youtube.commentThreads().list(
        part="id,replies,snippet",
        maxResults=100,
        videoId=videoId
    )
    response = request.execute()
    return response

def comments_to_dict(comments):
    '''Return a dictionary. Take as input a .json file'''
    df_data = {
    'authorDisplayName':[],
    'authorProfileImageUrl':[],
    'authorChannelUrl':[],
    'authorChannelId':[],
    'textDisplay':[],
    'textOriginal':[],
    'parentId':[],
    'canRate':[],
    'viewerRating':[],
    'likeCount':[],
    'publishedAt':[],
    'updatedAt':[],
    'canReply':[],
    'totalReplyCount':[],
    'isPublic':[]}

    for i in comments['items']:
        df_data['authorDisplayName'].append(i['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        df_data['authorProfileImageUrl'].append(i['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
        df_data['authorChannelUrl'].append(i['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
        df_data['authorChannelId'].append(i['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
        df_data['textDisplay'].append(i['snippet']['topLevelComment']['snippet']['textDisplay'])
        df_data['textOriginal'].append(i['snippet']['topLevelComment']['snippet']['textOriginal'])
        df_data['parentId'].append(i['snippet']['topLevelComment']['snippet'].get('parentId'))
        df_data['canRate'].append(i['snippet']['topLevelComment']['snippet']['canRate'])
        df_data['viewerRating'].append(i['snippet']['topLevelComment']['snippet']['viewerRating'])
        df_data['likeCount'].append(i['snippet']['topLevelComment']['snippet']['likeCount'])
        df_data['publishedAt'].append(i['snippet']['topLevelComment']['snippet']['publishedAt'])
        df_data['updatedAt'].append(i['snippet']['topLevelComment']['snippet']['updatedAt'])
        df_data['canReply'].append(i['snippet']['canReply'])
        df_data['totalReplyCount'].append(i['snippet']['totalReplyCount'])
        df_data['isPublic'].append(i['snippet']['isPublic'])

        if i.get('replies'):
            for c in i['replies']['comments']:

                df_data['authorDisplayName'].append(c['snippet']['authorDisplayName'])
                df_data['authorProfileImageUrl'].append(c['snippet']['authorProfileImageUrl'])
                df_data['authorChannelUrl'].append(c['snippet']['authorChannelUrl'])
                df_data['authorChannelId'].append(c['snippet']['authorChannelId']['value'])
                df_data['textDisplay'].append(c['snippet']['textDisplay'])
                df_data['textOriginal'].append(c['snippet']['textOriginal'])
                df_data['parentId'].append(c['snippet'].get('parentId'))
                df_data['canRate'].append(c['snippet']['canRate'])
                df_data['viewerRating'].append(c['snippet']['viewerRating'])
                df_data['likeCount'].append(c['snippet']['likeCount'])
                df_data['publishedAt'].append(c['snippet']['publishedAt'])
                df_data['updatedAt'].append(c['snippet']['updatedAt'])
                df_data['canReply'].append(c['snippet'].get('canReply'))
                df_data['totalReplyCount'].append(c['snippet'].get('totalReplyCount'))
                df_data['isPublic'].append(c['snippet'].get('isPublic'))
                
    return df_data