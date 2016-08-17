#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import numpy as np
import cv2
from sensor_msgs.msg import Joy
import time

enable =1
error = Twist()
twist = Twist()
drift_y = 40
drift_angle = 0.2

kp_y = 0.7
kp_angle = 1

ki_y = 0.01
ki_angle = 0.001

d_time = 0.1
integral_y =0
integral_angle=0

def nothing(x):
    pass

print 'Create trackbars'

cv2.namedWindow('P_I_Control')


cv2.createTrackbar('kp_y','P_I_Control',1,200,nothing)
cv2.createTrackbar('kp_angle','P_I_Control',1,200,nothing)
cv2.createTrackbar('ki_y','P_I_Control',-5,50,nothing)
cv2.createTrackbar('ki_angle','P_I_Control',-5,50,nothing)
print 'Trackbars created'

def callback(data):
	#print 'callback_executed'
	global error
	error = data

def joy_callback(data):
	global enable
	enable = data.buttons[5] 

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
	print 'Start Func exec'
	global pub
	rospy.init_node('line_controller_to_drone')
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	# subscribed to joystick inputs on topic "joy"
	rospy.Subscriber("/control/line_err", Twist, callback)
	rospy.Subscriber("/joy", Joy, joy_callback)
	rate = rospy.Rate(1/d_time)
	# starts the node
	while not rospy.is_shutdown():
		if enable==1:

			#'''
			#print 'Track_Bar_Updated'
			global kp_y
			global kp_angle
			global ki_y
			global ki_angle
			cv2.waitKey(1)
			kp_y = ((0.14/320)*cv2.getTrackbarPos('kp_y','P_I_Control'))/float(200)
			kp_angle = ((0.28/1.2)*cv2.getTrackbarPos('kp_angle','P_I_Control'))/float(200)
			ki_y = ((0.14/320)*cv2.getTrackbarPos('ki_y','P_I_Control'))/float(1000)
			ki_angle = ((0.28/1.2)*cv2.getTrackbarPos('ki_angle','P_I_Control'))/float(1000)
			#'''
			#print 'while loop'

			#print 'omg', kp_angle, kp_y, ki_angle,ki_y

			twist = Twist()
			global integral_y
			global integral_angle
			integral_y = integral_y + error.linear.y*d_time
			integral_angle = integral_angle + error.angular.z*d_time

			if abs(error.linear.y) > drift_y and abs(error.angular.z) < drift_angle:

				twist.angular.z = (0.28/1.2)*(kp_angle*error.angular.z + ki_angle*integral_angle)
				if twist.angular.z > 0.28:
					twist.angular.z = 0.28

				twist.linear.y = (0.14/320)*(kp_y*error.linear.y  + ki_y*integral_y)
				if twist.linear.y > 0.14:
					twist.linear.y = 0.14
		        '''
		        twist.angular.z = -0.14*np.sign(error.angular.z)#kp_angle*error.angular.z
		        twist.linear.y = 0.03*np.sign(error.linear.y)#kp_y*error.linear.y
		        '''
			if abs(error.angular.z) > drift_angle:
				twist.angular.z = (0.28/1.2)*(kp_angle*error.angular.z + ki_angle*integral_angle)
				if twist.angular.z > 0.28:
					twist.angular.z = 0.28

			pub.publish(twist)

		rate.sleep()

	rospy.spin()

if __name__ == '__main__':
	start()
