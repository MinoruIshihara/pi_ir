import cv2
from cv2 import add
from flirpy.camera.boson import Boson
import numpy as np
import time
import os
import datetime

# every ffc
# 0.sudo chmod 666 /dev/ttyACM0
# 1.capture-const-ffc 2.calc-csv 3.plt-csv

with Boson() as camera:
    while True:
        tmp = camera.grab().astype(np.float32)
        # Rescale to 8 bit
        img = 255 * (tmp - tmp.min()) / (tmp.max() - tmp.min())
        """ Apply colourmap - try COLORMAP_JET if INFERNO doesn't work. 
            You can also try PLASMA or MAGMA
            img_col = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO)
        """
        img = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO)
        img = img.astype(np.uint8)
        cv2.imshow("Boson", img)

        key = cv2.waitKey(1) & 0xFF
        dt_now = datetime.datetime.now()
        # y, m, d, h = dt_now.year, dt_now.month, dt_now.day, dt_now.hour
        min, s = dt_now.minute, dt_now.second
        name = "{}".format(dt_now.strftime("%Y%m%d_%H%M%S"))
        name_tiff = name + ".tiff"

        # if int(s) % 60 == 0 and int(min) % 30 == 0:
        #     camera.do_ffc()
        #     np.save("np/" + name, tmp)
        #     cv2.imwrite("capture/" + name_tiff, img)
        #     print("Saved {} & {}".format(name, name_tiff))
        #     time.sleep(1)
        # elif int(s) % 10 == 0:
        #     """
        #     camera.do_ffc()
        #     np.save("np/" + name, tmp)
        #     print("Saved {}".format(name))
        #     # cv2.imwrite("capture/" + name_tiff, img)
        #     # print("Saved {} & {}".format(name, name_tiff))
        #     time.sleep(1)
        #     """
        #     camera.do_ffc()
        #     np.save("np/" + name, tmp)
        #     print("Saved {}".format(name))
        #     time.sleep(1)

        if key == ord("q"):
            break  # esc to quit

        if key == ord("s"):
            camera.do_ffc()
            np.save(name, tmp)
            time.sleep(1)

        if key == ord("c"):
            camera.do_ffc()
            # np.save(name, tmp)
            time.sleep(1)
            # 画像を保存
            # cv2.imwrite("capture/" + name_tiff, img)
            cv2.imwrite(name_tiff, img)
            print("Saved {} & {}".format(name, name_tiff))

cv2.destroyAllWindows()
