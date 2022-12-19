

import sys

sys.path.insert(1, './pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

# 添加 Azure Kinect SDK 路径
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

#对获取的深度图像进行颜色处理
def color_depth_image(depth_image):
    depth_color_image = cv2.convertScaleAbs(depth_image,
                                            alpha=0.05)  # alpha is fitted by visual comparison with Azure k4aviewer results
    depth_color_image = cv2.applyColorMap(depth_color_image, cv2.COLORMAP_JET)

    return depth_color_image


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 初始化
    pyK4A = pyKinectAzure(modulePath)
    pyK4A.device_open()
    device_config = pyK4A.config
    device_config.color_format = _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
    device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_720P
    device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
    print(device_config)

    # 开启摄像头
    pyK4A.device_start_cameras(device_config)
    #获取相机序列号
    serial_number=pyK4A.device_get_serialnum()
    print(serial_number)

    k = 0
    while True:
        # Get capture
        pyK4A.device_get_capture()

        # Get the depth image from the capture
        depth_image_handle = pyK4A.capture_get_depth_image()

        # Get the color image from the capture
        color_image_handle = pyK4A.capture_get_color_image()

        # Check the image has been read correctly
        if depth_image_handle and color_image_handle:

            # Read and convert the image data to numpy array:
            color_image = pyK4A.image_convert_to_numpy(color_image_handle)[:, :, :3]
            depth_image=pyK4A.image_convert_to_numpy(depth_image_handle)
            depth_image=color_depth_image(depth_image)



            cv2.namedWindow(' Color Image', cv2.WINDOW_NORMAL)
            cv2.imshow(' Color Image', color_image)
            cv2.namedWindow(' Depth Image', cv2.WINDOW_NORMAL)
            cv2.imshow(' Depth Image', depth_image)
            k = cv2.waitKey(25)
            if k == 27:  # Esc
                break

        pyK4A.image_release(depth_image_handle)
        pyK4A.image_release(color_image_handle)

        pyK4A.capture_release()


    pyK4A.device_stop_cameras()
    pyK4A.device_close()


