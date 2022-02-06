from typing import Optional
import cv2 as cv #type: ignore
import numpy as np

from toolbox import get_frames
from testing import TEST_VIDEO
from keyvars.consts import (
	HORIZ_PORTIONS, 
	VERT_PORTIONS, 
	FRAME_SKIP_START,
	FRAME_COLLECTION_SKIP,
	NO_PORTIONS,
	PORTION_DATA_MAX_CAPACITY,
)

class Detector:
	__doc__ = """
	check video for certain features
		- epilepsy: .epilepsy(); (only hard flashing lights)
	"""
	
	def __init__(self, video: cv.VideoCapture) -> None:
		self._video = video
		self._vid_width = self._video.get(cv.CAP_PROP_FRAME_WIDTH)
		self._vid_height = self._video.get(cv.CAP_PROP_FRAME_HEIGHT)
		
		# dimensions of each eq portion, mapping for efficiency
		self._portion_width, self._portion_height = map(
			round, 
			(self._vid_width / HORIZ_PORTIONS, self._vid_height / VERT_PORTIONS)
		)

		self._all_frames = tuple(get_frames(self._video))	# list > tuple for mutability to slice last element
		# print(len(self._all_frames))

	def epilepsy(
			self, 
			is_gif: Optional[bool] = False, 
			dramatic_pixel_change: Optional[int] = 200,
			danger_trigger_requirement: Optional[int] = 8
		) -> bool:
		"""detect hard flashing lights"""
		
		cut_frames = self._all_frames if is_gif else (
			self._all_frames # if the video is short, just take everything
			[FRAME_SKIP_START :: FRAME_COLLECTION_SKIP] 
			# take every x frame starting from s - getting everything is not usually useful
		)

		# group the frames of the _video into tuples with 100 frames each, stored in dictionary
		frames = (cv.cvtColor(frame, cv.COLOR_BGR2GRAY) for frame in cut_frames)
		triggers = 0

		# separate the images into 8 portions to increase precision...in theory
		portion_data: dict[int, list[int]] = {i: [] for i in range(NO_PORTIONS)}
		for frame in frames:
			frame_data = [
				frame[
					y_cor : y_cor + self._portion_height, # crop portion
					x_cor : x_cor + self._portion_width
				] 
				for y_cor, x_cor 
				in (
					(self._portion_height * i, self._portion_width * j)	# coordinates
					for i in range(VERT_PORTIONS)						# rows	
					for j in range(HORIZ_PORTIONS)						# columns
				) # these are where the croppings of the sections start
			]

			# if some data about the frames exists, perform analysis
			for portion in portion_data: 
				"""the keys of _portion_data is represented by range(portions)"""

				avg = np.mean(frame_data[portion])
				if any(
						abs(prev_avg - avg) > dramatic_pixel_change # compare with previous frame's average
						for prev_avg 
						in portion_data[portion]
					):
					
					triggers += 1 # if a massive change is found, report danger

					# reset data, otherwise next iterations will report same danger 
					for port in portion_data:
						portion_data[port] = []

					break # if a trigger was found, the other portions of the frame 
						  # shouldn't be checked to avoid double counting

				portion_data[portion].append(avg) # add on the new data that's been checked

				# limit storage collection to avoid exponentially worsening time complexity
				if len(portion_data[portion]) > PORTION_DATA_MAX_CAPACITY:
					portion_data[portion].pop()

		# print(triggers)
		return triggers >= danger_trigger_requirement


if __name__ == '__main__':
	x=Detector(TEST_VIDEO)
	print(x._vid_width, x._vid_height)

	v=x.epilepsy()
	print(v)
