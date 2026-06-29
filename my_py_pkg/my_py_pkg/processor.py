#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class processor(Node):
    def __init__(self):
        super().__init__("processor")
        self.subscriber_=self.create_subscription(Int64,"sen2pro",self.attender,10)
        self.publisher_=self.create_publisher(Int64,"protoout",10)
        self.get_logger().info("processor started")
        
    def attender(self, msg: Int64 ):
        new_msg=Int64()
        new_msg.data=msg.data+1
        self.publisher_.publish(new_msg)
        self.get_logger().info("processor sending " + str(new_msg.data))
def main(args=None):
    rclpy.init(args=args)
    node = processor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=="__main__":
    main()




