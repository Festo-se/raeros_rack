#! /usr/bin/env python3


from raerospy_rack_client.RackClient import RackClient
import time
import rospy

if __name__ == "__main__":
    rospy.init_node()
    print("Rack Example")
    rack = RackClient()
    print("Home")
    rack.home()
    time.sleep(1)
    rack.to(0.07)
    time.sleep(1)
    rack.to(0.02)
    time.sleep(1)
    rack.to(0.05)