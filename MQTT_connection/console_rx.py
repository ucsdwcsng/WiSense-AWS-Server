import roslaunch, subprocess
import rospy

# Function to launch a ROS launch file
def run_ros_launch( launch_file):
    # # Initialize the ROS node 
    rospy.init_node('roslaunch_script', anonymous=True)

    # Prepare the launch file
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    
    # Create the launch file path and start the launch
    launch = roslaunch.parent.ROSLaunchParent(uuid,  [launch_file])
    
    try:
        # Define the command to source the ROS environment and run roslaunch
        command = f"source /opt/ros/noetic/setup.bash"

        # Run the command in a bash shell
        subprocess.run(command, shell=True, executable='/bin/bash')
        print('sourced')
        print("Starting ROS launch...")
        launch.start()
        
        # Keep the script alive to maintain the ROS launch process
        rospy.spin()  # This will keep the process alive until it's interrupted

        
    except KeyboardInterrupt:
        print("Shutting down ROS launch...")
        launch.shutdown()

# Example usage
launch_file = "~/wiros/src/wiros_csi_node/launch/basic.launch"    # Replace with your launch file name
run_ros_launch(launch_file)
