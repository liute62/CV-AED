import cv2
import feature_detetor

str1 = 'video/AED1.mp4'
cap = cv2.VideoCapture(str1)
while not cap.isOpened():
    cap = cv2.VideoCapture(str1)
    cv2.waitKey(1000)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
last_pos_frame = 1
frame_counter = 0
frame_sampling = 20
while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        if(pos_frame > last_pos_frame+frame_sampling):
            if frame_counter > 3:
                feature_detetor.detect_stage_area(last_valid_frame,frame)
                #gray = cv2.cvtColor(last_valid_frame, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('video', gray)
            last_pos_frame = pos_frame
            last_valid_frame = frame
            frame_counter = frame_counter + 1
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
