
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
    DB_NAME = "wiros_csi"
    # AWS_ACCESS_KEY_ID = ""
    # AWS_SECRET_ACCESS_KEY = ""
    BUCKET_NAME = "wiros-csi"
    SERVER_AREA = "us-west-1"
    LOCAL_COPY = True
    PARTITION_KEY = "txmac"
    PARTITION_KEY_VALUE = "6a:79:7e:67:48:38"
    SORT_KEY = "time_stamp"
    SORT_KEY_LOWER_BOUND = 1725492679
    SORT_KEY_UPPER_BOUND = 1725492699
    DEVICE_NAME = "wiros_desktop"
    CSV_FOR_NEEDED_FILES = True
    DOWNLOAD_NEEDED_FILES = True
    BINARY_FILES_FOLDER = "binary_data"
