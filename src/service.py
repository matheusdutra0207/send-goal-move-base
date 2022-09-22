#!/usr/bin/env python
# license removed for brevity

import socket

from is_wire.core import Channel, Subscription
from is_msgs.robot_pb2 import PathRequest
from is_msgs.common_pb2 import Phrase

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalID

from move_base_send_task.moveBaseSendTask import MoveBaseSendTasks

if __name__== "__main__":
    area_id = 0
    microphone_id = 0
    position_interpreter_topic = f"PathPlanner.AreaID.{area_id}.GetPath"
    speech_recognition_topic = f"SpeechRecognition.{microphone_id}.Phrase"
    channel = Channel("amqp://10.10.3.188:30000")
    subscription = Subscription(channel)
    subscription.subscribe(topic = position_interpreter_topic)
    subscription.subscribe(topic = speech_recognition_topic)
    rospy.init_node('movebase_send_goal_py')
    move_base_send_tasks = MoveBaseSendTasks(
        area_id = area_id, 
        microphone_id = microphone_id)

    while True:
        message = channel.consume()
        result = move_base_send_tasks.move_base_send_task(message)
        