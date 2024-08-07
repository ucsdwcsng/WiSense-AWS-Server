from boto3.dynamodb.conditions import Key, Attr
import boto3, os, csv, botocore, sys, struct
# import rospy, time, struct, 
from rf_msgs.msg import Wifi
# from std_msgs.msg import String
from _CONST import _Const
from botocore.config import Config
from datetime import datetime

def write_csv(items):

    # Write data to the CSV file 
    with open(f"csi_data_from {CONST.SORT_KEY_LOWER_BOUND}_to_{CONST.SORT_KEY_UPPER_BOUND}.csv", 'w', newline='') as csvfile:
        fieldnames = list(items[0].keys())
        csvwriter = csv.DictWriter(csvfile, delimiter=',',fieldnames = fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(items)

def get_DB_items():
    aws_config = Config(
        region_name = f'{CONST.SERVER_AREA}'
    )   
    dynamodb = boto3.resource(
        'dynamodb',
        config = aws_config,
        aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
        aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
         )

    table = dynamodb.Table(f'{CONST.DB_NAME}')
    response = table.query(
        KeyConditionExpression=Key(f'{CONST.PARTITION_KEY}').eq(f"{CONST.PARTITION_KEY_VALUE}") 
                                & Key(f'{CONST.SORT_KEY}').between(CONST.SORT_KEY_LOWER_BOUND, CONST.SORT_KEY_UPPER_BOUND)
    )

    return response

def create_file_list(items):
    # Mapping every file to the corresponding S3 bucket
    binary_files_dict = {}
    for entry in items:
        file_name = entry['file_name']
        if file_name not in binary_files_dict:
            binary_files_dict[file_name] = entry['bucket_name']

    if (CONST.CSV_FOR_NEEDED_FILES):
        # Create a CSV file of file names and S3 bucket names of needed binary files from query data
        with open('needed_binary_files.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['file_name', 'bucket_name'])
            # Write each file name and corresponding S3 bucket name to the CSV
            for file_name, bucket_name in binary_files_dict.items():
                writer.writerow([file_name, bucket_name])

    return binary_files_dict

# download to target folder and return a list of DNE files
def download_needed_files(binary_files_dict):
    # configure AWS s3
    aws_config = Config(
        region_name = f'{CONST.SERVER_AREA}'
    )   
    s3 = boto3.client(
        's3',
        config = aws_config,
        aws_access_key_id = f"{CONST.AWS_ACCESS_KEY_ID}",
        aws_secret_access_key =  f"{CONST.AWS_SECRET_ACCESS_KEY}",
    )

    # Get a list of all entries in the binary_data
    directory_path = CONST.BINARY_FILES_FOLDER
    entries = os.listdir(directory_path)
    file_names = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
    DNE_files = []
    print("The following files exist, ignoring...")
    print(file_names)
    for binary_file in list(binary_files_dict.keys()):
        if (binary_file not in file_names):
            try:
                # check if bucket exists
                bucket_name = binary_files_dict[binary_file]
                response = s3.head_object(Bucket = bucket_name, Key = binary_file)

                print(f'downloading file {binary_file}')
                s3.download_file(bucket_name, binary_file, Filename = f'binary_data/{binary_file}')
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    print(f"The file with key '{binary_file}' does not exist in the bucket '{bucket_name}'.")
                    DNE_files.append(binary_file)
                else:
                    # Handle other exceptions as needed
                    print(f"An error occurred: {e}")
                    raise
    print(f"\ndownloading complete.\nfiles not found:\n {str(DNE_files)}")
    return DNE_files

# takes a binary file and return a float array
def read_floats_from_file(filename):
    floats = []
    with open(str(f'{CONST.BINARY_FILES_FOLDER}/{filename}'), 'rb') as file:
        binary_data = file.read()
        num_floats = len(binary_data) // struct.calcsize('d')
        array = list(struct.unpack('d' * num_floats, binary_data))
    return array

# if required binary file is not downloaded, csi in entries will be None
def add_csi_to_entries(entries_list):
    for entry in entries_list:
        file_name = entry['file_name']
        offset = int(entry['offset_in_file'])
        # ignore if no such a binary file
        dirs = os.listdir(CONST.BINARY_FILES_FOLDER)
        existed_files = [entry for entry in dirs if os.path.isfile(os.path.join(CONST.BINARY_FILES_FOLDER, entry))]
        if file_name in existed_files:
            csi_real_imag = read_floats_from_file(file_name)[offset* CONST.COL_PER_ROW:(offset+1)* CONST.COL_PER_ROW]
            entry['csi_real'] = csi_real_imag[0:int(CONST.COL_PER_ROW/2)]
            entry['csi_imag'] = csi_real_imag[int(CONST.COL_PER_ROW/2) :-1]
            print(f"inserted to entry: {entry[CONST.PARTITION_KEY]}, {entry[CONST.SORT_KEY]}")
        else:
            entry['csi_imag'],entry['csi_real'] = None, None
    return entries_list 

if __name__ == '__main__':
    # initialize 
    
    CONST = _Const(os)
    print("AWS_ACCESS_KEY_ID: " + CONST.AWS_ACCESS_KEY_ID)
    print("AWS_SECRET_ACCESS_KEY: " + CONST.AWS_SECRET_ACCESS_KEY)
    print("DB: " + CONST.DB_NAME +f'\n')

    response = get_DB_items()
    # items are a list of queried entires from DB, where entires are dicts
    items = response['Items']
    if (len(items) <= 0):
        print("no items found")
        sys.exit(0)
    write_csv(items)
    binary_files_dict = create_file_list(items)
    if (CONST.DOWNLOAD_NEEDED_FILES):
        download_needed_files(binary_files_dict)
    items = add_csi_to_entries(items)
    for each in items:
        print(each, end=f'\n\n\n\n')
    print(f'{len(items)} items found, ')

    
    # response.pop('Items')
    # print(response)