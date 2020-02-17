# Colab Utils
This directory contains functions that extend and simplify the intereaction between Colab and files, Pandas dataframes and BigQuery.

## Functions
### BigQuery
* [df_to_bq](#df_to_bq)
* [csv_to_bq](#csv_to_bq)
* [bq_to_df](#bq_to_df)
* [get_random_rows_from_bq_table](#get_random_rows_from_bq_table)
* [list_datasets_from_bq_project](#list_datasets_from_bq_project)

### Pandas
* [csv_to_df](#csv_to_df)
* [excel_to_df](#excel_to_df)
* [gspread_to_dfs](#gspread_to_dfs)
* [df_to_csv](#df_to_csv)
* [df_to_gspread](#df_to_gspread)

### YouTube

## Documentation
### df_to_bq(df, table_location, partitioned=False)
### csv_to_bq(table_location, partitioned=False)
### bq_to_df(project_id, query)
### get_random_rows_from_bq_table(project_id, table_location, n_of_samples)
### list_datasets_from_bq_project(project_id)
