#
# Used for detecting stage three, namely to see if orange button has been pressed
#
import flash_detetor

detected_x = 0
detected_y = 0


def set_params(x,y):
    global detected_x
    global detected_y
    detected_x = x
    detected_y = y


def retrieve_params():

    return detected_x,detected_y


def run(last_valid_frame,frame):
    is_detected = flash_detetor.flash_detection(last_valid_frame, frame, detected_x, detected_y)

    return is_detected