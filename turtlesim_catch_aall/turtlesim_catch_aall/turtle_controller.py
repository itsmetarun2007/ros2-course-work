import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from functools import partial
from my_robot_interface.msg import Turtle
from my_robot_interface.msg import TurtleArray
from my_robot_interface.srv import CatchTurtle


class TurtleControllerNode(Node):
    def __init__(self):
        
        super().__init__('turtle_controller')
        self.pose: Pose = None
        self.turtle_to_catch_:Turtle = None
        self.declare_parameter("catch_closest_turtle_first", True)
        self.catch_closest_turtle_first_ = self.get_parameter("catch_closest_turtle_first").value
        self.pose_subscriber_=self.create_subscription(Pose,"/turtle1/pose",self.callback_pose,10)
        self.cmd_vel_publisher_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.get_logger().info('Turtle Controller Node has been started!')
        self.alive_turtles_subscriber_=self.create_subscription(TurtleArray,
                            "alive_turtles",self.callback_alive_turtles,10)
        self.catch_turtle_client_=self.create_client(CatchTurtle,"catch_turtle")
        self.control_loop_timer=self.create_timer(0.01,self.control_loop)

    def callback_pose(self,pose:Pose): 
        self.pose = pose

    def callback_alive_turtles(self, msg: TurtleArray):
        if len(msg.turtles) > 0:
            if self.catch_closest_turtle_first_:
                closest_turtle = None
                closest_turtle_distance = None 

                for turtle in msg.turtles:
                    dist_x = turtle.x - self.pose.x
                    dist_y = turtle.y - self.pose.y
                    distance =math.sqrt(dist_x*dist_x+dist_y*dist_y)
                    if closest_turtle == None or distance < closest_turtle_distance:
                        closest_turtle_distance = distance
                        closest_turtle = turtle

                self.turtle_to_catch_ = closest_turtle

            else:
                self.turtle_to_catch_ = msg.turtles[0]

    def control_loop(self):
        if self.pose == None or self.turtle_to_catch_== None:
            return
        
        dist_x= self.turtle_to_catch_.x - self.pose.x
        dist_y= self.turtle_to_catch_.y - self.pose.y
        distance =math.sqrt(dist_x*dist_x+dist_y*dist_y)

        cmd=Twist()

        if distance > 0.5:
            cmd.linear.x=float(2*distance)

            goal_theta= math.atan2(dist_y,dist_x)
            diff =goal_theta-self.pose.theta
            if diff >math.pi:
                diff-=2*math.pi
            elif diff < -math.pi:
                diff+=2*math.pi
            cmd.angular.z=float(6*diff)

            
        else:
            cmd.linear.x=0.0
            cmd.angular.z=0.0
            self.call_catch_service(self.turtle_to_catch_.name)
            self.turtle_to_catch_ = None

        self.cmd_vel_publisher_.publish(cmd)
    
    def call_catch_service(self,turtle_name):
        while not self.catch_turtle_client_.wait_for_service(1.0):
            self.get_logger().warn("clint is waiting for catch server......")

        request=CatchTurtle.Request()
        request.name = turtle_name

        future = self.catch_turtle_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle_service,turtle_name=turtle_name))

    def callback_call_catch_turtle_service(self,future, turtle_name):
        response: CatchTurtle.Response = future.result()
        if not response.success:
            self.get_logger().error("Turtle " + str(turtle_name) + " could not removed")
        

def main(args=None):
   
    rclpy.init(args=args)
    
    
    my_node = TurtleControllerNode()

    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
