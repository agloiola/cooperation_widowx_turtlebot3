#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Bool
from actionlib_msgs.msg import GoalStatus

object_received = False

def object_received_callback(msg):
    global object_received 
    object_received  = msg.data
    rospy.loginfo("Recebido sinal do objeto: " + str(object_received ))


def movebase_client():
    
    rospy.init_node('movebase_client')
    
    rospy.Subscriber('/object_received', Bool, object_received_callback)

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    goal.target_pose.pose.position.x = 0.5
    goal.target_pose.pose.position.y = 0.3
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)  
    client.wait_for_result()
    
    pub = rospy.Publisher('/robot_arrival', Bool, queue_size=10)
    rospy.sleep(1)
    
    if client.get_state() == GoalStatus.SUCCEEDED:
        rospy.loginfo("Robô moveu para a posição desejada")
        pub.publish(True)  # Publica o sinal de chegada
        rospy.loginfo("Sinal de chegada publicado!")
    else:
        rospy.loginfo("Erro")
        pub.publish(False)  # Publica um sinal de erro, caso necessário
  
    rospy.loginfo("Esperando o objeto ser posicionado")
    
    while not object_received:
        rospy.sleep(0.1)
	
    rospy.sleep(2)
    goal.target_pose.pose.position.x = 4.0
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)  
    client.wait_for_result()
    
    if client.get_state() == GoalStatus.SUCCEEDED:
        rospy.loginfo("Robô carregou o objeto")
    else:
        rospy.loginfo("Erro ao carregar o objeto")
        
    
	
if __name__ == "__main__":
    movebase_client()

