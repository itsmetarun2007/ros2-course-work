#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interface.msg import HardwareStart


class HardwareStatusPublisherNode(Node):
    def __init__(self):
        super().__init__("HardwareStatusPublisher")

        self.publisher_ = self.create_publisher(HardwareStart, "hardware_status_pub", 20)
        self.timer_=self.create_timer(2.0,self.timer_callback)
        

    def timer_callback(self):
        msg = HardwareStart()
        msg.temperature = 35.7
        msg.are_motors_ready=True 
        msg.debug_msg="everthing is ok"
        self.publisher_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()