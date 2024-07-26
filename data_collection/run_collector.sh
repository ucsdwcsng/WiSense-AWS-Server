#!/bin/bash

# Check if boto3 is installed
if ! python3 -c "import boto3" &> /dev/null; then
    echo "boto3 is not installed. Installing..."
    pip3 install boto3
else
    echo "boto3 is working"
fi

# Define the AWS_ACCESS_KEY_ID variable
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_key"
DB_NAME="you_dynamoDB_name"
BUCKET_NAME=""
SERVER_AREA="us-west-1"

# Export the variable so it is available to the Python script
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

# Run the Python script
python3 collector.py