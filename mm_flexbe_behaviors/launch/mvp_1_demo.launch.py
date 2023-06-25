# Copyright (c) 2021 Stogl Robotics Consulting UG (haftungsbeschränkt)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the {copyright_holder} nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Denis Stogl

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    joy_dev = LaunchConfiguration("joy_dev")
    namespace = LaunchConfiguration("namespace")
    launch_rviz = LaunchConfiguration("launch_rviz")

    mobile_manipulator = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("mm_description"), "/launch", "/gazebo_trajectory.launch.py"]
        ),
        launch_arguments={
            "sim_gazebo": "true",
            "joy_dev": joy_dev,
            "namespace": namespace,
            "launch_rviz": "false",
            "initial_controller": "mm_trajectory_controller"}.items(),
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("mm_navigation_config"), "/launch", "/robot_navigation.launch.py"]
        ),
        launch_arguments={
            "use_sim_time": "true",
            "launch_controller": "false",
            "launch_rviz": "true"}.items(),
    )

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("mm_moveit_config"), "/launch", "/robot_moveit.launch.py"]
        ),
        launch_arguments={
            "use_sim_time": "true",
            "launch_rviz": "true"}.items(),
    )

    cmd_adapter = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("mm_cmd_adapter"), "/launch", "/cmd_adapter.launch.py"]
        ),
        launch_arguments={
            "namespace": namespace}.items(),
    )

    flexbe_app = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("flexbe_app"), "/launch", "/flexbe_full.launch.py"]
        ),
    )

    vision_node = Node(
        name="vision_prepro_srv",
        package="vision_preprocess_srv", 
        executable="vision_prepro_srv", 
        output="screen",
    )

    painting_plan = Node(
        name="painting_plan",
        package="wall_painting_trajectory_planner", 
        executable="start", 
        output="screen",
    )

    traj_tracking = Node(
        name="traj_tracking",
        package="mm_ik", 
        executable="traj_ik_srv", 
        output="screen",
    )

    return [mobile_manipulator,
            navigation,
            moveit,
            cmd_adapter,
            flexbe_app,
            # vision_node,
            # painting_plan,
            traj_tracking
            ]


def generate_launch_description():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "joy_dev",
            default_value="js0",
            description="mobile base type",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "namespace", 
            default_value="", 
            description="Namespace for node"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_rviz", 
            default_value="true", 
            description="Launch RViz?",
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])