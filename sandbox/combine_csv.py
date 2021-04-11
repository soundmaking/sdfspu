""" sandbox/combine_csv.py

input: none yet - could be path to directory
process: get data from all csv files in the given directory
output: write a csv file which has all the data

assumptions:
  - all input csv have
     - the same header columns
     - the same encoding

created: by sdf 2021-04-11
"""
# # Adapted from
# # https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py
# # credited:
# # https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052
# # this version using sdfspu instead of pandas

import os
import glob
# import pandas as pd
from sdfspu import csv_data as cd

# # set working directory
dir_path = "/home/pi/Documents/bf/bookings/2021Q1"
os.chdir(dir_path)

# # find all csv files in the folder
# # use glob pattern matching -> extension = 'csv'
# # save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
print(f'Found {len(all_filenames)} csv files in\n\t{dir_path}')

# # combine all files in the list

# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_data = cd.DataObject()
count_loaded = 0
for f in all_filenames:
    f_data = cd.DataObject()
    if f_data.read_csv(f, 'iso-8859-14'):
        count_loaded += 1
        combined_data.dict_list.extend(f_data.dict_list)
    else:
        print(
            f'{f_data.info["load_msg"]}'
            f'\n\t{f_data.info["path_to_source"]}'
        )
print(
    f'combined_data: {len(combined_data.dict_list)} rows '
    f'loaded from {count_loaded} files'
)

# # export to csv
# combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')
file_name = f'{dir_path.rsplit("/", 1)[-1]}_combined_csv.csv'
key_homogenised_dict_list = cd.key_homogenised_dict_list(
    combined_data.dict_list
)
print(f'writing file to: {file_name}')
cd.write_dict_list_to_csv(key_homogenised_dict_list, file_name)
