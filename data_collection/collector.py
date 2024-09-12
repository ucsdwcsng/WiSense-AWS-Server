import boto3 
import sys, rospy, time, struct, csv, botocore, os
from rf_msgs.msg import Wifi
# from std_msgs.msg import String
from _CONST import _Const
from botocore.config import Config

def mac_to_str(mactup):
   assert len(mactup) == 6, f"Invalid MAC tuple: {mactup}"
   return "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(mactup[0], mactup[1], mactup[2], mactup[3], mactup[4], mactup[5])

def convert_to_decimal(x):
    # Count the number of digits in the number
    num_digits = len(str(x))
    # Divide the number by 10 raised to the power of the number of digits
    result = x / (10 ** num_digits)
    return result

def callback(msg):

    global count, error_flag
    count += 1

    if error_flag:
        # rospy.signal_shutdown("error detected when collecting data")
        pass

    single_item = {
            # "seq": {'N':str(msg.header.seq)},
            "txmac": {'S' :mac_to_str(msg.txmac)},
            # "time_stamp":{'N':str(msg.header.stamp.secs) + str(msg.header.stamp.nsecs)},
            "time_stamp": {'N':str(msg.header.stamp.secs + msg.header.stamp.nsecs/10**9)},
            "msg_id": {'N' :str(msg.msg_id)}, 
            "rx_id": {'S' :msg.rx_id},  
            "ap_id": {'N': str(msg.ap_id)},
            "chan": {'N' :str(msg.chan)},
            "n_sub": {'N' :str(msg.n_sub)},
            "n_rows": {'N' :str(msg.n_rows)},
            "n_cols": {'N' :str(msg.n_cols)},
            "bw": {'N' :str(msg.bw)},
            "mcs": {'N' :str(msg.mcs)},
            "rssi":{'N' :str( msg.rssi)},
            "fc": {'N' :str(msg.fc)},
            "seq_num": {'N' :str(msg.seq_num)},
            "bucket_name": {'S': f"{CONST.BUCKET_NAME}"},
            "file_name": {'S': f"{file_name}"},
            "offset_in_file":{'N': str(count % CONST.ROW_PER_FILE)}

            # NO csi will be stored on DB!

            # "csi_real": real_list,
            # "csi_imag": imag_list
        }
    size = sys.getsizeof(msg)
    callback_table_put(single_item)
    write_file(msg.csi_real, msg.csi_imag)
    
def write_file(real_list,imag_list):
    global count, CONST, file_name, aws_config, uploading_file
    array = real_list + imag_list

    # Convert the array to a binary format
    binary_data = struct.pack('d' * len(array), *array)

    # Write the binary data to a file
    with open(f'binary_data/{file_name}', 'ab') as file:
        file.write(binary_data)

    if (count % CONST.ROW_PER_FILE == 0):
        s3 = boto3.client(
            's3',
            aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
            aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
            config = aws_config)
        print(f'uploading binary file {file_name}')
        s3.upload_file(f'binary_data/{file_name}', f'{CONST.BUCKET_NAME}', f'{file_name}', Callback= deleter_on_callback)
        with open("/home/wcsng/s3_upload_log.txt", "a") as f:
            f.write(f"Uploaded 100 packets at {time.time()}\n")
        uploading_file = f'binary_data/{file_name}'
        file_name = str(time.time()) + CONST.DEVICE_NAME
    # print(f"." , end = "")

def deleter_on_callback(uploaded_bytes):
    global upload_size, uploading_file
    file_size = os.path.getsize(f'binary_data/{file_name}')

    upload_size += uploaded_bytes
    if (upload_size == file_size):
        upload_size = 0
        if (CONST.LOCAL_COPY):
            print(f'binary file {file_name} uploaded and kept')
        else:
            os.remove(f'binary_data/{file_name}')
            print(f'binary file {file_name} uploaded and removed')

def callback_table_put(item):
    global item_batch, count, CONST, file_name, error_flag, aws_config
    # table = dynamodb.Table('DB_test_2')
    # item_batch['RequestItems'][0]['DB_test_2'].append({'PutRequest':item})
    item_batch[f'{CONST.DB_NAME}'].append({'PutRequest':{"Item":item}})

    # upload every MAX_BATCH_ELEMENT_COUNT elements
    if (count % CONST.MAX_BATCH_ELEMENT_COUNT == 0):
        client = boto3.client(
            'dynamodb',
            aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
            aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
            config = aws_config
        )
        # response = client.batch_write_item(RequestItems = item_batch)
        # item_batch[f'{CONST.DB_NAME}'].clear()
        try: 
            response = client.batch_write_item(RequestItems = item_batch)
            item_batch[f'{CONST.DB_NAME}'].clear()
            print(f"\na new request batch uploaded, total requests: {count}")
            # print(response)
        except Exception as e:
            print(e)
            rospy.signal_shutdown("error detected when collecting data")
            raise


def listener():
    rospy.init_node('test_listener', anonymous=True)

    json_obj=rospy.Subscriber(CONST.ROS_TOPIC, Wifi, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    # initialize 
    
    CONST = _Const(os)
    print("AWS_ACCESS_KEY_ID: " + CONST.AWS_ACCESS_KEY_ID)
    print("AWS_SECRET_ACCESS_KEY: " + CONST.AWS_SECRET_ACCESS_KEY)
    print("DB: " + CONST.DB_NAME)
    file_size, upload_size, count = 0, 0 ,0
    error_flag = False
    uploading_file = None
    item_batch = {
        f'{CONST.DB_NAME}': []
    }
    aws_config = Config(
        region_name = f'{CONST.SERVER_AREA}',

        # signature_version = 'v4',
        # retries = {
        #     'max_attempts': 10,
        #     'mode': 'standard'
        # }
    )   
    file_name = str(time.time()) + CONST.DEVICE_NAME
    listener()






