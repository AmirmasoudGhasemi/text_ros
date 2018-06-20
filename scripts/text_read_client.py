#!/usr/bin/env python

import sys
import rospy
from sensor_msgs.msg import Image
from text_ros.srv import TextRead



def callback(data):
    rospy.wait_for_service('text_read')
    try:
	text_read = rospy.ServiceProxy('text_read', TextRead)
	resp = text_read(data)
	return resp.text
    except rospy.ServiceException, e:
	print "Service call failed: %s"%e



def text_read_client():
    rospy.init_node('text_read_client', anonymous=True)

    rospy.Subscriber('/camera/rgb/image_color', Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()    

if __name__ == "__main__":
    text_read_client() 
