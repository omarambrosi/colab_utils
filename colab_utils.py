"""To import into a Colab project:

!git clone https://github.com/omarambrosi/colab_utils
%load colab_utils/colab_utils.py
import sys
sys.path.append('colab_utils')
from colab_utils import *
"""

from google.colab import files, auth
from google.cloud import bigquery
from datetime import date
import pandas as pd
import io

def csv_to_df():
  local_file = files.upload()
  return pd.read_csv(list(local_file.keys())[0])

def excel_to_df():
  local_file = files.upload()
  return pd.read_excel(list(local_file.keys())[0])

def csv_to_bq(project_id, dataset, table):
  df_to_bq(csv_to_df(), project_id, dataset, table)

def df_to_bq(df, project_id, dataset, table):
  auth.authenticate_user()
  client = bigquery.Client(project=project_id)
  dataset_ref = client.dataset(dataset)
  table_ref = dataset_ref.table(table)
  client.load_table_from_dataframe(df, table_ref).result()

def df_to_csv(df, file_name):
  full_file_name = file_name + " " + str(date.today()) + '.csv'
  df.to_csv(full_file_name)
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
