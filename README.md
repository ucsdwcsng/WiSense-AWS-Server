# Data Collecting and Processing Support for WiROS

This repo contains scripts for collecting data from [WiROS](https://github.com/ucsdwcsng/WiROS) using AWS Services by BOTO3 Software Development Kit
![TODO: insert pipeline](/media/data_pipeline.png)

## Table of Contents

- [Imporatant Files](#important-files)
- [Configurations and Setup](#configurations-and-setup)
    - [AWS Account](#step-2-configure-aws)
    - [AWS DynamoDB](#step-3-configure-aws-dynamodb)
    - [AWS S3](#step-4-configure-aws-s3)
    - [AWS Users](#step-5-configure-aws-users)
    - [Data Collector and Processor Setup](#step-6-setup-and-configure-data-collector)
- [Usage Examples](#usage-examples)

## Important Files:
1. [**`data_collection/_CONST.py`**](/data_collection/_CONST.py) - Configuration file to setup all parameters, including AWS credentials, DB names, data collector and reader configs, and etc. 
2. [**`data_collection/collector.py`**](/data_collection/collector.py) - Data collector using on monitoring devices. Listens to ROS topic `/csi` and upload data to dynamoDB and S3bucket. 
3. [**`data_collection/data_reader.py`**](/data_collection/data_reader.py) - Data reader containing methods to query, download and parse data to local. 

## Configurations and Setup

#### Step 1: Set Up the WiROS
To get started with WiROS, follow the instructions on [WiROS](https://github.com/ucsdwcsng/WiROS), especially the [README](https://github.com/ucsdwcsng/wiros_csi_node/blob/main/README.md) in the [CSI Node](https://github.com/ucsdwcsng/wiros_csi_node) to configure your hardware and local setup.   



#### Step 2: Configure AWS 

1. **Create an AWS Account**:

- If you don't already have an AWS account, create one by following the [AWS sign-up process](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

2. **Login and Select Your Server Region**

- Interface options are on the top right corner of AWS console page.

#### Step 3: Configure AWS DynamoDB
    
1. Go to AWS Service ---> DynamoDB ---> Tables ---> Create Table


2. Configure the table with the following parameters
- Table name = your_table_name
- Partition key = txmac (string) 
- Sort Key = time_stamp (number)
- Customize settings ---> Read/write capacity settings ---> On-demand
    - maximum read >= 100 
    - maximum write >= 100 * number_of_devices 
    - **Note:** upscale these two if throughput limit reaches, remember to monitor your cost! 
- Modify other settings if needed
3. Create Table

##### [DynamoDb Price Info](https://aws.amazon.com/dynamodb/pricing/on-demand/)

#### Step 4: Configure AWS S3 

1. Go to AWS Service ---> S3 ---> Buckets ---> Create Bucket 

2. Table name = your_table_name

2. Create bucket with default settings (change configs if needed)

#### Step 5: Configure AWS Users 

1. Go to AWS Service ---> IAM ---> User Groups ---> Create Group

2. Configure the table with the following parameters
- Group name = your_group_name
- Attach permissions policies
    - Search and tick `AmazonS3FullAccess` and `AmazonDynamoDBFullAccess`

3. Create users
- For every data collector (e.g. RPi), create a new user 
- User name = your_deivce_name
- Add user to group
    - tick group `your_group_name` you just created
- Go to users detail page by directly clicking the `user name`
    - In the summary section, click `Create access key`
    - Choose use case `Local code` and tick 
*"I understand the above recommendation and want to proceed to create an access key."*
    - Skip the tag section unless needed
- Click `Create access key`, keep this key by other download the `.csv` file or copy to your document for later access. 




#### Step 6: Setup and Configure Data Collector

1. **Clone this repo on your device for data collection**:

    `git clone https://github.com/ucsdwcsng/wiros_data_collection.git`

2. Go to the data_collection folder 

- `cd wiros_data_collection/data_collection/`

3. Edit `_CONST.py`

- Modify these fields to the previous set values
    - tip: you can find your server area code by where you select your server area 
    
       (e.g. `US West (N. California) us-west-1`)
``` 
DB_NAME = "your db name"
AWS_ACCESS_KEY_ID = "your access key"
AWS_SECRET_ACCESS_KEY = "your secret key"
BUCKET_NAME = "your bucket name"
SERVER_AREA = "your server area"
```

## Usage Examples

### Collecting CSI and upload to the cloud

1. Launch a CSI tool that will publish CSI messages on ROS topic `/csi`

- e.g.

    ```
    cd YOUR_WIROS_FOLDER/src/wiros_csi_node/launch/
    
    roslaunch basic.launch
    ```

2. Go to `data_collection` folder

    ```
    cd YOUR_COLLECTOR_FOLDER/wiros_data_collection/data_collection
    chmod +x ./run_collector.sh
    ./run_collector.sh
    ```

- If running first time, the bash script will install `boto3`, which is required for the collector


### Querying data from the cloud

1. Repeat the first step here [to start WiROS](#collecting-csi-and-upload-to-the-cloud)

2. Go to `data_collection` folder

    ```
    cd YOUR_COLLECTOR_FOLDER/wiros_data_collection/data_collection
    ```
3. modify the following fields of your `_CONST.py`

    ```
    PARTITION_KEY_VALUE = "mac_addr_of_your_target_device(e.g. 5e:3e:12:f4:3a:36)"
    SORT_KEY_UPPER_BOUND = 1722981112 
    SORT_KEY_UPPER_BOUND = 1722981152
    DEVICE_NAME = "test"
    CSV_FOR_NEEDED_FILES = True
    DOWNLOAD_NEEDED_FILES = True
    ```
- Modify `SORT_KEY_UPPER_BOUND` and `SORT_KEY_UPPER_BOUND` to change the query range
- Tip: use time_stamp converter tools or APIs to translate to and from time_stamp to human-readable date. (e.g. [Epoch Converter](https://www.epochconverter.com/)) 

4. Run the example CSI visualizer

    ```
    chmod +x ./run_reader.sh
    ./run_reader.sh
    ```


# TODO: MQTT console

1. get a user with `AWSIoTConfigAccess` permission
2. run the env set secrete access and access