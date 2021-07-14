import rae_rack_messages.msg

import rospy
import actionlib


class RackClient(object):
    def __init__(self):
        #rospy.init_node('rack_client_py')
        self.__rack_home_client = actionlib.SimpleActionClient('/rae_rack_server/Home', rae_rack_messages.msg.HomeAction)
        self.__rack_home_client.wait_for_server()
        self.__rack_move_client = actionlib.SimpleActionClient('/rae_rack_server/Move', rae_rack_messages.msg.RackAction)
        self.__rack_move_client.wait_for_server()


    def home(self):
        goal = rae_rack_messages.msg.HomeGoal()
        self.__rack_home_client.send_goal(goal)
        self.__rack_home_client.wait_for_result()
        return self.__rack_home_client.get_result()

    def to(self,position, current=800):
        goal = rae_rack_messages.msg.RackGoal(position=position,current=current)
        self.__rack_move_client.send_goal(goal)
        self.__rack_move_client.wait_for_result()
        return self.__rack_move_client.get_result()
    
