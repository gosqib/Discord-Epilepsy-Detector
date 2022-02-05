from typing import Optional, Union
import cv2 as cv #type:ignore
import numpy as np

from keyvars.consts import TEST_DATA_DIR

def c_resize(img: np.ndarray, text_width_min: int = 200) -> np.ndarray:
    """resize image - used to resize the text image accordingly
    width_min expects the minimum width of the text-based image's 
    which is used to create the image with
    """

    scale_factor = text_width_min / img.shape[1] #img.shape[1] is width
    height, width = (
        dimension * scale_factor
        for dimension
        in img.shape[: 2] # gives (height, width)
    )

    # cv2.resize requires int arguments
    # map over list comp for performance boost even accounting for tuple conversion
    dimensions: map[int] = map(int, (width, height))
    
    # tuple > list for space
    return cv.resize(img, tuple(dimensions))



YESEP_VIDEO     = cv.VideoCapture(f'{TEST_DATA_DIR}/epil.mp4')
NOEP_VIDEO      = cv.VideoCapture(f'{TEST_DATA_DIR}/randomvid.mp4')
MIX_VIDEO       = cv.VideoCapture(f'{TEST_DATA_DIR}/mix.mp4')
TEST_VIDEO      = cv.VideoCapture(f'{TEST_DATA_DIR}/Me at the zoo.mp4')

