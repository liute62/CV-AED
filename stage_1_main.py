#
# Used for detecting stage one, namely to see if AED has been turned on
#

org_size = 0
detected_x = 0
detected_y = 0


def set_params(x, y,size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org


def retrieve_params():
    return detected_x, detected_y,org_size


def run(last_valid_frame,frame):

    return 0