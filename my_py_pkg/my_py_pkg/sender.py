#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class sender(Node):
    def __init__(self):
        super().__init__("sendernode")

        self.publisher_= self.create_publisher(Int64,"sen2pro",10)
        self.counter=0
        self.timer_=self.create_timer(2.0,self.callback)
    
    def callback(self):
        msg=Int64()
        msg.data=self.counter
        self.get_logger().info("sending "+str(self.counter))
        self.publisher_.publish(msg)
        self.counter+=2


def main(args=None):
    rclpy.init(args=args)
    node=sender()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()
