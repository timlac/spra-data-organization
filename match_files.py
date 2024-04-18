import os
from pathlib import Path

from read_biopac import get_biopac_df, remove_non_conforming_filenames
from read_video import get_video_df
import json

biopac_path = "/media/tim/TOSHIBA EXT/SPRätt/GEMEP biopac program och data/GEMEP biopac data"
video_path = "/media/tim/TOSHIBA EXT/AVIfiler"


biopac_df = get_biopac_df(biopac_path)
biopac_df.to_csv("/media/tim/TOSHIBA EXT/tim/biopac_original.csv", index=False)

print(biopac_df.head())

filtered_biopac_df = remove_non_conforming_filenames(biopac_df)
non_duplicate_biopac_df = filtered_biopac_df.drop_duplicates(subset=["readable_time"], keep=False)

video_df = get_video_df(video_path)
video_df.to_csv("/media/tim/TOSHIBA EXT/tim/avi_original.csv", index=False)
print(video_df.head())

non_duplicate_video_df = video_df.drop_duplicates(subset=["readable_time"], keep=False)

merged_df = non_duplicate_biopac_df.merge(non_duplicate_video_df, how='left', on='readable_time')
print(merged_df.head())

# check for duplicates
print("duplicates in merged")
print(merged_df[merged_df['code'].duplicated(keep=False)])

merged_df.to_csv("/media/tim/TOSHIBA EXT/tim/mappings.csv", index=False)

merged_df_no_nan = merged_df.dropna()

merged_json = json.loads(merged_df_no_nan.to_json(orient="records"))

filename2code = {}
for i in merged_json:
    filename2code[i['filename_video']] = i['code']

codes = set(filename2code.values())

renamed_files_path = "/media/tim/TOSHIBA EXT/tim/renamed_avi_files"

# Get all files in the directory
files = os.listdir(renamed_files_path)

# Loop through each file in the directory
for file in files:
    # Check if the file is in the dictionary to be renamed
    if file in filename2code:
        # Define the old and new file paths
        old_file_path = os.path.join(renamed_files_path, file)
        new_file_path = os.path.join(renamed_files_path, filename2code[file] + ".avi")

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{file}' to '{filename2code[file]}'")
    else:
        file_no_ext = Path(file).stem
        if file_no_ext not in codes:
            # If the file is not in the dictionary, delete it
            old_file_path = os.path.join(renamed_files_path, file)
            os.remove(old_file_path)
            print(f"Deleted '{file}' as it is not in the rename list.")
        else:
            print("skipped '{file}' as it is in the code list")
