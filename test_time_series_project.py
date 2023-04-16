# testing if modifications from book work on time series dataset
import pandas as pd
import datetime
import numpy as np


# open raw file downloaded to local machine:
raw_file_path = r'C:\LD2011_2014.txt'
raw_file = open(str(raw_file_path))

# use raw file to read csv and get raw dataframe:
raw_dataset = pd.read_csv(raw_file, delimiter=';', header=0, decimal=',', index_col=False, low_memory=False)

# check dataframe info and head:
print(raw_dataset.info)
print(raw_dataset.head)

# since column with datetime values doesn't have name, rename it to 'datetime':
data_timecol = raw_dataset.rename(columns={'Unnamed: 0':'datetime'})

# check dtypes for dataframe:
print(data_timecol.dtypes)

# transform rennamed column into datetime dtype:
data_timecol['datetime'] = pd.to_datetime(data_timecol['datetime'], format='%Y-%m-%d %H:%M:%S')

# resample data from 15min level to day level:
data_resamp = data_timecol.resample('D', on='datetime').sum()

# check to see if resampling went through:
print(data_resamp.info)
print(data_resamp.head)

# save resampled data to csv to be able to perform further changes:
data_resamp.to_csv(r'C:\Users\a\PycharmProjects\pythonProject\venv\Lib\DATASET_TIME_SERIES\time_series_dataframe_resampled.txt')

# open saved file:
resampled_file = open(r'C:\Users\a\PycharmProjects\pythonProject\venv\Lib\DATASET_TIME_SERIES\time_series_dataframe_resampled.txt')
resampled_data = pd.read_csv(resampled_file, delimiter=',', header=0)
resampled_data['datetime'] = pd.to_datetime(resampled_data['datetime'], format='%Y-%m-%d')

# check data status:
print(resampled_data.head)
print(resampled_data.info)
print(resampled_data.dtypes)

# before going on, lets remove the 'MT_' from the column names:
# first, create a dictionary of old and new column names, with new names as integers:
new_column_names = {col: col.replace('MT_', '') for col in resampled_data.columns if 'MT_' in col}
# next, use dictionary to rename old columns:
resampled_data = resampled_data.rename(columns=new_column_names)

# stack dataset by melting it (the value_name col will be recalculated after):
melted_data = pd.melt(resampled_data, id_vars=['datetime'], var_name='client_id', value_name='KwH')
# check changes: print(melted_data.head)
# change client_id col to int:
melted_data['client_id'] = melted_data['client_id'].astype(int)
# check changes: print(melted_data.dtypes)
# check head:
print(melted_data.head)
# make datetime as index to be able to do further changes:
# melted_data.set_index('datetime', inplace=True)
# check head:
print(melted_data.head)
# define starting and ending points for each client's data:
complete_idx = pd.MultiIndex.from_product((set(melted_data.datetime), set(melted_data.client_id)))
all_melted_data = melted_data.set_index(['datetime','client_id']).reindex(complete_idx, fill_value=0).reset_index()
all_melted_data.columns = ['datetime','client_id','KwH']
cutoff_dates = melted_data.groupby('client_id').datetime.agg(['min','max']).reset_index()
cutoff_dates = cutoff_dates.reset_index()

# remove dates before first and after last nonzero info for each client:
for _, row in cutoff_dates.iterrows():
    client_id = row['client_id']
    start_date = row['min']
    end_date = row['max']
    all_melted_data.drop(all_melted_data[all_melted_data.client_id == client_id][all_melted_data.datetime < start_date].index, inplace=True)
    all_melted_data.drop(all_melted_data[all_melted_data.client_id == client_id][all_melted_data.datetime > end_date].index, inplace=True)

# check data: print(all_melted_data.head)
# transform measure unit for column KwH from energy consumed
all_melted_data['KwH'] = all_melted_data['KwH'] * 4