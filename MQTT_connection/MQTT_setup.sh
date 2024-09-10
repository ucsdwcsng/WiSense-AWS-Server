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
echo "Please enter your new thing name (will also be used as clientID):"
read thingName

aws iot create-thing --thing-name $thingName
# TODO: complete the policy

echo "CertificateArn: $certificateArn"
echo "ThingName and clientID: $thingName"

echo "Please enter your desired topic:"
read topic

# Create the new thing
aws iot create-thing --thing-name $thingName



# Extract region and account ID from the certificateArn
region=$(echo "$certificateArn" | cut -d: -f4)
accountId=$(echo "$certificateArn" | cut -d: -f5)

# Define a sample policy and replace placeholders with user inputs
policy=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Receive",
        "iot:PublishRetain"
      ],
      "Resource": [
        "arn:aws:iot:$region:$accountId:topic/$topic"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": [
      "arn:aws:iot:$region:$accountId:topicfilter/$topic"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": [
      "arn:aws:iot:$region:$accountId:client/$thingName"
      ]
    }
  ]
}
EOF
)

policyName="$thingName-Policy"
# Save the policy to a file
echo "$policy" > ./$policyName.json
echo "New policy created: ./$policyName.json"

# Create the policy in AWS IoT
aws iot create-policy --policy-name $policyName --policy-document file://./$policyName.json


aws iot attach-policy --policy-name $policyName  --target $certificateArn
aws iot attach-thing-principal --thing-name $thingName --principal $certificateArn
export endpointAddress=$endpointAddress
export thingName=$thingName
export certificateArn=$certificateArn
export certificateArn=$topic

# Create the JSON file
jq -n \
  --arg endpointAddress "$endpointAddress" \
  --arg thingName "$thingName" \
  --arg certificateArn "$certificateArn" \
  --arg topic "$topic" \
  '{
    endpointAddress: $endpointAddress,
    thingName: $thingName,
    certificateArn: $certificateArn,
    topic: $topic
  }' > MQTT_param.json




