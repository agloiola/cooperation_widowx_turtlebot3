# Colaboração entre WidowX-250s e Turtlebot3 com ROS

Este repositório apresenta um tutorial para a simulação de uma colaboração simples entre o braço robótico **WidowX-250s** e o **Turtlebot3 Waffle Pi**, utilizando o **ROS (Robot Operating System)**.  

## Objetivo

O objetivo deste projeto é criar uma simulação onde:  
1. O Turtlebot3 se move até uma posição próxima ao braço robótico WidowX-250s.
2. O WidowX-250s pega um objeto de uma mesa e o transfere para o Turtlebot3. 
3. Após receber o objeto, o Turtlebot3 se desloca para outra posição, transportando o objeto.
   
## Índice
- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Execução](#execução)

## Pré-requisitos

Antes de começar, certifique-se de que você tenha o seguinte instalado e configurado:

- [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu) (Ubuntu 20.04)
- Python 3
- RViz
- Gazebo
- [MoveIt](https://moveit.ai/install/)

## Instalação
Siga estas etapas para configurar o ambiente de simulação:

1. Clone o repositório do braço robótico para o seu workspace ROS:
   
    Faça o download dos pacotes fornecidos pelo fabricante do braço robótico WidowX-250s.
   ```bash
   cd ~/catkin_ws/src && git clone https://github.com/Interbotix/interbotix_ros_manipulators.git
   cd ~/catkin_ws/src/interbotix_ros_manipulators/interbotix_ros_xsarms && rm CATKIN_IGNORE
   cd ~/catkin_ws/src && git clone https://github.com/Interbotix/interbotix_ros_core.git
   cd ~/catkin_ws/src/interbotix_ros_core/interbotix_ros_xseries && rm CATKIN_IGNORE 
   cd ~/catkin_ws/src && git clone https://github.com/Interbotix/interbotix_ros_toolboxes.git
   cd ~/catkin_ws/src/interbotix_ros_toolboxes/interbotix_xs_toolbox && rm CATKIN_IGNORE 
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash 

2. Clone o repositório do Turtlebot3 para o seu workspace ROS:

    Faça o download dos pacotes fornecidos pelo fabricante do Turtlebot3.
   
   ```bash
   cd ~/catkin_ws/src
   git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
   git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash

3. Clone o repositório de cooperação para o seu workspace ROS:
   
    Por fim, instale este repositório, que contém os arquivos necessários para a cooperação entre o WidowX-250s e o Turtlebot3:

   ```bash
   cd ~/catkin_ws/src
   git clone https://github.com/agloiola/cooperation_widowx_turtlebot3.git
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash

## Execução

Siga os passos abaixo para executar a simulação de cooperação entre o WidowX-250s e o Turtlebot3:

1. Inicie o ambiente de simulação:
   
   Abra um terminal e execute o comando a seguir para iniciar o ambiente de simulação:
   ```bash
   roslaunch cooperation_widowx_turtlebot3 wx250s_turtlebot3.launch
   

   Este comando inicializa o ambiente de simulação no Gazebo, contendo o braço robótico e o robô móvel, além do RViz e do MoveIt!, que são utilizados para planejar e executar os movimentos do braço robótico.

2. Inicie o mapa do ambiente de simulação:
   
   Abra um terminal e execute o comando a seguir para iniciar o mapa do ambiente de simulação:
   ```bash
   roslaunch cooperation_widowx_turtlebot3 turtlebot3_localization.launch 

Este comando inicializa o mapa do ambiente de simulação para a navegação do Turtlebot3.

3. Execute o launch de cooperação:
   
   Abra um novo terminal e execute o comando:
   ```bash
   roslaunch cooperation_widowx_turtlebot3 cooperation.launch
   
   
   Este comando inicia o script de cooperação, fazendo com que o Turtlebot3 se desloque até a posição próxima ao braço robótico. Assim que o robô chegar a essa posição, o braço robótico executará a ação de pegar e mover o objeto de uma mesa para o robô móvel, que, por fim, transportará o objeto para outra posição.
