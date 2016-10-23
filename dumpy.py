import cv2
import numpy as np
from matplotlib import pyplot as plt

#img = cv2.imread('AED photos/AED.jpg')
#img = cv2.imread('AED photos/hand/1.jpg')
#img = cv2.imread('AED photos/WechatIMG5.jpeg')
img = cv2.imread('AED photos/stage2/1.jpg')
#plt.imshow(img, interpolation='bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#plt.show()
#img2 = cv2.medianBlur(img,5)
#plt.imshow(img2, interpolation='bicubic')

#clip an area of the image
#box = img[1700:2300,1500:2000]
#plt.imshow(box, interpolation='bicubic')
#plt.show()


#
# Detection for right panel circle
#
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])
# mask = cv2.inRange(hsv, lower_blue, upper_blue)
# res = cv2.bitwise_and(img,img, mask= mask)
# plt.imshow(img)
# plt.show()
# #plt.imshow(mask,interpolation='bicubic')
# #cv2.imshow('res',res)
# plt.imshow(res,interpolation='bicubic')
# plt.show()


#
# Detection for bottom triangle
#
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_blue = np.array([5,47,47])
upper_blue = np.array([43,255,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(img,img, mask= mask)
plt.imshow(img)
plt.show()
#plt.imshow(mask,interpolation='bicubic')
#cv2.imshow('res',res)
plt.imshow(res,interpolation='bicubic')
plt.show()


#
#
#
#
#gray= cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT()
kp = sift.detect(res,None)
img=cv2.drawKeypoints(res,kp)
cv2.imwrite('sift_keypoints.jpg',img)


#
# Detection for canny edge
# 1. 5 X 5 Gaussian filter
# 2.
# http://docs.opencv.org/trunk/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de
# http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
#
# img = res
# img = cv2.bilateralFilter(img,9,75,75)
# edges = cv2.Canny(img, 0, 72)
# plt.subplot(121), plt.imshow(img, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()


#
# Find contours of a binary image:
#
# imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(res, contours, -1, (0, 255, 0), 3)
# plt.imshow(res, interpolation='bicubic')
# plt.show()

#
# Find Corner with SubPixel Accuracy
#
# imgray = cv2.cvtColor(imgRaw,cv2.COLOR_BGR2GRAY)
# gray = np.float32(imgray)
# dst = cv2.cornerHarris(gray,2,3,0.04)
# #result is dilated for marking the corners, not important
# dst = cv2.dilate(dst,None)
# # Threshold for an optimal value, it may vary depending on the image.
# imgRaw[dst>0.01*dst.max()]=[0,0,255]
# plt.imshow(imgRaw, interpolation='bicubic')
# plt.show()

# OpenCV has a function, cv2.goodFeaturesToTrack(). It finds N strongest corners in
# the image by Shi-Tomasi method (or Harris Corner Detection, if you specify it).
#  As usual, image should be a grayscale image. Then you specify number of corners you want to find.
#  Then you specify the quality level, which is a value between 0-1,
# which denotes the minimum quality of corner below which everyone is rejected.
#  Then we provide the minimum euclidean distance between corners detected.
# With all these informations, the function finds corners in the image.
#  All corners below quality level are rejected.
# Then it sorts the remaining corners based on quality in the descending order.
# Then function takes first strongest corner,
#  throws away all the nearby corners in the range of mini mum distance and returns N strongest corners.
# In below example, we will try to find 25 best corners

# gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
# corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
# corners = np.int0(corners)
# for i in corners:
#     x,y = i.ravel()
#     cv2.circle(img,(x,y),3,255,-1)
# plt.imshow(img),plt.show()

