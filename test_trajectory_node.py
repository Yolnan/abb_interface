#!/usr/bin/env python

import rospy
import yaml
from actionlib import SimpleActionClient
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal

def load_trajectory_from_yaml(file_name):
    """Load joint trajectory from a yaml file."""
    with open(file_name, 'r') as file:
        trajectory_data = yaml.safe_load(file)

    # Convert the data into a JointTrajectoryPoint list
    points = []
    for step in trajectory_data:
        point = JointTrajectoryPoint()
        point.positions = step['positions']
        point.time_from_start = rospy.Duration(step['time_from_start'])
        points.append(point)

    return points

if __name__ == "__main__":
    rospy.init_node('trajectory_loader_node', anonymous=True)

    # Load the joint trajectory from the yaml file
    trajectory_points = load_trajectory_from_yaml("test_trajectory.yaml")

    # Set up the action client
    client = SimpleActionClient('joint_trajectory_action', FollowJointTrajectoryAction)
    client.wait_for_server()

    # Create the goal message
    goal = FollowJointTrajectoryGoal()
    goal.trajectory.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
    goal.trajectory.points = trajectory_points

    # Send the goal to the action server
    client.send_goal(goal)
    client.wait_for_result()

    # Log the result
    result = client.get_result()
    if result.error_code == 0:
        rospy.loginfo("Trajectory executed successfully.")
    else:
        rospy.logerr("Error executing trajectory: %s", result.error_string)
