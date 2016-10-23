import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

def show_two_image(image1,image2):
    img_two = np.concatenate((image1, image2), axis=1)
    plt.imshow(img_two)
    plt.show()

def shape_detect(c):
    shape = "unidentified"
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.04 * peri,True)
    print approx

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ))

last_size = 1
def detect_stage_area(image1,image2):
    area_size_1 = 20000
    area_size_2 = 80000
    # loop over the contours
    lower_blue = np.array([8, 135, 47])
    upper_blue = np.array([43, 255, 255])
    hsv1 = cv2.cvtColor(img_noplug_raw,cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img_plug_raw,cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(img_noplug_raw, img_noplug_raw, mask=mask1)
    res2 = cv2.bitwise_and(img_plug_raw, img_plug_raw, mask=mask2)
    tmp1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
    tmp2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
    black1 = cv2.cvtColor(tmp1, cv2.COLOR_BGR2GRAY)
    black2 = cv2.cvtColor(tmp2, cv2.COLOR_BGR2GRAY)
    ret1, thresh1 = cv2.threshold(black1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(black2, 0, 255, cv2.THRESH_BINARY)
    show_two_image(black1,black2)
    cnts1, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts2, hierarchy = cv2.findContours(thresh2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    aimed1 = []
    aimed2 = []
    area1 = []
    area2 = []
    for cnt in cnts1:
        area0 = cv2.contourArea(cnt);
        # print area0
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area0 > area_size_1 and area0 < area_size_2:
            aimed1.append(cnt)
            area1.append(area0)
    print "------------"
    for cnt in cnts2:
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt);
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area0 > area_size_1 and area0 < area_size_2:
            aimed2.append(cnt)
            area2.append(area0)
    print area1
    print area2
    cv2.drawContours(thresh1,aimed1,-1, (0, 255, 0), 3)
    cv2.drawContours(thresh2,aimed2,-1, (0, 255, 0), 3)
    show_two_image(thresh1,thresh2)
    return judgement(area1,area2,last_size)

stable_counter = 0
is_start = False
def judgement(area1,area2,last):
    is_have = False
    stable_threshold = 1
    global stable_counter;
    global is_start;
    length_1 = len(area1)
    length_2 = len(area2)
    if length_1 == length_2:
        is_have = False
        if is_start:
            stable_counter = stable_counter+1
    else:
        is_start = True
        if length_2 > length_1:
            is_have = False
            #print "more"
        else:
            print "less"
            #is_have = True
    if(stable_counter > stable_threshold):
        is_have = True
    return is_have


for i in range(1,2):
    str1 = 'AED photos/exception/shadow.jpg'
    #str1 = 'AED photos/stage1/'+str(i)+'.jpg'
    str2 = 'AED photos/stage1/'+str(i+1)+'.jpg'
    str2 = str1
    img_noplug_raw = cv2.imread(str1)
    img_plug_raw = cv2.imread(str2)
    show_two_image(img_noplug_raw,img_plug_raw)
    is_have = detect_stage_area(img_noplug_raw,img_plug_raw)
    if is_have:
        print 'plug at image '+str1+'and image '+str2


#
# Detection for yellow plug
#
#hsv1 = cv2.cvtColor(img_noplug_raw,cv2.COLOR_BGR2HSV)
#hsv2 = cv2.cvtColor(img_plug_raw,cv2.COLOR_BGR2HSV)

# loop over the contours
# lower_blue = np.array([8,135,47])
# upper_blue = np.array([43,255,255])
# mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
# mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
# res1 = cv2.bitwise_and(img_noplug_raw,img_noplug_raw, mask= mask1)
# res2 = cv2.bitwise_and(img_plug_raw,img_plug_raw,mask=mask2)
#show_two_image(res1,res2)
#
# tmp1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
# tmp2 = cv2.cvtColor(res2,cv2.COLOR_HSV2BGR)
# black1 = cv2.cvtColor(tmp1,cv2.COLOR_BGR2GRAY)
# black2 = cv2.cvtColor(tmp2,cv2.COLOR_BGR2GRAY)
#
# ret1,thresh1 = cv2.threshold(black1,0,255,cv2.THRESH_BINARY)
# ret2,thresh2 = cv2.threshold(black2,0,255,cv2.THRESH_BINARY)
# cnts1, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# cnts2, hierarchy = cv2.findContours(thresh2.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cnts1 = cnts1[0] if imutils.is_cv2() else cnts1[1]
#cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
# aimed1 = []
# aimed2 = []
# for cnt in cnts1:
#     area0 = cv2.contourArea(cnt);
#     #print area0
#     cnt_len = cv2.arcLength(cnt, True)
#     cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
#     if area0 < 3000.0:
#         print "yes"
#     else:
#         aimed1.append(cnt)
#         print area0
#     #print len(cnt)
#     #print cv2.contourArea(cnt)
#     #print cv2.isContourConvex(cnt)
#     #if len(cnt) > 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
#         #cnt = cnt.reshape(-1, 2)
#         #max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
#         #if max_cos < 0.1:
#         #aimed1.append(cnt)
#     #else:
#     #    print cnt
# print "-----------"
# for cnt in cnts2:
#     cnt_len = cv2.arcLength(cnt, True)
#     #print cnt_len
#     area0 = cv2.contourArea(cnt);
#     #print area0
#     cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
#     if area0 < 11406.0:
#         print "yes";
#     else:
#         aimed2.append(cnt)
#         print area0
#     #print len(cnt)
#     #print cv2.contourArea(cnt)
#     #print cv2.isContourConvex(cnt)
#     #if len(cnt) > 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
#         #cnt = cnt.reshape(-1, 2)
#         #max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
#         #if max_cos < 0.1:
#     #    aimed2.append(cnt)
#     #else:
#      #   print cnt

#print aimed1
#print aimed2
#is_have = detect_stage_area(1,img_noplug_raw,img_plug_raw)
#print is_have
#show_two_image(thresh1,thresh2)
#cv2.drawContours(thresh1,aimed1,-1, (0, 255, 0), 3)
#cv2.drawContours(thresh2,aimed2,-1, (0, 255, 0), 3)
#show_two_image(thresh1,thresh2)

# for c in cnts1:
#     shape_detect(c)
#     M = cv2.moments(c)
#     cv2.putText(black1, "shape", (0, 0), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5, (255, 255, 255), 2)
# print "------------"
# for c in cnts2:
#     shape_detect(c)
#     cv2.drawContours(black2, [c], -1, (0, 255, 0), 2)
# show_two_image(black1,black2)



#
# SURF
#
# surf = cv2.SURF(4000)
# kp1, des1 = surf.detectAndCompute(black1,None)
# kp2, des2 = surf.detectAndCompute(black2,None)
#
# rows1 = black1.shape[0]
# cols1 = black1.shape[1]
# rows2 = black1.shape[0]
# cols2 = black1.shape[1]
# out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
# # Place the first image to the left
# out[:rows1,:cols1] = np.dstack([black1, black1, black1])
# # Place the next image to the right of it
# out[:rows2,cols1:] = np.dstack([black2, black2, black2])
# matches = []
# # For each pair of points we have between both images
# # draw circles, then connect a line between them
# for mat in matches:
#     # Get the matching keypoints for each of the images
#     img1_idx = mat.queryIdx
#     img2_idx = mat.trainIdx
#     # x - columns
#     # y - rows
#     (x1,y1) = kp1[img1_idx].pt
#     (x2,y2) = kp2[img2_idx].pt
#     # Draw a small circle at both co-ordinates
#     # radius 4
#     # colour blue
#     # thickness = 1
#     cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
#     cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)
#
#     # Draw a line in between the two points
#     # thickness = 1
#     # colour blue
#     cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)
#     # Show the image
#     cv2.imshow('Matched Features', out)


#
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# lower_blue = np.array([5,47,47])
# upper_blue = np.array([43,255,255])
# mask = cv2.inRange(hsv, lower_blue, upper_blue)
# res = cv2.bitwise_and(img,img, mask= mask)
# plt.imshow(img)
# plt.show()
# #plt.imshow(mask,interpolation='bicubic')
# #cv2.imshow('res',res)
# plt.imshow(res,interpolation='bicubic')
# plt.show()
#
# #
# # FAST
# #
# # Initiate FAST object with default values
# fast = cv2.FastFeatureDetector()
# # find and draw the keypoints
# kp = fast.detect(res,None)
# img2 = cv2.drawKeypoints(res, kp, color=(255,0,0))
# # Print all default params
# # print "Threshold: ", fast.getInt('threshold')
# # print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
# # print "neighborhood: ", fast.getInt('type')
# # print "Total Keypoints with nonmaxSuppression: ", len(kp)
#
# cv2.imwrite('fast_true.png',img2)
# # Disable nonmaxSuppression
# fast.setBool('nonmaxSuppression',0)
# kp = fast.detect(res,None)
# print "Total Keypoints without nonmaxSuppression: ", len(kp)
# img3 = cv2.drawKeypoints(res, kp, color=(255,0,0))
# cv2.imwrite('fast_false.png',img3)