import os
from glob import glob
import time
import re
import pandas as pd


def get_biopac_df(biopac_path):
    biopac_glob = glob(biopac_path + "/**/*.acq", recursive=True)

    biopac_map = []

    for file_path in biopac_glob:
        mod_time = os.path.getmtime(file_path)
        # readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
        readable_time = time.strftime('%Y-%m-%d', time.localtime(mod_time))

        filename = os.path.basename(file_path)
        code = re.match(r"[\w]+", filename).group()

        single_map = {"filename_biopac": filename, "code": code, "readable_time": readable_time}
        biopac_map.append(single_map)

    return pd.DataFrame(biopac_map)


def remove_non_conforming_filenames(df):
    # Regex pattern to match 'code gemep.acq'
    pattern = r'^\w+ gemep\.acq$'

    # Filter DataFrame to include only rows that match the pattern
    filtered_df = df[df['filename_biopac'].str.match(pattern)]

    return filtered_df

