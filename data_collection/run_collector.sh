#!/bin/bash

# Define the AWS_ACCESS_KEY_ID variable
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_key"
DB_NAME="you_dynamoDB_name"

# Export the variable so it is available to the Python script
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

# Run the Python script
python3 collector.py