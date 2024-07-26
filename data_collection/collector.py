import boto3 
import sys, rospy, time, struct, csv, botocore, os
from rf_msgs.msg import Wifi
from std_msgs.msg import String
from decimal import *
from _CONST import _Const

def mac_to_str(mactup):
   assert len(mactup) == 6, f"Invalid MAC tuple: {mactup}"
   return "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(mactup[0], mactup[1], mactup[2], mactup[3], mactup[4], mactup[5])

def callback(msg):

    global count, total_size, error_flag
    count += 1

    # # conver types from float to Decimal
    # real_list = tuple([Decimal(each) for each in msg.csi_real])
    # imag_list = tuple([Decimal(each) for each in msg.csi_imag])

    if error_flag:
        print("error detected")
        exit(1) 

    single_item = {
            "seq": {'N':str(msg.header.seq)},
            "time_stamp":{'N':str(msg.header.stamp.secs) + str(msg.header.stamp.nsecs)},
            "msg_id": {'N' :str(msg.msg_id)}, 
            "rx_id": {'S' :msg.rx_id},  
            "ap_id": {'N': str(msg.ap_id)},
            "txmac": {'S' :mac_to_str(msg.txmac)},
            "chan": {'N' :str(msg.chan)},
            "n_sub": {'N' :str(msg.n_sub)},
            "n_rows": {'N' :str(msg.n_rows)},
            "n_cols": {'N' :str(msg.n_cols)},
            "bw": {'N' :str(msg.bw)},
            "mcs": {'N' :str(msg.mcs)},
            "rssi":{'N' :str( msg.rssi)},
            "fc": {'N' :str(msg.fc)},
            "seq_num": {'N' :str(msg.seq_num)},
            "bucket_name": {'S': f"{CONST.BUCKET_NAME}"}
            "file_name": {'S': f"{file_name}"},
            "offset_in_file":{'N': str(count % CONST.ROW_PER_FILE)}

            # NO csi will be stored on DB!

            # "csi_real": real_list,
            # "csi_imag": imag_list
        }
    
    size = sys.getsizeof(msg)
    total_size += size

    # print('count = ' + str(count) +  ' item seq ' + str(msg.seq_num)+ ' inserted to request batch' )

    callback_table_put(single_item)
    write_file(msg.csi_real, msg.csi_imag)
    
def write_file(real_list,imag_list):
    global count, CONST, file_name
    array = real_list + imag_list

    # Convert the array to a binary format
    binary_data = struct.pack('d' * len(array), *array)

    # Write the binary data to a file
    with open(f'binary_data/{file_name}', 'ab') as file:
        file.write(binary_data)

    if (count % CONST.ROW_PER_FILE == 0):
        file_name = time.time()
    print(".",end = " ")


def callback_table_put(item):
    global item_batch, count, CONST, file_name, error_flag
    # table = dynamodb.Table('DB_test_2')
    # item_batch['RequestItems'][0]['DB_test_2'].append({'PutRequest':item})
    item_batch[f'{CONST.DB_NAME}'].append({'PutRequest':{"Item":item}})

    # upload every MAX_BATCH_ELEMENT_COUNT elements
    if (count % CONST.MAX_BATCH_ELEMENT_COUNT == 0):
        client = boto3.client(
            'dynamodb',
            aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
            aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
        )
        try: 
            response = client.batch_write_item(RequestItems = item_batch)
            print("\nrequest batch uploaded")
            item_batch[f'{CONST.DB_NAME}'].clear()
            print(response)
        except client.exceptions.LimitExceededException as error:
            print('API call limit exceeded!')
            raise
        # except botocore.exceptions.ClientError as error:
        #     print(error.response)
        #     raise
        # except client.exceptions.ThrottlingException as error:
        #     print(error.response)
        #     raise
        # except ThrottlingException:
        #     print("throttling")
        # except ValidationException:
        #     print("validation")

def listener():


    rospy.init_node('test_listener', anonymous=True)

    json_obj=rospy.Subscriber("/csi", Wifi, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    # initialize 
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    CONST = _Const(os)
    print(CONST.AWS_ACCESS_KEY_ID, CONST.AWS_SECRET_ACCESS_KEY)
    count = 0
    total_size = 0
    error_flag = False
    item_batch = {
        f'{CONST.DB_NAME}': []
    }
    file_name = time.time()
    listener()






