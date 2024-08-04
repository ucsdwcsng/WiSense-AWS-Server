from boto3.dynamodb.conditions import Key, Attr
import boto3, os, csv
# import sys, rospy, time, struct, csv, botocore
from rf_msgs.msg import Wifi
# from std_msgs.msg import String
from _CONST import _Const
from botocore.config import Config
from datetime import datetime

def write_csv(items):

    # Specify the file name
    # f = open(f"{csv_creation_time}.csv", "x")
    # Write data to the CSV file with a pipe delimiter
    with open(f"csi_data_from {CONST.START_TIME_FRAME}_to_{CONST.END_TIME_FRAME}.csv", 'w', newline='') as csvfile:
        fieldnames = list(items[0].keys())
        csvwriter = csv.DictWriter(csvfile, delimiter=',',fieldnames = fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(items)

def get_DB_items():
    aws_config = Config(
        region_name = f'{CONST.SERVER_AREA}'
    )   
    # dynamodb = boto3.resource('dynamodb')
    dynamodb = boto3.resource(
        'dynamodb',
        config = aws_config,
        aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
        aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
         )

    table = dynamodb.Table(f'{CONST.DB_NAME}')
    response = table.query(
        KeyConditionExpression=Key(f'{CONST.PARTITION_KEY}').eq(f"{CONST.PARTITION_KEY_VALUE}")
    )
    # response = table.scan(
    #     FilterExpression=Attr('time_stamp').between(1722031098782215703, 1722042193379421040)
    # )

    return response

if __name__ == '__main__':
    # initialize 
    
    CONST = _Const(os)
    print(CONST.AWS_ACCESS_KEY_ID, CONST.AWS_SECRET_ACCESS_KEY)
    # file_size, upload_size, count = 0, 0 ,0
    # error_flag = False
    # uploading_file = None
    print(CONST.DB_NAME)
    # item_batch = {
    #     f'{CONST.DB_NAME}': []
    # }
    response = get_DB_items()
    items = response['Items']
    write_csv(items)
    response.pop('Items')
    print(response)