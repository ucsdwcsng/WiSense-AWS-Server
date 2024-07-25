
class _Const:
    def __init__(self,access_key,secret_key):
        self.AWS_ACCESS_KEY_ID = f"{access_key}"
        self.AWS_SECRET_ACCESS_KEY = f"{secret_key}"

    MAX_BATCH_ELEMENT_COUNT = 25
    COL_PER_ROW = 2048
    ROW_PER_FILE = 10000
    DB_NAME = "data_on_07_19"
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    # MAX_THROTTLING_ERROR_TOLERANCE = 10
