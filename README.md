# wiros_data_collection
data collection context on RPi

1. need to install AWS CLI
2. aws configure
3. assign 
4. install boto3


# Data Collecting and Processing Support for WiROS

This repo contains scripts for collecting data from [WiROS](https://github.com/ucsdwcsng/WiROS) using AWS Services by BOTO3 Software Development Kit
[TODO: insert pipeline]

## Table of Contents

- [Imporatant Files](#important-files)
- [Configurations and Setup](#configurations-and-setup)

## Important Files:
1. [**`data_collection/_CONST.py`**](/data_collection/_CONST.py) - Configuration file to setup all parameters, including AWS credentials, DB names, data collector and reader configs, and etc. 
2. [**`data_collection/collector.py`**](/data_collection/collector.py) - Data collector using on monitoring devices. Listens to ROS topic `/csi` and upload data to dynamoDB and S3bucket. 
3. [**`data_collection/data_reader.py`**](/data_collection/data_reader.py) - Data reader containing methods to query, download and parse data to local. 

## Configurations and Setup

#### Step 1: Set Up the WiROS
To get started with WiROS, follow the instructions on [WiROS](https://github.com/ucsdwcsng/WiROS), especially the [README](https://github.com/ucsdwcsng/wiros_csi_node/blob/main/README.md) in the [CSI Node](https://github.com/ucsdwcsng/wiros_csi_node) to configure your hardware and local setup.   

#### Step 2: Configure AWS 

1. **Create an AWS Account**:

    If you don't already have an AWS account, create one by following the [AWS sign-up process](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

2. **hi**