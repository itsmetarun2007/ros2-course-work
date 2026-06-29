#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

class Addtwoints_client(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        self.client_ = self.create_client(AddTwoInts,"add_two_ints")
        self.get_logger().info("client is active")

    def call_add_two_ints(self,a,b):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for add_two_ints server")

        request=AddTwoInts.Request()
        request.a=a
        request.b=b

        future=self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_call,request=request))

    def callback_call(self,future,request):
        response= future.result()
        self.get_logger().info(str(request.a)+ "+" + str(request.b) + "=" + str(response.sum))


def main(args=None):
    rclpy.init(args=args)
    node=Addtwoints_client()
    for i in range(10):
        node.call_add_two_ints(i,10)
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

