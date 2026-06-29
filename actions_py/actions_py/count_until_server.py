#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import threading
from rclpy.action import ActionServer, GoalResponse,CancelResponse
from rclpy.action.server import ServerGoalHandle
from my_robot_interface.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class COUNTUNTILNODE(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.goal_handel_= None
        self.goal_lock_= threading.Lock()
        self.count_until_server_ = ActionServer(self,CountUntil,"count_until",
                                                goal_callback=self.goal_callback,
                                                cancel_callback=self.cancel_callback,
                                                execute_callback=self.execute_callback,
                                                callback_group=ReentrantCallbackGroup())
        
        self.get_logger().info("Action server of Count_until is started")

    def goal_callback(self, goal_request:CountUntil.Goal):

        # goal policy to refuse new request
        with self.goal_lock_:
            if ((self.goal_handel_ is not None) and (self.goal_handel_.is_active)):
                self.get_logger().info("there is an exesting goal....rejecting a new goal")
                return GoalResponse.REJECT


        self.get_logger().info("Recived a goal ")
        
        if goal_request.target_number <= 0:
            self.get_logger().info("Rejecting a goal")
            return GoalResponse.REJECT

        else:
            self.get_logger().info("accepting a goal")
            return GoalResponse.ACCEPT
        


    def cancel_callback(self, goal_handel: ServerGoalHandle):

        self.get_logger().info("Recived a cancel request")
        return CancelResponse.ACCEPT #REJECT
 

    def execute_callback(self,goal_handel: ServerGoalHandle):
        with self.goal_lock_:
            self.goal_handel_ = goal_handel

        #request from goal

        target=goal_handel.request.target_number
        period=goal_handel.request.period

        #execute action
        self.get_logger().info("executing the goal ")

        feedback = CountUntil.Feedback()
        result = CountUntil.Result()
        counter=0
        for i in range(target):
            if goal_handel.is_cancel_requested:
                self.get_logger().info("canceling the goal")
                goal_handel.canceled()
                result.reached_number = counter
                return result
                
            counter +=1
            self.get_logger().info(str(counter))
            feedback.current_number = counter
            goal_handel.publish_feedback(feedback)
            time.sleep(period)  

        #once done succed/abort
        goal_handel.succeed()

        # send the result
        result = CountUntil.Result()
        result.reached_number = counter
        return result   
   



def main(args=None):
    rclpy.init(args=args)
    node = COUNTUNTILNODE()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()

if __name__== "__main__":
    main()
