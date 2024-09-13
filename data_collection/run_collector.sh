#!/bin/bash

# Check if boto3 is installed
if ! python3 -c "import boto3" &> /dev/null; then
    echo "boto3 is not installed. Installing..."
    pip3 install boto3
else
    echo "boto3 is working"
fi

# Run the Python script

mkdir -p binary_data
AWS_ACCESS_KEY_ID=$(aws configure get default.aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get default.aws_secret_access_key)

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

python3 collector.py