'''To import into a Colab notebook:

!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
from colab_files import *
'''

from google.colab import files, auth
from datetime import date
import pandas as pd
import io
from oauth2client.client import GoogleCredentials
import gspread
import gspread_dataframe as gd

def csv_to_df(path=None):
  if path == None:
    local_file = files.upload()
    return pd.read_csv(list(local_file.keys())[0], encoding="latin-1")
  else:
    return pd.read_csv(path, encoding="latin-1")

def excel_to_df():
  local_file = files.upload()
  return pd.read_excel(list(local_file.keys())[0])

""" drops the index (the original df.to_csv() method doesn't drop the index by default)
"""
def df_to_csv(df, file_name="Untitled", index=False):
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

def df_to_gspread(df, gspread_name="Untitled"):
  auth.authenticate_user()
  gc = gspread.authorize(GoogleCredentials.get_application_default())
  sh = gc.create(gspread_name)
  ws = sh.get_worksheet(0)
  gd.set_with_dataframe(ws, df)
  return "https://docs.google.com/spreadsheets/d/" + sh.id

def dfs_columns_diff(dfs, highlight_value=False):
  """ Get the differences in the schema of a list of dfs
  Args:
    dfs: a dict or list of dataframe
  
  Returns:
    a dataframe where each cell is a list with the differenes in columns between a couple of dataframes 
    it's case sensitive. Doesn't get back the resulsts in orders 
  """
  
  if type(dfs) is dict:
    df = pd.DataFrame(index=[y for i,y in enumerate(dfs)], columns = [y for i,y in enumerate(dfs)])
  else:
    df = pd.DataFrame(index=[i for i,y in enumerate(dfs)], columns = [i for i,y in enumerate(dfs)])

  # give back a df with differences as intersection between all dfs.


  #df = df.apply(lambda row : list(set(dfs[row.name].values.tolist()).difference(set(dfs[row.name].values.tolist()))))
  for i in df.columns.values:
    for y in df.index.values:
      df.loc[i,y] = list(set(dfs[y].columns.values.tolist()).difference(set(dfs[i].columns.values.tolist())))
  
  if highlight_value:
    # convert the empty lists into empty strings
    df = df.applymap(lambda y : '' if len(y)==0 else y)
  else:
    df = df.applymap(lambda y : None if len(y)==0 else y)
  return df

def dfs_any_columns_diff(dfs):
  """
  Check if there is any difference in the columns names between the dataframes
  Args:
    dfs: a list of dataframes
  
  Returns:
    a boolean to display if there is any difference amongst any couple of dataframes
  """

  return dfs_columns_diff(dfs, False).any().any()
