FROM ros:noetic-ros-base

# Change the default shell to Bash
SHELL [ "/bin/bash" , "-c" ]

RUN source /opt/ros/noetic/setup.bash \
    && mkdir -p /opt/ros/src \
    && cd opt/ros/src \
    && catkin_create_pkg move_base_send_goal std_msgs rospy

COPY src opt/ros/src/move_base_send_goal/src
COPY etc opt/ros/src/move_base_send_goal/etc

RUN cd opt/ros/src/move_base_send_goal/src \
    && chmod +x service.py

RUN apt-get update \
    && apt-get --yes install python3-pip \ 
    && apt-get --yes install ros-noetic-navigation
 
WORKDIR opt/ros

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade protobuf==3.20.0

RUN source /opt/ros/noetic/setup.bash && \
    catkin_make 

COPY bootstrap.sh /opt/ros/src/move_base_send_goal/src
RUN cd /opt/ros/src/move_base_send_goal/src && \
    chmod +x bootstrap.sh

WORKDIR /opt/ros/src/move_base_send_goal/src    

