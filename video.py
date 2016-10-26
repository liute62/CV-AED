import cv2
import feature_detetor
import util


str1 = 'video/AED3.mp4'
cap = cv2.VideoCapture(str1)
while not cap.isOpened():
    cap = cv2.VideoCapture(str1)
    cv2.waitKey(1000)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
last_pos_frame = 1
frame_counter = 0
frame_sampling = 10

CONST_STAGE_PLUG = 0
CONST_STAGE_FLASH_BTN = 1
CONST_STAGE_SHOCK_DELIVER = 2
current_stage = CONST_STAGE_PLUG


while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        if(pos_frame > last_pos_frame+frame_sampling):
            if frame_counter > 3:
                if current_stage == CONST_STAGE_PLUG:
                    is_detected = feature_detetor.detect_stage_area(last_valid_frame,frame)
                    if is_detected:
                        print "detect the yellow plug, now turn to stage 2"
                    current_stage = CONST_STAGE_FLASH_BTN
                elif current_stage == CONST_STAGE_FLASH_BTN:
                    print "CONST_STAGE_FLASH_BTN"

                elif current_stage == CONST_STAGE_SHOCK_DELIVER:
                    print "CONST_STAGE_SHOCK_DELIVER"
                #gray = cv2.cvtColor(last_valid_frame, cv2.COLOR_BGR2GRAY)
                #util.show_resized_img(gray)
                #cv2.imshow('video', gray)
            last_pos_frame = pos_frame
            last_valid_frame = frame
            frame_counter = frame_counter + 1
            print "####################"
            #cv2.imshow('video', frame)
            #print str(pos_frame)+" frames"
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
        print "frame is not ready"
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 32:
        break
    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break
