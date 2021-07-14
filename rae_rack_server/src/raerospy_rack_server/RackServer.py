#! /usr/bin/env python3

import rospy

import actionlib
from raepy import Servo, Rack
import time

from rae_rack_messages.msg import RackAction, HomeAction
import rae_rack_messages.msg

servo = Servo()
rack = Rack() 

class RackServer(object):
    def __init__(self):
        self._move_action_name = "~Move"
        self._home_action_name = "~Home"
        self._feedback = rae_rack_messages.msg.RackActionFeedback().feedback
        self._home_feedback = rae_rack_messages.msg.HomeActionFeedback().feedback
        self._result = rae_rack_messages.msg.RackActionResult().result
        self._move_action = actionlib.SimpleActionServer(self._move_action_name, RackAction, execute_cb=self.handle_rack_move_request, auto_start=False)
        self._home_action = actionlib.SimpleActionServer(self._home_action_name, HomeAction, execute_cb=self.handle_rack_home_request, auto_start=False)
        self._move_action.start()
        self._home_action.start()
        
        self._goal_position = None
        self._total_distance = None
        rospy.loginfo("%s: initialized" % self._move_action_name)
    
    def handle_rack_move_request(self,goal):
        self._goal_position = goal.position
        
        rospy.loginfo("%s: launched, goal position is %f" , self._move_action_name, self._goal_position)
        rack.to(self._goal_position, current=goal.current, cb=self._move_feedback_cb)
        self._result.done = True
        self._move_action.set_succeeded(self._result)

        rospy.loginfo('%s: Succeeded' % self._move_action_name)

    def handle_rack_home_request(self,goal):
        rospy.loginfo("%s: Homing launched" % self._home_action_name)

        servo.led_to("cyan")
        servo.jog(-50)

        done = rack.home(self._home_feedback_cb)

        if done:
            self._result.done = True
            rospy.loginfo('%s: Succeeded' % self._home_action_name)
            self._move_action.set_succeeded(self._result)
            servo.led_to("green")
            time.sleep(1)
            servo.led_to("black")
    
    def _move_feedback_cb(self, initial_angle, goal_angle, actual_angle):
        # preempting routine
        if self._move_action.is_preempt_requested():
            rospy.loginfo('%s: Preempted' % self._move_action_name)
            self._move_action.set_preempted()
            return False

        self._feedback.percentage = self._calculate_percentage(initial_angle, goal_angle, actual_angle)
        self._move_action.publish_feedback(self._feedback)
        rospy.loginfo('%s: Executing, Rack Move to Position %f is at %i ' , self._move_action_name, self._goal_position, self._feedback.percentage )
        return True

    def _home_feedback_cb(self,actual_angle,actual_current):
        # Publish position as feedback
        rospy.loginfo("%s : Actual Current: %i, Actual Position: %i", self._home_action_name, actual_current, actual_angle)
        self._home_feedback.position = actual_angle
        self._home_action.publish_feedback(self._home_feedback)

    def _calculate_percentage(self,initial, goal, actual):
        return int((1-(abs(goal - actual)/abs(initial-goal))) * 100)+1