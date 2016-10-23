import cv2
import numpy as np
from matplotlib import pyplot as plt
#
# This is an  for
#
#

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
    return abs(np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ))

last_size = 1

def area_estimate(area,type):
    area_size_1 = 0
    area_size_2 = 0
    #orange button
    if(type == 1):
        area_size_1 = 500
        area_size_2 = 1200
    #person hand
    elif type == 2:
        area_size_1 = 3000
        area_size_2 = 12000
    if area > area_size_1 and area < area_size_2:
        return True
    return False



def detect_stage_area(image1,image2):
    show_two_image(image1,image2)
    # loop over the contours
    lower_blue = np.array([6, 135, 44])
    upper_blue = np.array([43, 255, 255])
    hsv1 = cv2.cvtColor(image1,cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2,cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1, image1, mask=mask1)
    res2 = cv2.bitwise_and(image2, image2, mask=mask2)
    tmp1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
    tmp2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
    black1 = cv2.cvtColor(tmp1, cv2.COLOR_BGR2GRAY)
    black2 = cv2.cvtColor(tmp2, cv2.COLOR_BGR2GRAY)
    ret1, thresh1 = cv2.threshold(black1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(black2, 0, 255, cv2.THRESH_BINARY)
    show_two_image(black1,black2)
    cnts1, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts2, hierarchy = cv2.findContours(thresh2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    orange_btn1 = []
    orange_btn2 = []
    hand_1 = []
    hand_2 = []
    for cnt in cnts1:
        area0 = cv2.contourArea(cnt);
        # print area0
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area_estimate(area0,1):
            orange_btn1.append(cnt)
        if area_estimate(area0,2):
            hand_1.append(area0)
    print "------------"
    for cnt in cnts2:
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt);
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area_estimate(area0, 1):
            orange_btn2.append(area0)
        if area_estimate(area0, 2):
            hand_2.append(area0)
    print orange_btn1
    print orange_btn2
    print hand_1
    print hand_2
    #cv2.drawContours(thresh1,orange_btn1,-1, (0, 255, 0), 3)
    #cv2.drawContours(thresh2,orange_btn2,-1, (0, 255, 0), 3)
    #show_two_image(thresh1,thresh2)
    return False
    #return judgement(area1,area2,last_size)


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
