#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.decision_state import DecisionState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from task_flexbe_behaviors.add_box_to_scene_sm import AddBoxToSceneSM
from task_flexbe_behaviors.change_tool_task_sm import ChangeToolTaskSM
from task_flexbe_behaviors.move_arm_to_joints_async_sm import MoveArmToJointsAsyncSM
from task_flexbe_behaviors.move_to_pick_sm import MoveToPickSM
from task_flexbe_behaviors.move_to_place_sm import MoveToPlaceSM
from task_flexbe_behaviors.tool_selection_based_on_gqcnn_sm import ToolSelectionbasedonGQCNNSM
from task_flexbe_states.get_DIO_state import GetDIOState
from task_flexbe_states.img_masking_client_state import ImgMaskingClientState
from task_flexbe_states.moveit_attached_obj_state import MoveItAttachedObjState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 01 2023
@author: Andy Chien
'''
class MultipleToolsBinPickingTaskSM(Behavior):
    '''
    Bin picking using multiple tools depend on GQCNN
    '''


    def __init__(self, node):
        super(MultipleToolsBinPickingTaskSM, self).__init__()
        self.name = 'Multiple Tools Bin Picking Task'

        # parameters of this behavior
        self.add_parameter('group_name', 'ur_manipulator')
        self.add_parameter('namespace', 'robot_2')
        self.add_parameter('sim', True)
        self.add_parameter('init_joints', dict())
        self.add_parameter('pressure_sensor_pin', dict())
        self.add_parameter('pick_and_place_param_file', 'task_flexbe_behaviors/config/pick_and_place.yaml')
        self.add_parameter('io_topic', dict())
        self.add_parameter('io_service', dict())
        self.add_parameter('place_pos_max', dict())
        self.add_parameter('place_pos_min', dict())
        self.add_parameter('infront_sucker', dict())
        self.add_parameter('sucker_spot', dict())
        self.add_parameter('joint_names', dict())
        self.add_parameter('vacuum_io_pins', dict())

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        DecisionState.initialize_ros(node)
        FlexibleCheckConditionState.initialize_ros(node)
        GetDIOState.initialize_ros(node)
        ImgMaskingClientState.initialize_ros(node)
        MoveItAttachedObjState.initialize_ros(node)
        self.add_behavior(AddBoxToSceneSM, 'Add Picking Box To Scene', node)
        self.add_behavior(ChangeToolTaskSM, 'Change Tool Task', node)
        self.add_behavior(ChangeToolTaskSM, 'Change Tool Task_2', node)
        self.add_behavior(MoveArmToJointsAsyncSM, 'Move Arm To Init Joints Async', node)
        self.add_behavior(MoveArmToJointsAsyncSM, 'Move Arm To Relay Joints Async', node)
        self.add_behavior(MoveToPickSM, 'Move To Pick', node)
        self.add_behavior(MoveToPlaceSM, 'Move To Place', node)
        self.add_behavior(ToolSelectionbasedonGQCNNSM, 'Tool Selection based on GQCNN', node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:600 y:213, x:108 y:555
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.zero_vector_3 = [0.0, 0.0, 0.0]
        _state_machine.userdata.gripper_mode = 'expert'
        _state_machine.userdata.pressure_sensor_pin = self.pressure_sensor_pin
        _state_machine.userdata.curr_tool_name = 'pj'
        _state_machine.userdata.place_pose = None
        _state_machine.userdata.velocity = 10
        _state_machine.userdata.target_tool_name = 'suction'
        _state_machine.userdata.exe_client = None
        _state_machine.userdata.init_joints = self.init_joints
        _state_machine.userdata.ik_target_frame = 'tool_tip'
        _state_machine.userdata.expected_joints = None
        _state_machine.userdata.none = None

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:51 y:39
            OperatableStateMachine.add('Move Arm To Init Joints Async',
                                        self.use_behavior(MoveArmToJointsAsyncSM, 'Move Arm To Init Joints Async',
                                            default_keys=['start_joints'],
                                            parameters={'group_name': self.group_name, 'joint_names': self.joint_names, 'namespace': self.namespace, 'use_curr_as_start': True}),
                                        transitions={'finished': 'start_img_update', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'velocity': 'velocity', 'target_joints': 'init_joints', 'exe_client': 'exe_client', 'expected_joints': 'expected_joints'})

            # x:579 y:36
            OperatableStateMachine.add('Change Tool Task',
                                        self.use_behavior(ChangeToolTaskSM, 'Change Tool Task',
                                            parameters={'namespace': self.namespace, 'group_name': self.group_name, 'joint_names': self.joint_names, 'sim': self.sim, 'infront_sucker': self.infront_sucker, 'sucker_spot': self.sucker_spot}),
                                        transitions={'finished': 'Tool Selection based on GQCNN', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'target_tool_name': 'target_tool_name', 'exe_client': 'exe_client', 'curr_tool_name': 'curr_tool_name', 'expected_joints': 'expected_joints', 'tool_frame': 'ik_target_frame'})

            # x:531 y:723
            OperatableStateMachine.add('Change Tool Task_2',
                                        self.use_behavior(ChangeToolTaskSM, 'Change Tool Task_2',
                                            parameters={'namespace': self.namespace, 'group_name': self.group_name, 'joint_names': self.joint_names, 'sim': self.sim, 'infront_sucker': self.infront_sucker, 'sucker_spot': self.sucker_spot}),
                                        transitions={'finished': 'Move To Pick', 'failed': 'release_occupied_marker_2'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'target_tool_name': 'target_tool_name', 'exe_client': 'exe_client', 'curr_tool_name': 'curr_tool_name', 'expected_joints': 'expected_joints', 'tool_frame': 'ik_target_frame'})

            # x:593 y:277
            OperatableStateMachine.add('Move Arm To Relay Joints Async',
                                        self.use_behavior(MoveArmToJointsAsyncSM, 'Move Arm To Relay Joints Async',
                                            parameters={'group_name': self.group_name, 'joint_names': self.joint_names, 'namespace': self.namespace, 'wait': False}),
                                        transitions={'finished': 'Tool Selection based on GQCNN', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'start_joints': 'expected_joints', 'velocity': 'velocity', 'target_joints': 'init_joints', 'exe_client': 'exe_client', 'expected_joints': 'expected_joints'})

            # x:531 y:621
            OperatableStateMachine.add('Move To Pick',
                                        self.use_behavior(MoveToPickSM, 'Move To Pick',
                                            parameters={'io_service': self.io_service, 'sim': self.sim, 'joint_names': self.joint_names, 'select_tool_by_input': True, 'namespace': self.namespace, 'group_name': self.group_name, 'vacuum_io_pins': self.vacuum_io_pins, 'pressure_sensor_pin': self.pressure_sensor_pin, 'io_topic': self.io_topic}),
                                        transitions={'finished': 'attach_obj', 'failed': 'release_occupied_marker_2'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'start_joints': 'expected_joints', 'velocity': 'velocity', 'exe_client': 'exe_client', 'pick_pose': 'target_picking_pose', 'ik_target_frame': 'ik_target_frame', 'tool_name': 'curr_tool_name', 'expected_joints': 'expected_joints'})

            # x:531 y:430
            OperatableStateMachine.add('Move To Place',
                                        self.use_behavior(MoveToPlaceSM, 'Move To Place',
                                            parameters={'io_service': self.io_service, 'sim': self.sim, 'place_in_random_area': True, 'joint_names': self.joint_names, 'select_tool_by_input': True, 'namespace': self.namespace, 'group_name': self.group_name, 'place_pos_max': self.place_pos_max, 'place_pos_min': self.place_pos_min, 'vacuum_io_pins': self.vacuum_io_pins}),
                                        transitions={'finished': 'detach_obj', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'start_joints': 'expected_joints', 'exe_client': 'exe_client', 'place_pose': 'place_pose', 'tool_name': 'curr_tool_name', 'velocity': 'velocity', 'ik_target_frame': 'ik_target_frame', 'expected_joints': 'expected_joints'})

            # x:741 y:203
            OperatableStateMachine.add('Tool Selection based on GQCNN',
                                        self.use_behavior(ToolSelectionbasedonGQCNNSM, 'Tool Selection based on GQCNN'),
                                        transitions={'finished': 'check_tool', 'failed': 'failed', 'nothing_to_grasp': 'stop_img_update'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'nothing_to_grasp': Autonomy.Inherit},
                                        remapping={'curr_tool_name': 'curr_tool_name', 'target_tool_name': 'target_tool_name', 'target_pose': 'target_picking_pose'})

            # x:787 y:620
            OperatableStateMachine.add('attach_obj',
                                        MoveItAttachedObjState(mesh_file='', operation='add', obj_type='box', link_name='', touch_links=[], size=[0.1, 0.1, 0.1], namespace=self.namespace, obj_name='picked_obj', pos=[0.0,0.0,0.0], quat=[1.0,0.0,0.0,0.0]),
                                        transitions={'done': 'release_occupied_marker'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'link_name': 'ik_target_frame', 'pose': 'none'})

            # x:796 y:368
            OperatableStateMachine.add('check_suc_status',
                                        DecisionState(outcomes=['True', 'False'], conditions=lambda x: x[0]),
                                        transitions={'True': 'Move To Place', 'False': 'detach_obj'},
                                        autonomy={'True': Autonomy.Off, 'False': Autonomy.Off},
                                        remapping={'input_value': 'pressure_sensor_vals'})

            # x:887 y:702
            OperatableStateMachine.add('check_tool',
                                        FlexibleCheckConditionState(predicate=lambda x: x[0] == x[1], input_keys=['curr_tool', 'target_tool']),
                                        transitions={'true': 'Move To Pick', 'false': 'Change Tool Task_2'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'curr_tool': 'curr_tool_name', 'target_tool': 'target_tool_name'})

            # x:545 y:353
            OperatableStateMachine.add('detach_obj',
                                        MoveItAttachedObjState(mesh_file='', operation='remove', obj_type='box', link_name='', touch_links=[], size=[0.1, 0.1, 0.1], namespace=self.namespace, obj_name='picked_obj', pos=[0.0,0.0,0.0], quat=[1.0,0.0,0.0,0.0]),
                                        transitions={'done': 'Move Arm To Relay Joints Async'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'link_name': 'ik_target_frame', 'pose': 'none'})

            # x:797 y:460
            OperatableStateMachine.add('get_suc_io',
                                        GetDIOState(io_topic=self.io_topic, namespace=self.namespace, sim=self.sim),
                                        transitions={'done': 'check_suc_status'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pins': 'pressure_sensor_pin', 'vals': 'pressure_sensor_vals'})

            # x:809 y:543
            OperatableStateMachine.add('is_suc',
                                        DecisionState(outcomes=['True', 'False'], conditions=lambda x: 'suc' in x),
                                        transitions={'True': 'get_suc_io', 'False': 'Move To Place'},
                                        autonomy={'True': Autonomy.Off, 'False': Autonomy.Off},
                                        remapping={'input_value': 'curr_tool_name'})

            # x:530 y:524
            OperatableStateMachine.add('release_occupied_marker',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=False, mark_release=True, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'is_suc', 'failed': 'failed', 'retry': 'release_occupied_marker'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:116 y:601
            OperatableStateMachine.add('release_occupied_marker_2',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=False, mark_release=True, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'failed', 'failed': 'failed', 'retry': 'release_occupied_marker_2'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:211 y:140
            OperatableStateMachine.add('start_img_update',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=True, start_update_timer=True, stop_update_timer=False, mark_release=False, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'Add Picking Box To Scene', 'failed': 'failed', 'retry': 'Add Picking Box To Scene'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:543 y:116
            OperatableStateMachine.add('stop_img_update',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=True, mark_release=False, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'finished', 'failed': 'failed', 'retry': 'stop_img_update'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:313 y:41
            OperatableStateMachine.add('Add Picking Box To Scene',
                                        self.use_behavior(AddBoxToSceneSM, 'Add Picking Box To Scene',
                                            parameters={'namespace': self.namespace, 'box_name': 'picking_box'}),
                                        transitions={'finished': 'Change Tool Task'},
                                        autonomy={'finished': Autonomy.Inherit},
                                        remapping={'frame_id': 'poses_frame', 'marker_poses': 'marker_poses'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
