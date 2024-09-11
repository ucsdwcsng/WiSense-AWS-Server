set -e


# Read values from MQTT_param.json
endpointAddress=$(jq -r '.endpointAddress' MQTT_param.json)
thingName=$(jq -r '.thingName' MQTT_param.json)
certificateArn=$(jq -r '.certificateArn' MQTT_param.json)
topic=$(jq -r '.topic' MQTT_param.json)

# Export as environment variables
export endpointAddress
export thingName
export certificateArn
export MQTT_topic=$topic
export launchFilePath='root/wiros/src/wiros_csi_node/launch/basic.launch'

# Print the values to verify (optional)
echo "Endpoint Address: $endpointAddress"
echo "Thing Name and clientID: $thingName"
echo "Certificate ARN: $certificateArn"
echo "Topic: $topic"

# Run listening program
python3 console_rx.py