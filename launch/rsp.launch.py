from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    Command,
)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    package_name = FindPackageShare("diff_drive_robot")

    urdf_path = PathJoinSubstitution([
        package_name,
        "urdf",
        "robot.urdf",
    ])

    use_sim_time = LaunchConfiguration("use_sim_time")
    urdf = LaunchConfiguration("urdf")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    declare_urdf = DeclareLaunchArgument(
        "urdf",
        default_value=urdf_path,
        description="Path to the robot description file",
    )

    robot_description = ParameterValue(
        Command(["xacro ", urdf]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "robot_description": robot_description,
        }],
    )

    return LaunchDescription([
        declare_urdf,
        declare_use_sim_time,
        robot_state_publisher,
    ])