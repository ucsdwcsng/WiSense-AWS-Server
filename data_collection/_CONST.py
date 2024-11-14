
class _Const:
    def __init__(self,os):
        pass
        self.AWS_ACCESS_KEY_ID = f"{os.getenv('AWS_ACCESS_KEY_ID')}"
        self.AWS_SECRET_ACCESS_KEY = f"{os.getenv('AWS_SECRET_ACCESS_KEY')}"
        # self.DEVICE_NAME =  f"{os.getenv('AWS_SECRET_ACCESS_KEY')}"
    #     self.DB_NAME = f"{os.getenv('DB_NAME')}"
    #     self.BUCKET_NAME = f"{os.getenv('BUCKET_NAME')}"
    #     self.SERVER_AREA = f"{os.getenv('SERVER_AREA')}"
    #     self.ROW_PER_FILE = int(f"{os.getenv('ROW_PER_FILE')}")
    #     self.LOCAL_COPY = bool(int(f"{os.getenv('LOCAL_COPY')}"))

    MAX_BATCH_ELEMENT_COUNT = 25
    ROS_TOPIC = "csi_server/csi"
    COL_PER_ROW = 2048
    ROW_PER_FILE = 1000
    DB_NAME = "wiros_csi"
    BUCKET_NAME = "wiros-csi"
    SERVER_AREA = "us-west-1"
    LOCAL_COPY = True
    PARTITION_KEY = "txmac"
    PARTITION_KEY_VALUE = "ac:37:43:de:62:e7"
    SORT_KEY = "time_stamp"
    SORT_KEY_LOWER_BOUND = 1731544658
    SORT_KEY_UPPER_BOUND = 1731544678
    DEVICE_NAME = "wiros_desktop1"
    CSV_FOR_NEEDED_FILES = True
    DOWNLOAD_NEEDED_FILES = False
    BINARY_FILES_FOLDER = "binary_data"
        
    # Don't use these to input keys! Your keys should be setup in MQTT_setup.sh
    # AWS_ACCESS_KEY_ID = ""
    # AWS_SECRET_ACCESS_KEY = ""
