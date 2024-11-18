#!/usr/bin/env python3

import rospy
from gazebo_ros_link_attacher.srv import Attach, AttachRequest, AttachResponse
from std_msgs.msg import Bool

object_received = False

def object_received_callback(msg):
    global object_received 
    object_received  = msg.data
    rospy.loginfo("Recebido sinal do objeto: " + str(object_received ))


if __name__ == '__main__':
    
    rospy.Subscriber('/object_received', Bool, object_received_callback)

    rospy.init_node('demo_attach_links')
    rospy.loginfo("Creating ServiceProxy to /link_attacher_node/attach")
    attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',
                                    Attach)
    attach_srv.wait_for_service()
    rospy.loginfo("Created ServiceProxy to /link_attacher_node/attach")

    rospy.loginfo("Esperando sinal do objeto")
    while not object_received:
        rospy.sleep(0.1)
	
    # Link them
    rospy.loginfo("Attaching turtlebot3_waffle_pi and cube2")
    req = AttachRequest()
    req.model_name_1 = "turtlebot3_waffle_pi"
    req.link_name_1 = "base_footprint"
    req.model_name_2 = "object"
    req.link_name_2 = "link_0"
    
    
    attach_srv.call(req)


'''rosservice call /link_attacher_node/attach "{model_name_1: 'turtlebot3_waffle_pi', 
link_name_1: 'base_footprint', 
model_name_2: 'object', 
link_name_2: 'link_0'}"
'''


