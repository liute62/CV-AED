#
# Used for detecting the feature of AED device
#
import cv2
import numpy as np
from matplotlib import pyplot as plt
#
# This is an for
#
#

area_orange_btn_x = []
area_orange_btn_y = []



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

def area_range_estimate(areaX,areaY,type):
    area_x_left = 0
    area_x_right = 0
    area_y_right = 0
    area_y_left = 0
    area_y = 0
    if(type == 1):
        area_x_left = 300
        area_x_right = 600
        area_y_left = 30
        area_y_right = 500
    if(areaX < area_x_left or areaX > area_x_right):
        return False
    if(areaY < area_y_left or areaY > area_y_right):
        return False
    return True

#
# to estimate the area size of the target is within the range
#
def area_estimate(area,type):
    area_size_1 = 0
    area_size_2 = 0
    #orange button
    if(type == 1):
        area_size_1 = 1600
        area_size_2 = 3500
    #person hand
    elif type == 2:
        area_size_1 = 10000
        area_size_2 = 120000
    if area > area_size_1 and area < area_size_2:
        return True
    return False

def refresh():
    print "refresh"

def determine_orange_btn(array1,array2):
    to_return1 = array1[0]
    to_return2 = array2[0]
    min_dis = 100000000
    for cnt1 in array1:
        for cnt2 in array2:
            x1, y1, w1, h1 = cv2.boundingRect(cnt1)
            x2, y2, w2, h2 = cv2.boundingRect(cnt2)
            dis = np.abs(x1 - x2) ** 2 + np.abs(y1 - y2) ** 2
            if(dis < min_dis):
                min_dis = dis
                to_return1 = cnt1
                to_return2 = cnt2
    return to_return1,to_return2

def determine_yellow_plug(cnts,btn_x,btn_y):
    slope_left = 3
    slope_right = 5
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        print x,y,btn_x,btn_y
        if x != btn_x:
            slope = float(np.abs(y - btn_y)) / float(np.abs(x - btn_x))
            #print "SLOPE1"
            #print slope
            #print "SLOPE2"
            if(slope > slope_left and slope < slope_right):
                print slope,x,y
                return 1
    return 0

confidence_counter = 0
def detect_stage_area(image1,image2):

    # loop over the contours
    lower_blue = np.array([4, 135, 44])
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
    #show_two_image(black1,black2)

    cnts1, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts2, hierarchy = cv2.findContours(thresh2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    org_btn_candidate_1 = []
    org_btn_candidate_2 = []
    yellow_plug_candidate_1 = []
    yellow_plug_candidate_2 = []

    for cnt in cnts1:
        area0 = cv2.contourArea(cnt)
        #if area0 > 10:
        #    print area0
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area_estimate(area0,1):
            x, y, w, h = cv2.boundingRect(cnt)
            print w,h,x,y
            org_btn_candidate_1.append(cnt)
            #if area_range_estimate(x,y,1):
             #   org_btn_candidate_1.append(area0)
    print "------------start"
    for cnt in cnts2:
        #if area0 > 10:
         #   print area0
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt);
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area_estimate(area0, 1):
            x, y, w, h = cv2.boundingRect(cnt)
            print w, h,x,y
            org_btn_candidate_2.append(cnt)
            #if area_range_estimate(x,y,1):
             #   org_btn_candidate_2.append(area0)
    print '------------end'
    cnt1,cnt2 = determine_orange_btn(org_btn_candidate_1,org_btn_candidate_2)
    x, y, w, h = cv2.boundingRect(cnt1)
    #print w, h, x, y
    result1 = determine_yellow_plug(org_btn_candidate_1,x,y)
    x, y, w, h = cv2.boundingRect(cnt2)
    #print w, h, x, y
    result2 = determine_yellow_plug(org_btn_candidate_2,x,y)
    if(result1 == 1 and result2 == 1):
        global confidence_counter;
        confidence_counter += 1
    if(confidence_counter > 3):
        show_two_image(black1,black2)
        return True
    return False
    #cv2.drawContours(thresh1,orange_btn1,-1, (0, 255, 0), 3)
    #cv2.drawContours(thresh2,orange_btn2,-1, (0, 255, 0), 3)
    #show_two_image(thresh1,thresh2)
    #return False
    #return img_two
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
