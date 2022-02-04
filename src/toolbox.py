import cv2 as cv #type:ignore
from typing import Generator
import numpy as np

from consts import *

def get_frames(video: cv.VideoCapture) -> Generator[np.ndarray, None, None]:
	while 1:
		status, frame = video.read()
		if status == False:
			break
		
		yield frame

