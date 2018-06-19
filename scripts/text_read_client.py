#!/usr/bin/env python

import sys
import rospy
from sensor_msgs.msg import Image
from text_ros.srv import TextRead

def text_read_client(image):
    rospy.wait_for_service('text_read')
    while rospy_is_shutdown():
	    try:
		text_read = rospy.ServiceProxy('text_read', TextRead)
		Image() 
		resp1 = text_read(image)
		return resp1.text
	    except rospy.ServiceException, e:
		print "Service call failed: %s"%e


if __name__ == "__main__":
    if len(sys.argv) == 1:
        image = int(sys.argv[1])
    else:
        print usage()
        sys.exit(1)
    text_read_client(image) 
