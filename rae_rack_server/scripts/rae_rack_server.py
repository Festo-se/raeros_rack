#! /usr/bin/env python3

import rospy

from raerospy_rack_server.RackServer import RackServer

if __name__ == "__main__":
    rospy.init_node('rae_rack_server')
    RackServer()
    rospy.spin()