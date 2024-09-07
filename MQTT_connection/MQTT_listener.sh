set -e


# Read values from MQTT_param.json
endpointAddress=$(jq -r '.endpointAddress' MQTT_param.json)
thingName=$(jq -r '.thingName' MQTT_param.json)
certificateArn=$(jq -r '.certificateArn' MQTT_param.json)

# Export as environment variables
export endpointAddress
export thingName
export certificateArn
export MQTT_topic='sdk/test/js'
export launchFilePath='"/home/wcsng/van_wiros/src/wiros_csi_node/launch/basic.launch"'
# Print the values to verify (optional)
echo "Endpoint Address: $endpointAddress"
echo "Thing Name: $thingName"
echo "Certificate ARN: $certificateArn"

# Run listening program
python3 console_rx.py