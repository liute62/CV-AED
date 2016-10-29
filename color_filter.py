#
# A filter to extract target color of AED device.
#
import cv2
import numpy as np


def filter_red(image1,image2):
    # loop over the contours
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([30, 135, 100])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1, res2


def filter_orange(image1,image2):
    # loop over the contours
    lower_blue = np.array([4, 135, 44])
    upper_blue = np.array([43, 255, 255])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1,res2