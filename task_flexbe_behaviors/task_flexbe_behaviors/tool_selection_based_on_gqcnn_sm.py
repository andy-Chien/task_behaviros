#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from mm_flexbe_states.moveit_compute_ik import MoveItComputeIK
from task_flexbe_states.gqcnn_grasp_plan_state import GQCNNGraspPlanState
from task_flexbe_states.img_masking_client_state import ImgMaskingClientState
from task_flexbe_states.picking_pose_adjust_state import PickingPoseAdjustState
from task_flexbe_states.set_data_by_data_state import SetDataByDataState
from task_flexbe_states.tool_selection_state import ToolSelectionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 01 2023
@author: Andy Chien
'''
class ToolSelectionbasedonGQCNNSM(Behavior):
    '''
    Using FC pj and suc gqcnn to decide a tool and the grasp pose
    '''


    def __init__(self, node):
        super(ToolSelectionbasedonGQCNNSM, self).__init__()
        self.name = 'Tool Selection based on GQCNN'

        # parameters of this behavior
        self.add_parameter('group_name', '')
        self.add_parameter('joint_names', dict())
        self.add_parameter('namespace', '')

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        GQCNNGraspPlanState.initialize_ros(node)
        ImgMaskingClientState.initialize_ros(node)
        MoveItComputeIK.initialize_ros(node)
        PickingPoseAdjustState.initialize_ros(node)
        SetDataByDataState.initialize_ros(node)
        ToolSelectionState.initialize_ros(node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
		
		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:679 y:198, x:190 y:260, x:197 y:475
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'nothing_to_grasp'], input_keys=['curr_tool_name', 'fail_cnt', 'ik_target_frame', 'start_joints'], output_keys=['target_tool_name', 'target_pose'])
        _state_machine.userdata.curr_tool_name = 'suction'
        _state_machine.userdata.target_pose = None
        _state_machine.userdata.target_tool_name = ''
        _state_machine.userdata.fail_cnt = 0
        _state_machine.userdata.ik_target_frame = 'tool_tip'
        _state_machine.userdata.translation_list = [0,0,0]
        _state_machine.userdata.start_joints = None
        _state_machine.userdata.retry_cnt = 0
        _state_machine.userdata.zero = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


        with _state_machine:
            # x:48 y:47
            OperatableStateMachine.add('get_masked_img',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=False, mark_release=False, get_masked_img=True, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'gqcnn', 'failed': 'release_occupied_marker', 'retry': 'get_masked_img'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:732 y:236
            OperatableStateMachine.add('check_ik',
                                        MoveItComputeIK(group_name=self.group_name, joint_names=self.joint_names, namespace=self.namespace, from_frame='base_link', to_frame='tool_tip', translation_in_target_frame=True),
                                        transitions={'done': 'finished', 'failed': 'adjust_pose'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'start_joints': 'start_joints', 'target_pose': 'target_pose', 'target_frame': 'ik_target_frame', 'translation_list': 'translation_list', 'target_joints': 'target_joints'})

            # x:36 y:329
            OperatableStateMachine.add('gqcnn',
                                        GQCNNGraspPlanState(pj_grasp_service='/gqcnn_pj/grasp_planner_segmask', suc_grasp_service='/gqcnn_suc/grasp_planner_segmask'),
                                        transitions={'done': 'reset_retry_cnt', 'failed': 'release_occupied_marker', 'retry': 'release_marker_occupy', 'nothing': 'nothing_to_grasp'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off, 'nothing': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'camera_info_msg': 'img_info', 'pj_pose': 'pj_pose', 'suc_pose': 'suc_pose', 'frame': 'frame', 'pj_qv': 'pj_qv', 'suc_qv': 'suc_qv'})

            # x:377 y:172
            OperatableStateMachine.add('release_marker_occupy',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=False, mark_release=True, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'get_masked_img', 'failed': 'failed', 'retry': 'release_marker_occupy'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:126 y:167
            OperatableStateMachine.add('release_occupied_marker',
                                        ImgMaskingClientState(namespace='', marker_id=5, create_depth_mask=False, update_mask=False, start_update_timer=False, stop_update_timer=False, mark_release=True, get_masked_img=False, resolution_wide=516, resolution_high=386),
                                        transitions={'done': 'failed', 'failed': 'failed', 'retry': 'release_occupied_marker'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'retry': Autonomy.Off},
                                        remapping={'mask_img_msg': 'mask_img_msg', 'img_info': 'img_info', 'marker_poses': 'marker_poses', 'poses_frame': 'poses_frame'})

            # x:237 y:348
            OperatableStateMachine.add('reset_retry_cnt',
                                        SetDataByDataState(userdata_src_names=['zero'], userdata_dst_names=['retry_cnt']),
                                        transitions={'done': 'select_tool'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'zero': 'zero', 'retry_cnt': 'retry_cnt'})

            # x:408 y:349
            OperatableStateMachine.add('select_tool',
                                        ToolSelectionState(),
                                        transitions={'done': 'adjust_pose', 'failed': 'release_marker_occupy'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'marker_poses': 'marker_poses', 'pj_pose': 'pj_pose', 'suc_pose': 'suc_pose', 'frame': 'frame', 'pj_qv': 'pj_qv', 'suc_qv': 'suc_qv', 'curr_tool': 'curr_tool_name', 'img_info': 'img_info', 'img': 'mask_img_msg', 'fail_cnt': 'fail_cnt', 'target_pose': 'target_pose', 'tar_tool': 'target_tool_name'})

            # x:718 y:320
            OperatableStateMachine.add('adjust_pose',
                                        PickingPoseAdjustState(),
                                        transitions={'done': 'check_ik', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'marker_poses': 'marker_poses', 'target_pose': 'target_pose', 'retry_cnt': 'retry_cnt'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]