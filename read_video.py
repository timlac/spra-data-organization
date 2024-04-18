import os
from glob import glob
import time
import pandas as pd


def get_video_df(video_path):
    video_glob = glob(video_path + "/**/*.avi", recursive=True)

    video_map = {}

    for file_path in video_glob:
        mod_time = os.path.getmtime(file_path)
        # readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
        readable_time = time.strftime('%Y-%m-%d', time.localtime(mod_time))

        filename = os.path.basename(file_path)

        video_map[filename] = readable_time

    return pd.DataFrame(video_map.items(), columns=['filename_video', 'readable_time'])


if __name__ == '__main__':
    video_path = "/media/tim/TOSHIBA EXT"
    video_df = get_video_df(video_path)

    print(video_df.shape)
