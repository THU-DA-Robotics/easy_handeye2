import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    aruco_single_params = {
        "image_is_rectified": False,
        "marker_id": 99,
        "marker_size": 0.15,
        "reference_frame": "camera_base",
        "camera_frame": "rgb_camera_link",
        "marker_frame": "camera_marker",
        "corner_refinement": "LINES",
    }
    aruco_camera_info_topic_name = "/rgb/camera_info"
    aruco_image_topic_name = "/rgb/image_raw"

    easy_handeye_launch_path = os.path.join(
        get_package_share_directory("easy_handeye2"), "launch", "calibrate.launch.py"
    )

    return LaunchDescription(
        [
            Node(
                package="aruco_ros",
                executable="single",
                parameters=[aruco_single_params],
                remappings=[
                    ("/camera_info", aruco_camera_info_topic_name),
                    ("/image", aruco_image_topic_name),
                ],
            ),
            # Include the easy_handeye2 launch file with arguments
            IncludeLaunchDescription(
                easy_handeye_launch_path,
                launch_arguments={
                    "calibration_type": "eye_on_base",
                    "name": "kinect_panda_calib",
                    "robot_base_frame": "panda_link0",
                    "robot_effector_frame": "panda_hand",
                    "tracking_base_frame": "camera_base",
                    "tracking_marker_frame": "camera_marker",
                }.items(),
            ),
        ]
    )
