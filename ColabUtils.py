"""To import into a Colab project:

!git clone https://github.com/omarambrosi/colab_utils
%load colab_utils/ColabUtils.py
import sys
sys.path.append('colab_utils')
from ColabUtils import *
"""

from google.colab import files, auth
from google.cloud import bigquery
from datetime import date
import pandas as pd
import io
from oauth2client.client import GoogleCredentials
import gspread
import gspread_dataframe as gd
from apiclient.discovery import build

def csv_to_df():
  local_file = files.upload()
  return pd.read_csv(list(local_file.keys())[0])

def excel_to_df():
  local_file = files.upload()
  return pd.read_excel(list(local_file.keys())[0])

def df_to_bq(df, table_location, partitioned=False):
  project_id, dataset_id, table_id = table_location.split(".")
  
  auth.authenticate_user()
  client = bigquery.Client(project=project_id)
  dataset_ref = client.dataset(dataset_id)
  table_ref = dataset_ref.table(table_id)  
  
  job_config = bigquery.LoadJobConfig()
  job_config.autodetect=True
  if partitioned:
    job_config._properties['load']['timePartitioning'] = {'type': 'DAY'}

  client.load_table_from_dataframe(df, table_ref, job_config=job_config).result()
  
def csv_to_bq(table_location, partitioned=False):
  project_id, dataset_id, table_id = table_location.split(".")
  
  auth.authenticate_user()
  client = bigquery.Client(project=project_id)
  dataset_ref = client.dataset(dataset_id)
  table_ref = dataset_ref.table(table_id)  

  job_config = bigquery.LoadJobConfig()
  job_config.source_format = 'CSV'
  job_config.autodetect=True
  if partitioned:
    job_config._properties['load']['timePartitioning'] = {'type': 'DAY'}

  local_file = files.upload()
  with open(list(local_file.keys())[0], "rb") as source_file:
    client.load_table_from_file(source_file, table_ref, job_config=job_config).result()

""" drops the index (the original df.to_csv() method doesn't drop the index by default)
"""
def df_to_csv(df, file_name, index=False):
  full_file_name = file_name + " " + str(date.today()) + '.csv'
  df.to_csv(full_file_name, index=index)
  files.download(full_file_name)
  
def gspread_to_dfs(spreadsheet_id):
  import gspread
  from oauth2client.client import GoogleCredentials
  
  auth.authenticate_user()
  gc = gspread.authorize(GoogleCredentials.get_application_default())
  book = gc.open_by_key(spreadsheet_id)

  #Import the data from the spreadsheet into a dict of tables
  tables = {sheet.title : sheet.get_all_values() for sheet in book.worksheets()}

  #Convert the dict of tables into a dict of dataframes
  return {key : pd.DataFrame(tables[key][1:], columns=tables[key][0]) for key in tables}

def df_to_gspread(df, gspread_name):
  auth.authenticate_user()
  gc = gspread.authorize(GoogleCredentials.get_application_default())
  sh = gc.create(gspread_name)
  ws = sh.get_worksheet(0)
  gd.set_with_dataframe(ws, df)
  return "https://docs.google.com/spreadsheets/d/" + sh.id

def bq_to_df(project_id, query):
  auth.authenticate_user()
  job_config = bigquery.QueryJobConfig()
  return bigquery.Client(project_id).query(query, job_config=job_config).to_dataframe()

# pull an APPROX. number of random samples
def get_random_rows_from_bq_table(project_id, table_location, n_of_samples):
  query = f"""
      WITH a as (SELECT COUNT(*) FROM `{table_location}`)

      SELECT *
      FROM `{table_location}`
      WHERE RAND() < {n_of_samples}/(SELECT COUNT(*) FROM `{table_location}`)
  """
  return bq_to_df(project_id, query)

from google.cloud import bigquery

def list_datasets_from_bq_project(project_id):
  auth.authenticate_user()
  client = bigquery.Client(project=project_id)
  datasets = list(client.list_datasets()) 
  project = client.project

  return [dataset.dataset_id for dataset in datasets]

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
	result = pd.DataFrame()
	if type(id) is list:
		start = stop = 0
		c = 0
		if (len(l) % 50) == 0:
  			x = 0
		else:
 			x = 1
  
		rounds = (len(l) // 50) + x
		while rounds > 0: 
			results.append(_get_videos(youtube, l[c * 50: c * 50 + 50], rounds))
			rounds -=1
			c += 1
				
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
