import cv2 as cv#type:ignore

# notify person of epilepsy detection
EPILEPSY_DETECTION_REACTIONS = ['🔺', '🇸', '🇪', '🇮', '🇿', '🇺', '🇷', '📸', '🔻']

# frame data
NO_PORTIONS, VERT_PORTIONS, HORIZ_PORTIONS = (8, 2, 4)

# where test data is found
TEST_DATA_DIR = 'testdata'

"""used in analysis"""
# fluid
DANGER_TRIGGER_REQUIREMENT  = 8
DRAMATIC_PIXEL_CHANGE       = 200
PORTION_DATA_MAX_CAPACITY   = 10
FRAME_SKIP_START            = 1
FRAME_COLLECTION_SKIP       = 2

#statics
MP4_DANG_TRIG_REQ = 8
MP4_DRAM_PIX_CHANGE = 200

# change in values due to gif form should be a decrease
# doing this just in case i'm sleepy
GIF_DANG_TRIG_REQ = min(DANGER_TRIGGER_REQUIREMENT, 1)
GIF_DRAM_PIX_CHANGE = min(DRAMATIC_PIXEL_CHANGE, 180)
