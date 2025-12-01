from main_error_table_code import CreateErrorTableCode

if __name__ == "__main__":
    MACHINE_NAME_CODE = {
        "AM322": {"code": 1, "error_pattern": "pattern_1"}, 
        "AM323": {"code": 2, "error_pattern": "pattern_2"}
    }
    tracker = CreateErrorTableCode(machine_name_code=None ,day_night="昼勤", unit_code="10-1719")

    print(tracker.extract_bit_value("0100",8))