#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle , GoalStatus
from my_robot_interface.action import CountUntil


class COUNTUNTILNODECLIENT(Node):
    def __init__(self):
        super().__init__("count_until_client")
        self.declare_parameter("target_",10)
        self.declare_parameter("period_",1.0)
        
        self.target = self.get_parameter("target_").value
        self.period = self.get_parameter("period_").value
        self.count_until_client_ = ActionClient(self,CountUntil,"count_until")
        self.get_logger().info("Action Client of Count_until is started")

    def send_goal(self,target ,period):
        self.count_until_client_.wait_for_server()

        goal=CountUntil.Goal()
        goal.target_number = target
        goal.period = period

        self.get_logger().info("sending Goal")
        self.count_until_client_.send_goal_async(goal,feedback_callback = self.goal_feedback_callback).add_done_callback(self.goal_response)

        #self.timer_=self.create_timer(2.0,self.cancel_goal)
    def cancel_goal(self):
        self.get_logger().info("sending a cancel request")
        self.goal_handel_.cancel_goal_async()
        self.timer_.cancel()
        
    def goal_response(self, future):

        self.goal_handel_: ClientGoalHandle = future.result()     
        if self.goal_handel_.accepted:
            self.get_logger().info("Accepted the goal ")

            self.goal_handel_.get_result_async().add_done_callback(self.result_response)
        else:
            self.get_logger().warn("goal is Rejected")
    
    def result_response(self,future):
        status =future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("sucess")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info("Canceled")

        self.get_logger().info("result = " + str(result.reached_number))

    def goal_feedback_callback(self, feedback_msg):
        number = feedback_msg.feedback.current_number
        self.get_logger().info("current num is "+ str(number))

def main(args=None):
    rclpy.init(args=args)
    node = COUNTUNTILNODECLIENT()
    node.send_goal(node.target,node.period)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__== "__main__":
    main()





        
'''
    def cancel_active_goal(self):
        """Method triggered by manual terminal input."""
        if self.goal_handle_ is not None:
            self.get_logger().info("Manual cancellation triggered! Sending cancel request...")
            self.goal_handle_.cancel_goal_async()
        else:
            self.get_logger().warn("No active goal handle found to cancel.")


def main(args=None):
    rclpy.init(args=args)
    node = COUNTUNTILNODECLIENT()
    node.send_goal(node.target, node.period)

    # CRITICAL: Spin ROS 2 in a background thread so it doesn't freeze
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    try:
        # The main thread blocks here waiting for YOUR manual terminal input
        input() 
        node.cancel_active_goal()
        
        # Keep main thread alive briefly to let the cancel callbacks complete
        ros_thread.join(timeout=2.0)
        
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()

'''
