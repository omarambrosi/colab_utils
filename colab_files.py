'''To import into a Colab notebook:

!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
from colab_files import *
'''

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
