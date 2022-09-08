import socket

from is_wire.core import Channel, Subscription
from is_msgs.robot_pb2 import PathRequest

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback, MoveBaseResult
from tf.transformations import quaternion_from_euler


def define_goal(x, y, theta_rad):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map' 
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    quaternion = quaternion_from_euler(0, 0, theta_rad)
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]    
    return goal 

def send_goal(x, y, theta_rad, client):
    goal = define_goal(x, y, theta_rad)
    client.send_goal(goal)
    print('setting final position task to  x:{:.2f}, y:{:.2f}, theta: {:.2f}'.format(pose[0],pose[1],pose[2]))
    client.wait_for_result()


if __name__== "__main__":
    channel = Channel("amqp://10.10.3.188:30000")
    subscription = Subscription(channel)
    subscription.subscribe(topic=f"PathPlanner.AreaID.{0}.GetPath")

    while True:
        message = channel.consume()
        pathRequest = message.unpack(PathRequest)
        rospy.init_node('send_client_goal')
        client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move base server")
        client.wait_for_server()     
        send_goal(  x= pathRequest.destination_pose.position.x,
                    y = pathRequest.destination_pose.position.y,
                    theta = 0, 
                    client = client)
        client.cancel_all_goals()
    