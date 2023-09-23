#! /home/reallounger/anaconda3/bin/python3.8

import rospy
from random import uniform
from time import sleep
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class Move:
    def __init__(self):
        self.velocity = 0.1 # m/s
        self.moving_range = uniform(1, 1.5) # m
        self.target_position = self.moving_range / 2
        self.current_speed = Twist()
        self.current_speed.linear.x, self.current_speed.linear.y, self.current_speed.linear.z = 0, 0, 0
        self.current_speed.angular.x, self.current_speed.angular.y, self.current_speed.angular.z = 0, 0, 0

    def SingleMovement(self, speed):
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 20)
        self.current_speed.linear.x = speed
        pub.publish(self.current_speed)

    def Init(self):
        self.SingleMovement(self.velocity)

    def IsArrived(self, x):
        if self.target_position > 0:
            if x >= self.target_position:
                return True
        else:
            if x <= self.target_position:
                return True
        return False

    def ReciprocatingMotion(self, odometry_msg):
        current_position_x = odometry_msg.pose.pose.position.x
        if self.IsArrived(current_position_x):
            
            # 电机停转1ms
            self.SingleMovement(0)
            sleep(0.001)
            
            # 换向
            self.velocity *= -1
            self.SingleMovement(self.velocity)
            
            self.target_position *= -1

# 初始化
move = Move()
move.Init()

if __name__ == "__main__":
    rospy.init_node('reciprocating_motion_pub')
    
    rospy.Subscriber('/odom', Odometry, move.ReciprocatingMotion) # 第一个参数修改为里程计话题

    rospy.spin()
    


