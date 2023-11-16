import glob
import time
from datetime import datetime

import cv2
import numpy as np

import post_ir_image


def str_2_np(s):
    lines = s.splitlines()
    data_idx = lines.index("[Data]")
    lines = lines[data_idx + 1 : data_idx + 512]

    bytes_str = [l.replace(",", ".").strip("	").split("	") for l in lines]
    bytes = [list(map(float, l)) for l in bytes_str]
    np_arr = np.array(bytes)
    return np_arr


def read_from_asc(asc_file):
    with open(asc_file, encoding="CP932") as f:
        f = f.read()
        np_img = str_2_np(f)
    return np_img


def float_2_normalized(np_arr):
    np_img = 255 * (np_arr - np_arr.min()) / (np_arr.max() - np_arr.min())
    return np_img


if __name__ == "__main__":
    asc_files = sorted(glob.glob("asc/*.asc"))
    for f in asc_files:
        np_img = read_from_asc(f)
        img = float_2_normalized(np_img)

        current_time = datetime.now().strftime("%Y-%m-%d-%H%M%S%f")
        file_name = f"data/{current_time}.png"
        cv2.imwrite(file_name, img)
        time.sleep(1)
        post_ir_image.post_ir(file_name)
        time.sleep(2)
