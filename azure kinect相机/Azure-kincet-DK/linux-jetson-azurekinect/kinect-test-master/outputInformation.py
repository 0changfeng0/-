import sys

sys.path.insert(1, './pyKinectAzure/')

import numpy as np
import cv2

from pyKinectAzure import pyKinectAzure, _k4a

# TODO: 添加 Azure Kinect SDK 路径
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

if __name__ == '__main__':

    # 初始化
    pyK4A = pyKinectAzure(modulePath)
    pyK4A.device_open()
    device_config = pyK4A.config
    device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
    print(device_config)

    # 开启摄像头
    pyK4A.device_start_cameras(device_config)
    while True:
        pyK4A.device_get_capture()
        color_image_handle = pyK4A.capture_get_color_image()
        depth_image_handle = pyK4A.capture_get_depth_image()

        if color_image_handle:
            color_image = pyK4A.image_convert_to_numpy(color_image_handle)
            print(color_image.shape)
            depth_image = pyK4A.image_convert_to_numpy(depth_image_handle)
            print(depth_image.shape)
            depth_color_image = cv2.convertScaleAbs(depth_image, alpha=0.05)
            depth_color_image = cv2.applyColorMap(depth_color_image, cv2.COLORMAP_JET)
            # merge_image = np.hstack([color_image, depth_color_image])

            # cv2.namedWindow('Color & Colorized Depth Image', cv2.WINDOW_NORMAL)
            # cv2.imshow("Color Image", merge_image)
            pyK4A.image_release(color_image_handle)
        pyK4A.capture_release()

        # Q 键停止
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()
