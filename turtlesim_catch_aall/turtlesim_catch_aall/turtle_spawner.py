#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial
import random
import math
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from my_robot_interface.msg import Turtle
from my_robot_interface.msg import TurtleArray
from my_robot_interface.srv import CatchTurtle


class Turtle_spawner(Node):
    def __init__(self):
        super().__init__("turtle_spawn")
        self.declare_parameter("turtle_prefix_name", "turtle")
        self.declare_parameter("spawn_frequency", 1.0)
        self.turtle_name_prefix_= self.get_parameter("turtle_prefix_name").value
        self.spawn_frequency_=self.get_parameter("spawn_frequency").value
        
        self.turtle_counter_ = 0
        self.alive_turtules_ = []
        self.alive_turtle_publisher_=self.create_publisher(TurtleArray,"alive_turtles", 10)
        self.spawn_client_=self.create_client(Spawn,"/spawn")
        self.kill_client_= self.create_client(Kill,"/kill")
        self.catch_turtle_service_= self.create_service(CatchTurtle,"catch_turtle",self.callback_catch_turtle)
        self.spawner_timer_ = self.create_timer(2.0/self.spawn_frequency_ ,self.spawn_new_turtle)

    def callback_catch_turtle(self, request: CatchTurtle.Request, response: CatchTurtle.Response):
        self.callback_kill_service(request.name)
        response.success= True
        return response

    def publish_alive_tutrles(self):
        msg=TurtleArray()
        msg.turtles=self.alive_turtules_
        self.alive_turtle_publisher_.publish(msg)

    def spawn_new_turtle(self):
        self.turtle_counter_+= 1
        name = self.turtle_name_prefix_ + str(self.turtle_counter_)
        x =random.uniform(0.0, 11.0)
        y =random.uniform(0.0, 11.0)
        theta =random.uniform(0.0, 2*math.pi)

        self.call_spawn_service(x, y, name, theta)

    def call_spawn_service(self, x:float, y:float, turtle_name:str, theta:float):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("clint is waiting for spawn server......")

        request=Spawn.Request()
        request.x=x
        request.y=y
        request.name=turtle_name
        request.theta=theta

        future=self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn_service,request=request))
    

    def callback_call_spawn_service(self,future,request:Spawn.Request):
        response: Spawn.Response = future.result()
        if response.name != "":
            self.get_logger().info("new alive turtle:"+ response.name)
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtules_.append(new_turtle)
            self.publish_alive_tutrles()
    
    def callback_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("clint is waiting for kill server......")

        request=Kill.Request()
        request.name=turtle_name

        future = self.kill_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_kill_service,turtle_name=turtle_name))

    def callback_call_kill_service(self, future, turtle_name):
        for (i, turtle) in enumerate(self.alive_turtules_):
            if turtle.name == turtle_name:
                del self.alive_turtules_[i]
                self.publish_alive_tutrles()
                break 
        

def main(args=None):
    rclpy.init(args=args)
    node = Turtle_spawner()
    node.call_spawn_service(5.0, 2.8, "tar", 8.5)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()