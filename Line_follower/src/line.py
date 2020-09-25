#!/usr/bin/env python

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from math import *

class Follower:

	def __init__(self):
		self.i=0
		self.bridge = cv_bridge.CvBridge()
		self.image_sub = rospy.Subscriber('/camera1/camera/rgb/image_raw/compressed',CompressedImage, self.image_callback,queue_size=1)
		#motion publisher
		self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
		self.twist = Twist()

	def image_callback(self, msg):
        
		image = self.bridge.compressed_imgmsg_to_cv2(msg)
		cv2.imwrite('image.png',image)		
		#Choose your color and translate it into HSV data
		lower_yellow = numpy.array([-10, -10, 183])
		upper_yellow= numpy.array([ 10,  10, 263])
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		kernel=numpy.ones((5,5),numpy.uint8)				
		mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
		h, w, d = image.shape
		search_top = h/4
		search_bot = 3*h/4 + 150
		numpy.floor(search_top)
		numpy.floor(search_bot)
		image[0:int(search_top), 0:w] = 0
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
		kernel=numpy.ones((5,5),numpy.uint8)
		dilation=cv2.dilate(mask,kernel,iterations=2)
		p=w/2	
		M = cv2.moments(dilation)
		if M['m00'] > 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			err = cx-p
			self.twist.linear.x = 0.015	  
			self.twist.angular.z= - float(err) / 100
		else: 
			print('no line detected')		
		self.cmd_vel_pub.publish(self.twist)

rospy.init_node('line_follower')
follower = Follower()
rospy.Rate(20)
rospy.spin()
