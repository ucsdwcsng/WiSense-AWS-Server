
class _Const:
    def __init__(self,os):
        pass
        self.AWS_ACCESS_KEY_ID = f"{os.getenv('AWS_ACCESS_KEY_ID')}"
        self.AWS_SECRET_ACCESS_KEY = f"{os.getenv('AWS_SECRET_ACCESS_KEY')}"
    #     self.DB_NAME = f"{os.getenv('DB_NAME')}"
    #     self.BUCKET_NAME = f"{os.getenv('BUCKET_NAME')}"
    #     self.SERVER_AREA = f"{os.getenv('SERVER_AREA')}"
    #     self.ROW_PER_FILE = int(f"{os.getenv('ROW_PER_FILE')}")
    #     self.LOCAL_COPY = bool(int(f"{os.getenv('LOCAL_COPY')}"))

    MAX_BATCH_ELEMENT_COUNT = 25
    ROS_TOPIC = "csi_server/csi"
    COL_PER_ROW = 2048
    ROW_PER_FILE = 100
    DB_NAME = "your db name"
    AWS_ACCESS_KEY_ID = "your access key"
    AWS_SECRET_ACCESS_KEY = "your secret key"
    BUCKET_NAME = "your bucket name"
    SERVER_AREA = "your server area"
    LOCAL_COPY = False
    PARTITION_KEY = "txmac" 
    PARTITION_KEY_VALUE = "ac:37:43:de:62:e7"
    SORT_KEY = "time_stamp"
    SORT_KEY_LOWER_BOUND = 1722690344
    SORT_KEY_UPPER_BOUND = 1722727344
    DEVICE_NAME = "you_device_name(to avoid naming conflict)"
    CSV_FOR_NEEDED_FILES = True
    DOWNLOAD_NEEDED_FILES = True
    BINARY_FILES_FOLDER = "binary_data"


