from is_msgs.robot_pb2 import PathRequest
from is_msgs.common_pb2 import Phrase

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID


class MoveBaseSendTasks():

    def __init__(self, area_id, microphone_id):
        self.position_interpreter_topic = f"PathPlanner.AreaID.{area_id}.GetPath"
        self.speech_recognition_topic = f"SpeechRecognition.{microphone_id}.Phrase" 

    def move_base_send_task(self, message):     
        if message.topic == self.position_interpreter_topic:
            pathRequest = message.unpack(PathRequest)            
            self.__movebase_send_goal(
                x = pathRequest.destination_pose.position.x,
                y = pathRequest.destination_pose.position.y
            )      

        elif message.topic == self.speech_recognition_topic:
            message.unpack(Phrase)
            phrase = message.unpack(Phrase)
            for word in phrase.content:
                if word in ['pare', 'stop']:      
                    self.__move_base_stop()

    def __movebase_send_goal(self, x, y):
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("wait for move base server")
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1
        client.send_goal(goal)
        rospy.loginfo(f" send goal to x = {x} y = {y}")

    def __move_base_stop(self):
        cancel_pub = rospy.Publisher("/move_base/cancel", actionlib.GoalID, queue_size=1)
        cancel_msg = GoalID()
        cancel_pub.publish(cancel_msg)
        rospy.loginfo(f"goal canceled")