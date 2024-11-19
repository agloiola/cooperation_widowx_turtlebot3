#!/usr/bin/env python3

import sys
import copy
from math import pi

import geometry_msgs.msg
import rospy
import moveit_commander
from geometry_msgs.msg import PoseStamped, Quaternion
from std_msgs.msg import Bool
import tf

# Variável para armazenar a chegada do robô móvel
robot_arrived = False

def robot_arrival_callback(msg):
    global robot_arrived
    robot_arrived = msg.data
    rospy.loginfo("Recebido sinal de chegada do robô móvel: " + str(robot_arrived))

def main():
    global robot_arrived
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)


    rospy.Subscriber('/robot_arrival', Bool, robot_arrival_callback)
    
    
    robot = moveit_commander.RobotCommander()

    scene = moveit_commander.PlanningSceneInterface()

    arm_group = moveit_commander.MoveGroupCommander("interbotix_arm", ns="/wx250s")
    hand_group = moveit_commander.MoveGroupCommander("interbotix_gripper", ns="/wx250s")

    arm_group.set_max_velocity_scaling_factor(0.5)
    arm_group.set_max_acceleration_scaling_factor(0.5)


    eef_link = arm_group.get_end_effector_link()
    touch_links = robot.get_link_names(group="interbotix_gripper")

    # Criando uma cena
    rospy.sleep(1)  
    scene_objects = create_scene(scene)
    rospy.loginfo('Cena Criada. Os objetos sao: ' + str(scene_objects))
    arm_group.set_support_surface_name('table1')
    rospy.sleep(1)
    
    # Aguarda o robô móvel chegar à posição desejada
    rospy.loginfo("Esperando o robô móvel chegar à posição")
    while not robot_arrived:
        rospy.sleep(0.1)

    rospy.loginfo("O robô móvel chegou.")
    rospy.loginfo("Movendo objeto para a posição de destino.")


    # coloca o braço na posição inicial
    arm_group.set_named_target("Upright")
    plan = arm_group.go(wait=True)
    rospy.sleep(1)
    if plan:
        rospy.loginfo("O BRAÇO ESTÁ NA POSIÇÃO INICIAL")
    else:
        rospy.loginfo("ERRO AO IR PARA A POSIÇÃO INICIAL")
        moveit_commander.roscpp_shutdown()
        sys.exit()


    # abre a garra
    hand_group.set_named_target("Open")
    plan = hand_group.go(wait=True)
    rospy.sleep(1)

    if plan:
        rospy.loginfo("GARRA ABERTA")
    else:
        rospy.loginfo("ERRO AO ABRIR A GARRA")
        moveit_commander.roscpp_shutdown()
        sys.exit()    
    
    
    # Define a pose inicial do objeto
    object_initial_pose = geometry_msgs.msg.Pose()
    object_initial_pose.orientation.w = 1.0
    object_initial_pose.position.x = 0.4 
    object_initial_pose.position.y = -0.2
    object_initial_pose.position.z = 0.18
    
    arm_group.set_pose_target(object_initial_pose)
    plan = arm_group.go(wait=True)
   
    if plan:
        rospy.loginfo("O BRAÇO ESTÁ PROXIMO AO OBJETO")
    else:
        rospy.loginfo("ERRO AO IR PARA A POSIÇÃO PROXIMA AO OBJETO")
        moveit_commander.roscpp_shutdown()
        sys.exit()
        
    
    scene.attach_box(eef_link, 'object', touch_links=touch_links)
    scene_objects.remove('object')
    wait_for_scene_update(scene, scene_objects, expected_attached_objects=['object'])
   
    rospy.sleep(5)
    
    # fecha a garra
    hand_group.set_named_target("Closed")
    plan = hand_group.go(wait=True)
    rospy.sleep(2)
    
    if plan:
        rospy.loginfo("GARRA FECHADA")
    else:
        rospy.loginfo("ERRO AO FECHAR A GARRA")
         
    
    rospy.sleep(1)
    
    
    # Define a pose de destino do objeto
    object_target_pose = geometry_msgs.msg.Pose()
    object_target_pose.orientation.w = 1
    object_target_pose.position.x = 0.4
    object_target_pose.position.y = 0.2
    object_target_pose.position.z = 0.2
    
    arm_group.set_pose_target(object_target_pose)
    plan = arm_group.go(wait=True)
    if plan:
        rospy.loginfo("O BRAÇO MOVEU O OBJETO")
    else:
        rospy.loginfo("ERRO AO MOVER O OBJETO")
        moveit_commander.roscpp_shutdown()
        sys.exit()  
        
        
    rospy.sleep(1)
    
    publicar = rospy.Publisher('/object_received', Bool, queue_size=10)
    rospy.sleep(1)
   
    # abre a garra para soltar o objeto
    hand_group.set_named_target("Open")
    plan = hand_group.go()
   
    if plan:
        rospy.loginfo("O BRAÇO SOLTOU O OBJETO")
        publicar.publish(True)
        rospy.loginfo("sinal enviado")
        
    else:
        publicar.publish(False)
        rospy.loginfo("ERRO AO SOLTAR O OBJETO")
        moveit_commander.roscpp_shutdown()
        sys.exit()
        
    rospy.sleep(1)
    scene.remove_attached_object(eef_link, name='object')
    scene_objects.append('object')
    wait_for_scene_update(scene, scene_objects, expected_attached_objects=None)

    rospy.sleep(1)
    
    # coloca o braço na posição inicial
    arm_group.set_named_target("Sleep")
    plan = arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()
    if plan:
        rospy.loginfo("O BRAÇO RETORNOU PARA A POSIÇAO INICIAL")
    else:
        rospy.loginfo("ERRO AO RETORNAR PARA A POSIÇAO INICIAL")

    rospy.sleep(1)
    

    scene.clear()


