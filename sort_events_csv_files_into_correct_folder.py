import os
import shutil
import pandas as pd


# Purpose: to separate the 4stim event tables and the stimulator (thermal/mechanical) event tables into two separate folder
# the stimulator files will be located at folder "sort_events_stimulator", those with 4stim will sit (remained) at "sorted_events"

# define csv folder path and meta data path, output folder path
metadata_csv = "C:/Users/silic/Desktop/electrophysiology-project/metadata_with_base_name_23_to_26.csv"

#csv_folder = "C:/Users/silic/Desktop/electrophysiology-project/sorted_events"  # your big folder
csv_folder = "C:/Users/silic/Downloads/sort_events_stimulator"

#output_folder = "C:/Users/silic/Downloads/sort_events_stimulator"  # new folder to create
output_folder = "C:/Users/silic/Downloads/sort_events_thermal_stimulator"  # new folder to create


# load metadata
df = pd.read_csv(metadata_csv)

# create output folder is it is not existence
os.makedirs(output_folder, exist_ok=True)

# filter files, select the rows that has either mechanical_stim or thermal_stim as non-NA 
#target = df['mechanical_stim'].notna() | df['thermal_stim'].notna()

# filter files, select the rows that has thermal_stim as non-NA 
target = df['thermal_stim'].notna()

filtered_df = df[target]

print(f"Found {len(filtered_df)} matching rows out of {len(df)} total.")

# version 1
# move these stimulator files into the target folder sort_events_stimulator
# those remaining in my sorted_events folder are the 4 stim files

# version 2
# move these thermal stimulator files into the target folder sort_events_thermal_stimulator
# those remaining in my sorted_events_stimulator folder are the mechanical stimulator files
moved_count = 0
missing_count = 0

for _, row in filtered_df.iterrows():
    prefix = row['file_name'].replace(".abf", "") # my metadata csv file_name column contains the file name of my abf (e.g 2026_06_04_0001.abf), i need to strip the extension off first
    fname = f"{prefix}_events.csv" # then create the new string stored as fname variable, with _events, which matches my current csv files (splitted by R studio code by me)
    src = os.path.join(csv_folder, fname)

    if not os.path.exists(src):
        print(f"warning: file not found, {src}")
        missing_count += 1
        continue

    dst = os.path.join(output_folder, fname)
    shutil.move(src, dst)
    print(f"Successully moved {fname} to destination{dst}")
    moved_count += 1

# version 1
#print(f"\nFinished moving {moved_count} stimulator files. {missing_count} were missing.")
# I moved 165 stimulator files, 209 were "missing", means that I did not really analyze it, or just the event table were absent somehow, coz no events detceted
# i need to later find out which recording had 0 events


# version 2
print(f"\nFinished moving {moved_count} thermal stimulator files. {missing_count} were missing.")
