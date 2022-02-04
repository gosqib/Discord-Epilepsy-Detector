import cv2 as cv #type: ignore
import numpy as np

from testing import *
from consts import *
from toolbox import *

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

	def epilepsy(self) -> bool:
		"""detect hard flashing lights"""
		
		if len(self._all_frames) < GIF_DETERMINER_MINFRAME:
			# this section is just some adjustments for gifs since they're different from .mp4
			
			DANGER_TRIGGER_REQUIREMENT = 1	# also lower the trigger quantity requirements
			DRAMATIC_PIXEL_CHANGE = 180
			cut_frames = self._all_frames 	# if the video is short, just take everything
		else:
			DANGER_TRIGGER_REQUIREMENT = 7
			DRAMATIC_PIXEL_CHANGE = 200
			cut_frames = (
				self._all_frames
				[FRAME_SKIP_START :: FRAME_COLLECTION_SKIP] 
				# take every x frame starting from s - getting everything is not usually useful
			)

		# group the frames of the _video into tuples with 100 frames each, stored in dictionary
		frames = (cv.cvtColor(frame, cv.COLOR_BGR2GRAY) for frame in cut_frames)
		triggers = 0

		# next two bunches of code are to separate the images into 8 portions
		# this is done to increase precision...in theory
		portion_dims = tuple(
			(self._portion_height * i, self._portion_width * j) # coordinates
			for i in range(VERT_PORTIONS)                       # rows
			for j in range(HORIZ_PORTIONS)                      # columns
		) # represented by a tuple of {portion_number} elements that point toward 
		  # future cropping locations

		portion_data: dict[int, list[int]] = {i: [] for i in range(NO_PORTIONS)}
		for frame in frames:
			frame_data = [
				frame[
					y_cor : y_cor + self._portion_height, # crop portion
					x_cor : x_cor + self._portion_width
				] 
				for y_cor, x_cor 
				in portion_dims 
			]

			# if some data about the frames exists, perform analysis
			for portion in portion_data: 
				"""the keys of _portion_data is represented by range(portions)"""

				avg = np.mean(frame_data[portion])
				if any(
						abs(prev_avg - avg) > DRAMATIC_PIXEL_CHANGE # compare with previous frame's average
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
		return triggers >= DANGER_TRIGGER_REQUIREMENT


if __name__ == '__main__':
	x=Detector(TEST_VIDEO)
	print(x._vid_width, x._vid_height)

	v=x.epilepsy()
	print(v)