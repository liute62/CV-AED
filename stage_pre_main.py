#
# The preparation for detecting the following three stages.
#
import aed_detector

detected_org_x = 0
detected_org_y = 0
detected_org_size = 0


def retrieve_pos():
    return detected_org_x,detected_org_y


def retrieve_size():
    return detected_org_size


def prepare(last_valid_frame,frame):

    is_prepared = True
    global detected_org_x
    global detected_org_y

    is_aed_detected = aed_detector.aed_detect(last_valid_frame, frame)
    # now find the orange button and other important items precisely
    if is_aed_detected:
        # get the orange button position and relative size
        a = 0
    else:
        is_prepared = False
    return is_prepared
