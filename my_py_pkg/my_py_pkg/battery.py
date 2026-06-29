#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interface.srv import SetLed

class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery")
        self.battery_state_="full"
        self.last_time_battery_state_changed=self.get_current_time_sec()
        self.timer_ = self.create_timer(1.0, self.check_battery_state)
        self.led_client_=self.create_client(SetLed,"led_panel_server")
        self.get_logger().info("battery node is started")
    

    def get_current_time_sec(self):
        sec, nanosec = self.get_clock().now().seconds_nanoseconds()
        return sec+nanosec /1000000000.0
    
    def check_battery_state(self):
        time_now=self.get_current_time_sec()
        if self.battery_state_=="full":
            if time_now-self.last_time_battery_state_changed > 4.0:
                self.battery_state_="empty"
                self.get_logger().info("the battery is empty!  charging....")
                self.call_set_led(2, 1)
                self.last_time_battery_state_changed=time_now
        
        elif self.battery_state_ == "empty":
            if time_now-self.last_time_battery_state_changed > 6.0:
                self.battery_state_="full"
                self.get_logger().info("battery is full ")
                self.call_set_led(2, 0)
                self.last_time_battery_state_changed=time_now

    def call_set_led(self, led_number, state):
        while not self.led_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for led panel server")

        request=SetLed.Request()
        request.led_number=led_number
        request.state=state

        future=self.led_client_.call_async(request)
        future.add_done_callback(self.callback_call)

    def callback_call(self,future):
        response: SetLed.Response = future.result()
        if response.success:
            self.get_logger().info("Led state changed")
        else:
            self.get_logger().info("Led not changed")
        

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()