def create_scene(scene, reference_frame='world'):
    """Criar uma cena artificial no Rviz"""
    scene_objects = []

    # Criação de uma mesa (table 1)
    table1_name = 'table1'
    table1_size = (0.2, 0.2, 0.2)  # x, y, z
    table1_pose = PoseStamped()
    table1_pose.header.frame_id = reference_frame
    table1_pose.pose.orientation.w = 1.0
    table1_pose.pose.position.x = 0.4
    table1_pose.pose.position.y = -0.2
    table1_pose.pose.position.z = 0
    scene.add_box(table1_name, table1_pose, size=table1_size)
    scene_objects.append(table1_name)
    
    
    # Criação de uma mesa (table 2)
    table2_name = 'table2'
    table2_size = (0.2, 0.2, 0.2)  # x, y, z
    table2_pose = PoseStamped()
    table2_pose.header.frame_id = reference_frame
    table2_pose.pose.orientation.w = 1.0
    table2_pose.pose.position.x = 0.4
    table2_pose.pose.position.y = 0.2
    table2_pose.pose.position.z = 0
    scene.add_box(table2_name, table2_pose, size=table2_size)
    scene_objects.append(table2_name)

    # Cria um objeto a ser pegado (object)
    object_name = 'object'
    object_height = 0.1
    object_radius = 0.01
    object_pose = PoseStamped()
    object_pose.header.frame_id = reference_frame
    object_pose.pose.orientation.w = 1.0
    object_pose.pose.position.x = 0.4
    object_pose.pose.position.y = -0.2
    object_pose.pose.position.z = 0.15
    scene.add_cylinder(object_name, object_pose, object_height, object_radius, )
    scene_objects.append(object_name)



    try:
        wait_for_scene_update(scene, expected_scene_objects=scene_objects)
        return scene_objects
    except TimeoutError as error:
        rospy.logerr(error.args[0] + ' Objects not created.')
        scene.clear()
        return None


def wait_for_scene_update(scene, expected_scene_objects=None,
                        expected_attached_objects=None, timeout=10):
    """Wait until moveit scene is updated"""
    if expected_scene_objects is None:
        expected_scene_objects = []
    if expected_attached_objects is None:
        expected_attached_objects = []

    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        
        scene_objects_ok = \
            set(expected_scene_objects) == set(scene.get_known_object_names())
       
        attached_objects_ok = \
            set(expected_attached_objects) == set(scene.get_attached_objects())

        if scene_objects_ok and attached_objects_ok:
            return
        else:
            rospy.sleep(0.1)
            seconds = rospy.get_time()

  
    raise TimeoutError('Scene was not updated before timeout.')

if __name__ == "__main__":
    main()


