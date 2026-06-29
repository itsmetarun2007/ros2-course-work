#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from my_robot_interface.action import RobotMovement

class MOVEROBOTSERVERNODE(Node):
    def __init__(self):
        super().__init__("Robot_move_server")
        self.robot_position_=50
        self.robot_move_server_=ActionServer(self,RobotMovement,
                                             "robot_move",
                                             execute_callback=self.execute_callback)
        
        self.get_logger().info("action server is started")
        self.get_logger().info("robot position: " +str(self.robot_position_) )

    def execute_callback(self,goal_handel:ServerGoalHandle):
        goal_position =goal_handel.request.position
        velocity=goal_handel.request.velocity

        result = RobotMovement.Result()
        feedback = RobotMovement.Feedback()

        self.get_logger().info("execute goal")
        while rclpy.ok():
            diff = goal_position-self.robot_position_
            
            if diff == 0:
                result.position = self.robot_position_
                result.message = "sucess"
                goal_handel.succeed()
                return result

            elif diff > 0:
                if diff >= velocity:
                    self.robot_position_ += velocity
                else:
                    self.robot_position_ += diff
            else:
                if abs(diff) >= velocity:
                     self.robot_position_ -= velocity
                else:
                    self.robot_position_ -= abs(diff)
            self.get_logger().info("robot position: " +str(self.robot_position_) )
            feedback.current_position = self.robot_position_
            goal_handel.publish_feedback(feedback)  

            time.sleep(1.0)



def main(args=None):
    rclpy.init(args=args)
    node =MOVEROBOTSERVERNODE()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()