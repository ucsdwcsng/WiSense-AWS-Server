import roslaunch, subprocess
import rospy, shlex

def start_roscore():
    # Start roscore in a new macOS Terminal window
    return subprocess.Popen(['gnome-terminal', '--', 'roscore'])


# Function to launch a ROS launch file
def run_ros_launch( launch_file):
    # # Initialize the ROS node 
    rospy.init_node('roslaunch_script', anonymous=True)

    # # Prepare the launch file
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    # roslaunch.configure_logging(uuid)

    # Define the command to source the bashrc and run roslaunch
    command = f"source ~/.bashrc && roslaunch {launch_file}"

    # Construct the gnome-terminal command to run the command
    gnome_terminal_command = f'gnome-terminal -- bash -c "{command}"'

    # Run the command in a subprocess within a new GNOME Terminal
    process = subprocess.Popen(gnome_terminal_command, shell=True, text=True)


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
