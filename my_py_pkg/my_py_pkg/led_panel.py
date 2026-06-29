import rclpy
from rclpy.node import Node
from my_robot_interface.msg import LedStatusArray
from my_robot_interface.srv import SetLed

class LedPanel(Node):
    def __init__(self):
        super().__init__('led_panel')
        self.led_states_=[0,0,0]
        self.led_publisher =self.create_publisher(LedStatusArray,"Led_panel_topic",20)
        self.led_service =self.create_service(SetLed,"led_panel_server",self.led_server_callback)
        self.timer_=self.create_timer(1.0,self.led_callback)    
        self.get_logger().info("LED panel node has been started")

    def led_callback(self):
        msg=LedStatusArray()
        msg.led_state = self.led_states_
        self.led_publisher.publish(msg)

    def led_server_callback(self, request: SetLed.Request, response: SetLed.Response):
        led_number=request.led_number
        state=request.state

        if led_number >= len(self.led_states_) or led_number < 0 :
            response.success=False
            return response
    
        if state not in [0, 1]:
            response.success=False
            return response
    
        self.led_states_[led_number]=state
        self.led_callback()
        response.success=True
        return response

    




def main(args=None):
    rclpy.init(args=args)
    node = LedPanel()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()