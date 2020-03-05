# Extend and simplify frequent operations in Colab
This package contains modules that extend and simplify the intereaction with Pandas, BigQuery and YouTube.

To import all the functions of a module into a Colab notebook:
```
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
### Pandas
### YouTube
### BigQuery
### df_to_bq(df, table_location, partitioned=False)
### csv_to_bq(table_location, partitioned=False)
### bq_to_df(project_id, query)
### get_random_rows_from_bq_table(project_id, table_location, n_of_samples)
### list_datasets_from_bq_project(project_id)
```colab
list_datasets_from_bq_project('bigquery-public-data')[:3]
```
results:

```Python
['austin_311', 'austin_bikeshare', 'austin_crime']
```

### yt_to_df(developerKey, id)
```colab
yt_to_df(YOUR_DEVELOPER_KEY, 'UC-lHJZR3Gqxm24_Vd_AJ5Yw').head(3)
```
pull metadta from video or channel or playlist

results:
|   video_id   |       publishedAt       |       video_title        |                    description                     | channelTitle | tags | madeForKids | viewCount | likeCount | dislikeCount | commentCount |
|--------------|-------------------------|--------------------------|----------------------------------------------------|-------------------|-------------------------|--------------------------|-------------------|--------------------------------|-------------------|-------------------------|
| VgvvfSvg2bQ | 2020-02-23T17:30:01.000Z | What is Jake Paul up to? | The financial freedom movement is here thanks ...	 | PewDiePie | [SATIRE, What is Jake Paul up to?, jake paul, ...] | False | 6279395 | 554819 | 8267 46464 |
