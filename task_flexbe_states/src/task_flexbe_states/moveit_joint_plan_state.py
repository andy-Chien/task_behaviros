#!/usr/bin/env python

import rospy
import moveit_commander
from moveit_msgs.msg import MoveItErrorCodes
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
# from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, Constraints, JointConstraint, MoveItErrorCodes

'''
Created on 23.02.2022

@author: Andy Chien
'''

class MoveItJointsPlanState(EventState):
	'''
	Uses MoveIt to plan the trajectory of specified joints value.

	-- robot_name       string      move group name.
	-- velocity         int     	The velocity for robot motion.

	># start_joints 	float[]		The joints of start pose, defult is current joints.
	># target_joints	float[]		Target configuration of the joints.
									Same order as their corresponding names in joint_names.

	#> joint_trajectory JointTrajectory  planned or executed trajectory

	<= done 						Target joint configuration has been planned.
	<= failed 						Failed to find a plan to the given joint configuration.
	'''


	def __init__(self, robot_name, velocity):
		'''
		Constructor
		'''
		super(MoveItJointsPlanState, self).__init__(outcomes=['failed', 'done'],
											input_keys=['start_joints', 'target_joints'],
											output_keys=['joint_trajectory'])
		# group_name = ""
		self._group_name = robot_name
		self._move_group = moveit_commander.MoveGroupCommander(self._group_name)
		self._move_group.set_planner_id("RRTConnectkConfigDefault")
		self._move_group.set_planning_time(1)
		self._velocity = velocity / 100 if 1 <= velocity <= 100 else 0.1
		self._result = None

	def execute(self, userdata):
		'''
		Execute this state
		'''
		if len(self._result.joint_trajectory.points) > 0:
			userdata.joint_trajectory = self._result
			userdata.target_joints = userdata.target_joints
			return 'done'
		else:
			return 'failed'

	def on_enter(self, userdata):
		self._move_group.set_max_velocity_scaling_factor(self._velocity)
		self._move_group.set_max_acceleration_scaling_factor(self._velocity)
		self._result = self._move_group.plan(userdata.target_joints)

	def on_stop(self):
		pass

	def on_pause(self):
		pass

	def on_resume(self, userdata):
		self.on_enter(userdata)