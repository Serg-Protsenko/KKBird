import cv2
import os
# import urllib.request
# import numpy as np
from django.conf import settings


# load our serialized bird detector model from disk
bird_detection_webcam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR, 'opencv_haarcascade_data/bird_cascade.xml'))

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # 1 - for USB webcam on the laptop
		if not self.video.isOpened():
			self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 - for integrated laptop's webcam

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = bird_detection_webcam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image, 1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()
