# Extend and simplify frequent operations in Colab
This package contains modules that extend and simplify the intereaction with Pandas, BigQuery and YouTube.

To import all the functions of a module into a Colab notebook:
```python
!git clone https://github.com/omarambrosi/colab_utils
import sys
sys.path.append('colab_utils')
import colab_youtube
```

## Functions

### Pandas
* [csv_to_df]
* [excel_to_df]
* [gspread_to_dfs]
* [df_to_csv]
* [df_to_gspread]

### BigQuery
* [df_to_bq](#df_to_bqdf-table_location-partitionedfalse)
* [csv_to_bq](#csv_to_bqtable_location-partitionedfalse)
* [gspread_to_bq]
* [bq_to_df](#bq_to_dfproject_id-query)
* [get_random_rows_from_bq_table](#get_random_rows_from_bq_tableproject_id-table_location-n_of_samples)
* [list_datasets_from_bq_project](#list_datasets_from_bq_projectproject_id)

### YouTube
* [yt_to_df]
* [cid_to_df]

## Documentation
## Pandas
## BigQuery
### [df_to_bq(df, table_location, partitioned=False)](colab_bigquery.py)
### [csv_to_bq(table_location, partitioned=False)](colab_bigquery.py)
### [bq_to_df(project_id, query)](colab_bigquery.py)
### [get_random_rows_from_bq_table(project_id, table_location, n_of_samples)](colab_bigquery.py)
### [list_datasets_from_bq_project(project_id)](colab_bigquery.py)
```python
list_datasets_from_bq_project('bigquery-public-data')[:3]
```
results:
```python
['austin_311', 'austin_bikeshare', 'austin_crime']
```
## YouTube
### [yt_to_df(developerKey, id)](colab_youtube.py)
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
             | False       | 7086811   | 515929    | 6571         |  28694        |
