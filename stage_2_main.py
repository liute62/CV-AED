#
# Used for detecting stage two, namely to see if yellow plug has been plugged
#
import feature_detetor


org_size = 0
detected_x = 0
detected_y = 0


def set_params(x,y,size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org


def retrieve_params():

    return detected_x,detected_y,org_size


def run(last_valid_frame,frame):
    feature_detetor.pre_size_estimate(1000, 3600)
    is_detected = feature_detetor.detect_stage_area(last_valid_frame, frame, detected_x, detected_y)
    return is_detected