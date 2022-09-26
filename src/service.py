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

from move_base_send_task.moveBaseSendTask import ManageTasks

if __name__== "__main__":

    config_file = sys.argv[1] if len(sys.argv) > 1 else '../etc/config/config.json'
    config = json.load(open(config_file, 'r'))
    broker_uri = config['broker_uri']
    area_id = config['area_id']
    microphone_id = config['microphone_id']
    position_interpreter_topic = f"PathPlanner.AreaID.{area_id}.GetPath"
    speech_recognition_topic = f"SpeechRecognition.{microphone_id}.Phrase"
    channel = Channel(broker_uri)
    subscription = Subscription(channel)
    subscription.subscribe(topic = position_interpreter_topic)
    subscription.subscribe(topic = speech_recognition_topic)
    rospy.init_node('movebase_send_goal_py')
    move_base_send_tasks = ManageTasks(
        area_id = area_id, 
        microphone_id = microphone_id)

    while True:
        message = channel.consume()
        result = move_base_send_tasks.move_base_send_task(message)
        