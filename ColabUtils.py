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

def df_to_csv(df, file_name):
  full_file_name = file_name + " " + str(date.today()) + '.csv'
  df.to_csv(full_file_name, index=False)
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
