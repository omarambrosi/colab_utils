'''To import into a Colab notebook:

!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
from colab_bigquery import *
'''

from google.colab import files, auth
from google.cloud import bigquery
from datetime import date
import pandas as pd
import io
from oauth2client.client import GoogleCredentials
import gspread
import gspread_dataframe as gd

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
  job_config.maxBadRecords = 1000
  job_config.ignoreUnknownValues=True
  job_config.autodetect=True
  if partitioned:
    job_config._properties['load']['timePartitioning'] = {'type': 'DAY'}

  local_file = files.upload()
  with open(list(local_file.keys())[0], "rb") as source_file:
    client.load_table_from_file(source_file, table_ref, job_config=job_config).result()
    
def bq_to_df(project_id, query):
  auth.authenticate_user()
  job_config = bigquery.QueryJobConfig()
  return bigquery.Client(project_id).query(query, job_config=job_config).to_dataframe()

def get_random_rows_from_bq_table(project_id, table_location, n_of_rows):
  query = f"""
      WITH a as (SELECT COUNT(*) FROM `{table_location}`)

      SELECT *
      FROM `{table_location}`
      WHERE RAND() < {n_of_rows}/(SELECT COUNT(*) FROM `{table_location}`)
  """
  return bq_to_df(project_id, query)

from google.cloud import bigquery

def list_datasets_from_bq_project(project_id):
  auth.authenticate_user()
  client = bigquery.Client(project=project_id)
  datasets = list(client.list_datasets()) 
  project = client.project

  return [dataset.dataset_id for dataset in datasets]
