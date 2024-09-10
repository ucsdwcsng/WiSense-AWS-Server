#!/bin/bash

# Source .bashrc to load environment variables and settings
source ~/.bashrc

aws configure

# download CA cert
mkdir -p ~/certs/pubsub
curl -o ~/certs/AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
chmod 745 ~
chmod 700 ~/certs
chmod 644 ~/certs/AmazonRootCA1.pem
ls -l ~/certs


output=$(aws iot create-keys-and-certificate \
--set-as-active \
--certificate-pem-outfile "~/certs/pubsub/device.pem.crt" \
--public-key-outfile "~/certs/pubsub/public.pem.key" \
--private-key-outfile "~/certs/pubsub/private.pem.key")

certificateArn=$(echo "$output" | jq -r '.certificateArn')
echo $certificateArn

chmod 700 ~/certs/pubsub
chmod 644 ~/certs/pubsub/*
chmod 600 ~/certs/pubsub/private.pem.key

ls -l ~/certs/pubsub

mkdir ~/.aws-iot-device-client
mkdir ~/.aws-iot-device-client/log
chmod 745 ~/.aws-iot-device-client/log
echo " " > ~/.aws-iot-device-client/log/aws-iot-device-client.log
echo " " > ~/.aws-iot-device-client/log/pubsub_rx_msgs.log
chmod 600 ~/.aws-iot-device-client/log/*

output=$(aws iot describe-endpoint --endpoint-type IoT:Data-ATS)

endpointAddress=$(echo "$output" | jq -r '.endpointAddress')
echo endpointAddress: $endpointAddress
echo "Please enter your new thing name:"
read thingName

aws iot create-thing --thing-name $thingName
# TODO: complete the policy

echo $certificateArn
echo $thingName

aws iot attach-policy --policy-name wiros_MQTT_console  --target $certificateArn
aws iot attach-thing-principal --thing-name $thingName --principal $certificateArn
export endpointAddress=$endpointAddress
export thingName=$thingName
export certificateArn=$certificateArn

# Create the JSON file
jq -n \
  --arg endpointAddress "$endpointAddress" \
  --arg thingName "$thingName" \
  --arg certificateArn "$certificateArn" \
  '{
    endpointAddress: $endpointAddress,
    thingName: $thingName,
    certificateArn: $certificateArn
  }' > MQTT_param.json




