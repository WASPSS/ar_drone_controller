#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import numpy as np
drift_y = 40
drift_angle = 0.2
kp_y = 0.00001
kp_angle = -0.28

def callback(data):
    twist = Twist()
    if abs(data.linear.y) > drift_y and abs(data.angular.z) < drift_angle:
        twist.angular.z = -0.14*np.sign(data.angular.z)#kp_angle*data.angular.z
        twist.linear.y = 0.03*np.sign(data.linear.y)#kp_y*data.linear.ydata.angular.z
    if abs(data.angular.z) > drift_angle:
        twist.angular.z = -0.14*np.sign(data.angular.z)#kp_angle*data.angular.z
    pub.publish(twist)

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global pub
    rospy.init_node('Joy2Turtle')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("/control/line_err", Twist, callback)
    # starts the node

    rospy.spin()

if __name__ == '__main__':
    start()
