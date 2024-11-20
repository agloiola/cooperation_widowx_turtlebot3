# Colaboração entre WidowX-250s e Turtlebot3 com ROS

Este repositório apresenta um tutorial para a simulação de uma colaboração simples entre o braço robótico **WidowX-250s** e o **Turtlebot3 Waffle Pi**, utilizando o **ROS (Robot Operating System)**.  

## Objetivo

O objetivo deste projeto é criar uma simulação onde:  
1. O **Turtlebot3** se move até uma posição predefinida.  
2. O **WidowX-250s** transfere um objeto de uma mesa para o Turtlebot3.  
3. Após receber o objeto, o **Turtlebot3** se desloca para outra posição, transportando o objeto.

---

## Índice
- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Execução](#execução)

---

## Pré-requisitos

Antes de começar, certifique-se de que você tenha o seguinte instalado e configurado:

- [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu) (Ubuntu 20.04).  
- Python 3.  
- [RViz](http://wiki.ros.org/rviz) (para visualização).  
- [Gazebo](http://gazebosim.org/) (para simulação).  
- [MoveIt](https://moveit.ros.org/install/) (para controle do braço robótico).  

---

## Instalação
Siga estas etapas para configurar o ambiente de simulação:

1. Clone o repositório do braço robotico para o seu workspace ROS:
    Faça o download dos pacotes fornecidos pelo fabricante do braço robótico WidowX-250s.

2. Clone o repositório do Turtlebot3 para o seu workspace ROS:
    Faça o download dos pacotes fornecidos pelo fabricante do Turtlebot3.

3. Clone o repositório de cooperação para o seu workspace ROS:
    Por fim, instale este repositório, que contém os arquivos necessários para a cooperação.
