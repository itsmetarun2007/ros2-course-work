#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Mypub(Node):
    def __init__(self):
        super().__init__("pubnode")

        self.publisher_ = self.create_publisher(String, "chat", 20)
        self.counter_ = 0
        self.timer_ = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = "hi from tarun " + str(self.counter_)
        self.get_logger().info(msg.data)
        self.publisher_.publish(msg)
        self.counter_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = Mypub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()