from boto3.dynamodb.conditions import Key, Attr
import boto3, os
# import sys, rospy, time, struct, csv, botocore
from rf_msgs.msg import Wifi
# from std_msgs.msg import String
from _CONST import _Const
from botocore.config import Config



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
    # response = table.query(
    #     KeyConditionExpression=Key('time_stamp').eq(1722031098792215803)
    # )
    response = table.scan(
        FilterExpression=Attr('time_stamp').between(1722031098782215703, 1722042193379421040)
    )
    items = response['Items']
    print(items)