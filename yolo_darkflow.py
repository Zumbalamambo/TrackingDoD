import numpy as np
import cv2
import os,sys,time
import argparse
import glob
from matplotlib import pyplot as plt
from darkflow.net.build import TFNet

parser   = argparse.ArgumentParser()

"""
In getYoloDetector funsction:
You must set darkflowPath variable to the directory
where darkflow is installed
"""

def getYoloDetector(threshold = 0.6):
	# darkflowPath = "/home/basem/ws/git/darkflow-master/"
	darkflowPath = "./darkflow-master/"
	options = {"model": darkflowPath+"cfg/yolo.cfg", 
	    	  	 "load":  darkflowPath+"yolo.weights", 
			   		 "threshold": threshold,
			   		 "gpu": 0.75,
			   		 "config": darkflowPath+"cfg/"}
	tfnet = TFNet(options)

	return tfnet


def parseDetection(detection):
	boxTl = (detection['topleft']['x'], detection['topleft']['y'])
	boxBr = (detection['bottomright']['x'],detection['bottomright']['y'])
	label = detection['label']
	confidence = detection['confidence']
	box = [boxTl,boxBr]

	return box, confidence, label


def drawBoxes(detections, frame,selectedClasses):

	for detection in detections:
		boxTl = (detection['topleft']['x'], detection['topleft']['y'])
		boxBr = (detection['bottomright']['x'],detection['bottomright']['y'])
		label = detection['label']
		confidence = int( detection['confidence']*100 )
		txtBoxW = 20
		txtBoxL = 150
		if not(label in selectedClasses):
			continue
		cv2.rectangle(frame, (boxTl[0],boxTl[1]-txtBoxW),(boxTl[0]+txtBoxL,boxTl[1]) , (0, 255, 0), -1)
		cv2.rectangle(frame, (boxTl[0],boxTl[1]-txtBoxW),(boxTl[0]+txtBoxL,boxTl[1]) , (0, 255, 0), 6)
		cv2.rectangle(frame, boxTl, boxBr, (0, 255, 0), 6)
		midPoint = (int((boxTl[0]+boxBr[0])/2),int((boxTl[1]+boxBr[1])/2))
		cv2.rectangle(frame, midPoint, midPoint, (0, 0, 0), 12)

		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,label + "  " + str(confidence),(boxTl[0],boxTl[1]), 
							 font, 0.8,(0,0,0),2,cv2.LINE_AA)

	return frame