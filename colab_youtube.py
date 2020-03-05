''' to use this module in colab:
!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
from colab_youtube import *
'''

import pandas as pd
from apiclient.discovery import build

def _yt_auth(developerKey):
	''' To create a project: https://cloud.google.com/console
	'''
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	DEVELOPER_KEY = developerKey
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
	return youtube
	
def _generate_df():
	return pd.DataFrame(columns=['video_id', 'publishedAt', 'video_title', 'description', 'duration', 'privacyStatus',
	                          'channelTitle', 'tags', 'madeForKids', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount'])

def yt_to_df(developerKey, id):
	youtube = _yt_auth(developerKey)
	results = pd.DataFrame()
	if type(id) is list:
		start = stop = 0
		c = 0
		x = 0 if (len(id) % 50) == 0 else 1
		rounds = (len(id) // 50) + x
		while rounds > 0: 
			try:
				results = results.append(_get_videos(youtube, id[c * 50: c * 50 + 50]))
				rounds -=1
				c += 1
			except:
				print('API quota error. The results are partial')
				return results
				
		for i in id:
			if len(i) != 11:
				raise ValueError(f'{i} is not a valid video id')
		return results
	
	elif type(id) is str:
		resource = {24:"channel", 34:"playlist"}
		try:
			resource_type = resource[len(id)]
		except:
			raise ValueError(f'{id} is not a valid channel or playlist id')

		if resource_type == 'channel':
			return _get_videos_from_channel(youtube, id)
		elif resource_type == 'playlist':
			return _get_videos_from_playlist(youtube, id)

def _get_videos_from_channel(youtube, channel_id):
	channel_response = youtube.channels().list(
		id=channel_id,
		part='contentDetails',
		fields='items/contentDetails/relatedPlaylists/uploads',
  ).execute()

  # Get the id of the uploads playlist
	playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
	return _get_videos_from_playlist(youtube, playlist_id)

def _get_videos(youtube, video_ids):
	df = _generate_df()
	video_response = youtube.videos().list(
		id=",".join(video_ids),
		part='snippet,status,statistics,contentDetails'
	).execute()
	videos = video_response['items']

	for video in videos:
		df = df.append({'video_id': video['id'],
				'publishedAt' : video['snippet'].get('publishedAt'),
				'video_title' : video['snippet'].get('title'),
				'description' : video['snippet'].get('description'),
				'channelTitle' : video['snippet'].get('channelTitle'),
				'tags' : video['snippet'].get('tags'),
				'duration' : video['contentDetails'].get('duration'),
				'privacyStatus' : video['status'].get('privacyStatus'),
				'madeForKids' : video['status'].get('madeForKids'),
				'viewCount' : video['statistics'].get('viewCount'),
				'likeCount' : video['statistics'].get('likeCount'),
				'dislikeCount' : video['statistics'].get('dislikeCount'),
				'commentCount' : video['statistics'].get('commentCount')
				}, ignore_index=True)
	 	
	df.set_index('video_id', inplace=True)
	df.sort_values(by='publishedAt', ascending=False, inplace=True)
	return df

def _get_videos_from_playlist(youtube, playlist_id):
	df = _generate_df()
	df.set_index('video_id', inplace=True)
	playlistitems_list_request = youtube.playlistItems().list(
		playlistId=playlist_id,
		part='snippet',
	fields='items/snippet/resourceId/videoId,nextPageToken,pageInfo,prevPageToken',
		maxResults=50
	)
	while playlistitems_list_request:
		try:
			playlistitems_list_response = playlistitems_list_request.execute()
		except:
			print('Quota error. The dataframe has incomplete results')
			return df

		v_ids = [i['snippet']['resourceId']['videoId'] for i in playlistitems_list_response['items']]
		df = pd.concat([df, _get_videos(youtube, v_ids)])
		playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
	
	df.sort_values(by='publishedAt', ascending=False, inplace=True)
	return df
