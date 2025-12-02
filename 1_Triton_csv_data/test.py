# from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES, get_bit_number

# error_columns_details = ERROR_TABLE.get("columns", {})
# print("Columns in ERROR_TABLE:", list(error_columns_details.keys()))

import pandas as pd 
from datetime import datetime

example_timestamp = "2025/11/27 14:58:01"

#extract only date part
dt_object = datetime.strptime(example_timestamp, "%Y/%m/%d %H:%M:%S")
print("Date:", dt_object.date())