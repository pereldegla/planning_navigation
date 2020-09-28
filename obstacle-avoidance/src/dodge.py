#! /usr/bin/env python
#this program was written for a class project regarding the obstacle avoidance issue.
import rospy

from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist



#================================================#




def clbk_laser(msg):
    #we define the method that receives the laser readings through the subscriber
    regions = {
        'front': min(min(msg.ranges[0:22]),min(msg.ranges[338:360]),3.5),
        'fright': min(min(msg.ranges[23:49]), 3.5), 
        'right': min(min(msg.ranges[50:90]), 3.5), #right and left are useless in this case but could be useful for future projects       
        'fleft': min(min(msg.ranges[311:337]), 3.5), 
        'left': min(min(msg.ranges[270:310]), 3.5),
    }

    take_action(regions)
  

def take_action(regions):
    #motion init
    msg = Twist()
    linear_x = 0
    angular_z = 0
    dist=0.4 #security distance
    state_description = ''

    if regions['front'] > dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_description = 'case 1 - nothing'
        linear_x = 0.4
        angular_z = 0
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = -0.6
    elif regions['front'] > dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = -0.6
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = 0.6
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = -0.6
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = 0.6
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = -0.6
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0
        angular_z = -0.6
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)
        

rospy.init_node('dodge')
sub=rospy.Subscriber('/scan', LaserScan, clbk_laser)
pub= rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.spin()


