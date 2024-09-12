# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys, os, json, signal
import threading
import time
# from utils.command_line_utils import CommandLineUtils
import wiros_subprocess 
import xml.etree.ElementTree as ET

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
# cmdData = CommandLineUtils.parse_sample_input_pubsub()

received_count = 0
received_all_event = threading.Event()
json_cmd = {}
new_cmd = False
 
class Processes():
    def __init__(self):
        # self.roscore_process = None
        self.wiros_process = None
        self.launch_file = os.getenv('launchFilePath')  
        self.status_map={
            'deviceId':os.getenv('thingName'),
            'wiros': 0,
            'count':0
        }
        tree = ET.parse(self.launch_file)
        root = tree.getroot()
        self.roscore_process = wiros_subprocess.start_roscore()

        for param in root.findall(".//param"):
            self.status_map[param.get('name')]=param.get('value')

    # Function to find and modify a param in the launch file
    def modify_param(self, param_name, new_value):
        tree = ET.parse(self.launch_file)
        root = tree.getroot()
        # Find the param element with the specified name
        for param in root.findall(".//param"):
            if param.get('name') == param_name:
                oldVal = param.get('value')
                # Modify the attribute
                param.set('value', str(new_value))
                tree.write(self.launch_file)
                self.update_status()
                return oldVal
        # if DNE
        return None
        
    def update_status(self):
        tree = ET.parse(self.launch_file)
        root = tree.getroot()
        for param in root.findall(".//param"):
            self.status_map[param.get('name')]=param.get('value')

    def start_wiros(self):
        # self.roscore_process = wiros_subprocess.start_roscore()
        # self.roscore_process.wait()
        self.wiros_process = wiros_subprocess.run_ros_launch(self.launch_file)
        self.status_map['wiros'] = 1
        print(f'Successfully started')


    def stop_wiros(self):
        # Retrieve the PID of the terminal and terminate
        pgid = os.getpgid(self.wiros_process.pid)
        os.killpg(pgid, signal.SIGINT)


        self.wiros_process.wait()  
        # self.roscore_process.wait()  
        print("roscore and wiros has been terminated.")
        self.status_map['wiros'] = 0

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    global received_count, status_map, json_cmd, new_cmd, process_console
    print("Received message from topic '{}': {}".format(topic, payload))
    json_string = payload.decode('utf-8')
    json_cmd = json.loads(json_string)
    received_count += 1
    new_cmd = True

def cmd_parser(json_cmd):
    
    if "stop_wiros" in json_cmd and json_cmd["stop_wiros"] == 1:
        if process_console.status_map["wiros"] == 1:
            print('stopping wiros...')
            process_console.stop_wiros()
        else:
            print('already stopped')

    if "start_wiros" in json_cmd and json_cmd["start_wiros"] == 1:
        if process_console.status_map["wiros"] == 0:
            print('starting wiros...')
            process_console.start_wiros()
        else:
            print('already started')

    if "change_params" in json_cmd:
        if process_console.status_map['wiros'] == 0:
            paramsToChange = json_cmd['change_params']
            for param in paramsToChange.keys():
                process_console.modify_param(param, paramsToChange[param])
        else: 
            message_json = {
                'deviceId':os.getenv('thingName'),
                'warning_msg': 'cannot change param while wiros is running'
            }
            mqtt_connection.publish(
            topic=os.getenv('MQTT_topic'),
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)

    if "status" in json_cmd and json_cmd["status"] == 1:
        message_json = json.dumps(process_console.status_map)
        mqtt_connection.publish(
            topic=os.getenv('MQTT_topic'),
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)






# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))

# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):
    print("Connection closed")

if __name__ == '__main__':
    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    # Parse the launch file

    process_console = Processes()
    # if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
    #     proxy_options = http.HttpProxyOptions(
    #         host_name=cmdData.input_proxy_host,
    #         port=cmdData.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=os.getenv("endpointAddress"),
        # port=cmdData.input_port,
        # cert_filepath=cmdData.input_cert,
        cert_filepath=os.path.expanduser('~/certs/pubsub/device.pem.crt'),
        pri_key_filepath=os.path.expanduser("~/certs/pubsub/private.pem.key"),
        ca_filepath=os.path.expanduser("~/certs/AmazonRootCA1.pem"),
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=os.getenv("thingName"),
        # client_id="basicPubSub",
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed)
    print(f"Connecting to {os.getenv('endpointAddress')} with client ID '{os.getenv('thingName')}'...")



    # if not cmdData.input_is_ci:
    #     print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    # else:
    #     print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # message_count = cmdData.input_count
    message_topic = os.getenv('MQTT_topic')
    # message_string = cmdData.input_message

    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    


    # constantly check for new cmds
    while (1):
        try:
            if (new_cmd):
                cmd_parser(json_cmd)
                print("cmd handled")
                new_cmd=False
            else:
                print("no message yet.")
            
            time.sleep(3)
        except KeyboardInterrupt as e:
            print(e)
            mqtt_connection.disconnect()
            sys.exit()
        
        except Exception as e:
            print(e)
            mqtt_connection.disconnect()
            sys.exit()

    # subscribe_result = subscribe_future.result()
    # print("Subscribed with {}".format(str(subscribe_result['qos'])))

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    # if message_string:

    #     # Sending messages until program killed
    #     publish_count = 1
    #     while (publish_count <= message_count) or (message_count == 0):
    #         message_string = input()
    #         message = "{} [{}]".format(message_string, publish_count)
    #         print("Publishing message to topic '{}': {}".format(message_topic, message))
    #         message_json = json.dumps(message)
    #         mqtt_connection.publish(
    #             topic=message_topic,
    #             payload=message_json,
    #             qos=mqtt.QoS.AT_LEAST_ONCE)
    #         # time.sleep(1)
    #         publish_count += 1

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    if message_count != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")


    received_all_event.wait()
    print("{} message(s) received.".format(received_count))

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")