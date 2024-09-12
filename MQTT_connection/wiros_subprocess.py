import roslaunch, rospy, subprocess


def start_roscore():
    command = f'bash -c "source ~/.bashrc && roscore"'
    
    # Start roscore in a new macOS Terminal window
    # return subprocess.Popen(['gnome-terminal', '--', 'roscore'])
    process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.DEVNULL)
    return process

def stop_roscore():
    rospy.signal_shutdown('roscore subprocess shutdown')

def stop_roslaunch():
    pass

# Function to launch a ROS launch file
def run_ros_launch(launch_file):
    # # Initialize the ROS node 
    rospy.init_node('roslaunch_script', anonymous=True)

    # # Prepare the launch file
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)

    # Define the command to source the bashrc and run roslaunch
    command = f'bash -c "source ~/.bashrc && roslaunch {launch_file}"'

    # Run the command in a subprocess within a new GNOME Terminal
    process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.DEVNULL)

    # # Keep the script alive to maintain the ROS launch process
    # rospy.spin()

    return process


        
if __name__ == "__main__":
    start_roscore()
    print("roscore started in a new Terminal window.")
    # Example usage
    launch_file = "/home/wcsng/van_wiros/src/wiros_csi_node/launch/basic.launch"    # Replace with your launch file name
    # launch_file = "launch/basic.launch"    # Replace with your launch file name
    run_ros_launch( launch_file)
