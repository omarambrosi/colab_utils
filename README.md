# colab_utils
This package contains modules that extend and simplify the interaction with files, BigQuery and YouTube.
## Installing
To import all the functions from one module into a Colab notebook:
```ipython
!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
from colab_youtube import *
```
## Author
* [Omar Ambrosi](https://www.linkedin.com/in/omarambrosi)

## Functions

### Files 
* csv_to_df
* excel_to_df
* gspread_to_dfs
* [df_to_csv](#df_to_csvdf-file_name="untitled"-index=false)
* df_to_gspread

### BigQuery
* [df_to_bq](#df_to_bqdf-table_location-partitionedfalse)
* [csv_to_bq](#csv_to_bqtable_location-partitionedfalse)
* gspread_to_bq
* [bq_to_df](#bq_to_dfproject_id-query)
* [get_random_rows_from_bq_table](#get_random_rows_from_bq_tableproject_id-table_location-n_of_rows)
* [list_datasets_from_bq_project](#list_datasets_from_bq_projectproject_id)

### YouTube
* [yt_to_df](#yt_to_dfdeveloperKey-id)
* cid_to_df

## Documentation
### Files
from colab_files import *
#### [df_to_csv(df, file_name="Untitled", index=False)](colab_files.py)
Export a Pandas DataFrame as a local csv. It doesn't include the index by default and appends the current date to the file name.
```python
df_to_csv(df)
```

### BigQuery
from colab_bigquery import *
#### [df_to_bq(df, table_location, partitioned=False)](colab_bigquery.py)
#### [csv_to_bq(table_location, partitioned=False)](colab_bigquery.py)
#### [bq_to_df(project_id, query)](colab_bigquery.py)
#### [get_random_rows_from_bq_table(project_id, table_location, n_of_rows)](colab_bigquery.py)
Get an APPROXIMATED number of random rows from a BigQuery table
```python
df = get_random_rows_from_bq_table(YOUR_BQ_PROJECT_ID, 'bigquery-public-data.wikipedia.wikidata', 3)
df.iloc[:,0:6]
```
results:
| id	      | numeric_id | en_label                      | en_wiki	| en_description	| ja_label |
|-----------|------------|-------------------------------|----------|-----------------|----------|
|	Q38962972	| 38962972	 | Veterans Living with HIV: ... | None	    | scientific a... | None     |
|	Q51195092	| 51195092	 | Template:Taxonomy/Bythaelurus | Templa...|	None	          | None     |
|	Q75088335	| 75088335	 | CTLGD 8239	                   | None	    | None	          | None     |
|	Q56129812	| 56129812	 | transcriptional regulator...  | None	    | microbial ge... | None     |

#### [list_datasets_from_bq_project(project_id)](colab_bigquery.py)
```python
list_datasets_from_bq_project('bigquery-public-data')[:3]
```
results:
```python
['austin_311', 'austin_bikeshare', 'austin_crime']
```
### YouTube
from colab_youtube import *
#### [yt_to_df(developerKey, id)](colab_youtube.py)
Import data from a list of videos, a channel or a playlist.
```python
yt_to_df(YOUR_DEVELOPER_KEY, "UC-lHJZR3Gqxm24_Vd_AJ5Yw").head(2)
```
results:
|  video_id   |       publishedAt        |       video_title        |            description              | duration | privacyStatus  | channelTitle |           tags           | madeForKids | viewCount | likeCount | dislikeCount | commentCount |
|-------------|--------------------------|--------------------------|----------------------------------------------------|-------------|----------------|--------------|--------------------------|-------------|-----------|-----------|-----------------|--------------|
| Lq8QxKnN_5I | 2020-03-03T18:10:31.000Z | LOST my HAIR, When H...  | new meme album is boppin\n100...	 | PT14M9S  | public         | PewDiePie    | [SATIRE, pewdiepie,...]  | False       | 5854206   | 450998    | 6331         | 52937        |
| grphMTBly7Q | 2020-03-02T17:54:21.000Z |  Supergirl is Super C... | supergirl is super not epic  ...	 | PT10M30S | public         | PewDiePie    | [SATIRE]                 | False       | 5079267   | 554819    | 10956        |   32723        |

```python
yt_to_df(YOUR_DEVELOPER_KEY, ["Lq8QxKnN_5I", "grphMTBly7Q"])
```
results:
|  video_id   |       publishedAt        |       video_title        |            description              | duration | privacyStatus  | channelTitle |           tags           | madeForKids | viewCount | likeCount | dislikeCount | commentCount |
|-------------|--------------------------|--------------------------|----------------------------------------------------|-------------|----------------|--------------|--------------------------|-------------|-----------|-----------|-----------------|--------------|
| Lq8QxKnN_5I | 2020-03-03T18:10:31.000Z | LOST my HAIR, When H...  | new meme album is boppin\n100...	 | PT14M9S  | public         | PewDiePie    | [SATIRE, pewdiepie,...]  | False       | 5854206   | 450998    | 6331         | 52937        |
| grphMTBly7Q | 2020-03-02T17:54:21.000Z |  Supergirl is Super C... | supergirl is super not epic  ...	 | PT10M30S | public         | PewDiePie    | [SATIRE]                 | False       | 5079267   | 554819    | 10956        |   32723        |
