#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle,GoalStatus
from my_robot_interface.action import RobotMovement


class MOVEROBOTCLIENTNODE(Node):                
    def __init__(self):
        super().__init__("Robot_move_client")
        self.robot_move_client_=ActionClient(self,RobotMovement,
                                             "robot_move")
        
        self.get_logger().info("client server is started")

    def send_goal(self,position,velocity):
        self.robot_move_client_.wait_for_server()

        goal=RobotMovement.Goal()
        goal.position=position
        goal.velocity=velocity

        self.get_logger().info("sending goal position: "+str(position)+" velocity: "+str(velocity))

        self.robot_move_client_.\
            send_goal_async(goal,feedback_callback = self.goal_feedback).\
            add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self,future):
        goal_handel:ClientGoalHandle =future.result()
        if goal_handel.accepted:
            self.get_logger().info("goal accepted")
            goal_handel.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().info("goal rejected")

    def goal_result_callback(self,future):
        status=future.result().status
        result =future.result().result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("goal Succeeded")        
        elif status== GoalStatus.STATUS_ABORTED:
            self.get_logger().error("goal Aborted")    
        elif status== GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        
        self.get_logger().info("position " +str(result.position))
        self.get_logger().info("message " +str(result.message))

    def goal_feedback(self,feedback_msg):
        position =feedback_msg.feedback.current_position
        self.get_logger().info("feedback position "+ str(position))

def main(args=None):
    rclpy.init(args=args)
    node = MOVEROBOTCLIENTNODE()
    node.send_goal(100,6)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__== "__main__":
    main()
