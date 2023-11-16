import datetime
import os
import time

import cv2
import numpy as np
import requests
from cv2 import add
from flirpy.camera.boson import Boson


def get_ir():
    root_path = "/etc/ir-camera-client/"

    with Boson() as camera:
        tmp = camera.grab().astype(np.float32)
        # Rescale to 8 bit
        img = 255 * (tmp - tmp.min()) / (tmp.max() - tmp.min())
        """ Apply colourmap - try COLORMAP_JET if INFERNO doesn't work. 
            You can also try PLASMA or MAGMA
            img_col = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO)
        """
        img = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO)
        img = img.astype(np.uint8)

        key = cv2.waitKey(1) & 0xFF
        dt_now = datetime.datetime.now()
        # y, m, d, h = dt_now.year, dt_now.month, dt_now.day, dt_now.hour
        min, s = dt_now.minute, dt_now.second
        name = "{}".format(dt_now.strftime("%Y%m%d_%H%M%S"))
        name_jpg = root_path + name + ".jpg"

        camera.do_ffc()
        # np.save(name, tmp)
        time.sleep(1)
        # 画像を保存
        # cv2.imwrite("capture/" + name_jpg, img)
        cv2.imwrite(name_jpg, img)
        print("Saved {} & {}".format(name, name_jpg))

        return name_jpg


def post_ir(img_name):
    host_name = "http://163.221.158.54:8080/wallpaper/"

    headers = {
        "Content-Type": "multipart/form-data",
    }
    data = {
        "name": img_name,
    }
    files = {"file": open(img_name, "rb")}
    path = "image/"
    res = requests.post(host_name + path, files=files, data=data)
    return res


def get_and_post_ir():
    file_name = get_ir()
    print(post_ir(file_name))
