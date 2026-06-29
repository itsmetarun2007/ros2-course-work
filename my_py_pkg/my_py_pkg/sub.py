#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class mysub(Node):
    def __init__(self):
        super().__init__("subnode")
        self.subscriber_=self.create_subscription(String,"chat", self.callback_message,20)
        self.get_logger().info("sub is started")
    
    def callback_message(self, msg: String):
        self.get_logger().info("sub recived "+msg.data)






def main(args=None):
    rclpy.init(args=args)
    node = mysub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()