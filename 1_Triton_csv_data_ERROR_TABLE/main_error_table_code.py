from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES, get_bit_number
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
# some of the predefined data 




class CreateErrorTableCode:
    def __init__(self, machine_name_code=None, day_night="昼勤", 
                 unit_code="10-1719", data_path=None):
        self.day_night = day_night
        self.unit_code = unit_code
        self.machine_name_code = machine_name_code
        self.working_mode = {"502.12": "自動", "502.13": "手動", "502.14": "払出"}
        self.data = None

        # Initilaize ERROR_TABLE
        self.ERROR_TABLE = ERROR_TABLE
        self.error_columns_details = self.ERROR_TABLE.get("columns", {})
        self.error_column_names = list(self.error_columns_details.keys())
        # Active error tracking: {machine_name: {bit_number: {start_time, error_type}}}
        self.active_errors = {}
        
        # Output rows: List of dictionaries for CSV
        self.output_rows = []
        
        if data_path is not None:
            self.data = pd.read_csv(data_path, encoding="utf-8", dtype=str)
            print()
    
    
    def extract_bit_value(self, register_value, bit_position: int) -> int:
        """Extract specific bit value from register value 
        (16-bit integer or 4-digit hex string).

        Args:
            register_value: int or str (hex) [my case is str from csv]
            bit_position: int (0-15)
        Returns: 
            int: 0 or 1        
        """
        if pd.isna(register_value) or register_value in ('nan', ''):
            return 0

        # Handle hex string input
        if isinstance(register_value, str):
            # Clean the hex string
            cleaned = register_value.lower().replace('0x', '')
            if not all(c in '0123456789abcdef' for c in cleaned):
                raise ValueError(f"Invalid hex string: {register_value}. Contains non-hex characters.")
            if len(cleaned) > 4:
                raise ValueError(f"Invalid hex string: {register_value}. Too many digits (max 4).")
            # Pad with leading zeros to make 4 digits
            cleaned = cleaned.zfill(4)
            # Convert to integer
            register_value = int(cleaned, 16)

        # Extract the bit (works for integers)
        return (int(register_value) >> bit_position) & 1

    
    def add_output_row(self, timestamp: datetime, machine_code: int, machine_name: str,
                       bit_number: int, error_type: str, number_status: str ,duration: Optional[int]):
        """
        Add a row to output.
        duration: 0 for start, calculated seconds for end, None for other error type
        """
        row = {}
        columns = list(self.error_columns_details.keys())
        # in the timestamp repace - with /
        timestamp = timestamp.strftime("%Y/%m/%d %H:%M:%S")

        # column 0 -  日付
        row[columns[0]] = timestamp

        # column 1 - 勤務日付軸 
        try:
            dt_object = datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
            date = dt_object.date().strftime("%Y/%m/%d")
            row[columns[1]] = date
        except Exception as e :
            print("Error parsing timestamp:", timestamp, e)
        

        # column 2 - 昼夜勤
        row[columns[2]] = self.day_night

        #column 3 - ユニットコード
        row[columns[3]] = self.unit_code

        # column 4 - 工程順番
        row[columns[4]] = machine_code

        # column 5 - 機番
        row[columns[5]] = machine_name

        # column 6 - 時間帯
        row[columns[6]] = "-"

        # column 7 - 作業者
        row[columns[7]] = "--"

        # column 8 - 運転モード -- has to be developed
        
        filer_value = self.data.loc[
                    (self.data['Timestamp'] == timestamp) &
                    (self.data['Machine_Name'] == machine_name)
                    ]["IO_0502"]
        if not filer_value.empty:
            mode_value = filer_value.values[0]
        # print("mode_value:", mode_value)
        if mode_value == "9000":
            row[columns[8]] = "自動"
        elif mode_value == "A000":
            row[columns[8]] = "手動"
        elif mode_value == "8000":   
            row[columns[8]] = "払出"
        else:
            row[columns[8]]="None" 
        # row[columns[8]] = "--"


        # column 9 - 異常種類
        row[columns[9]] = error_type

        # column 10 - 異常№
        row[columns[10]] = bit_number

        # column 11 - 異常内容
        row[columns[11]] = "need_data"

        # column 12 - ON/OFF (number status)
        row[columns[12]] = number_status


        # column 13, 14 - 起動時異常, 運転中異常
        if error_type == "起動時異常":
            row[columns[13]] = duration
            row[columns[14]] = 0
        elif error_type == "運転中異常":
            row[columns[13]] = 0
            row[columns[14]] = duration
        else:
            row[columns[13]] = 0
            row[columns[14]] = 0

        # print("From the 15 columns ##### ------------")
        # print(f"\n\n{self.data.head()}")
        # for all other columns, fill with None
        # for col in columns[15:]:
        #     row[col] = "None"
        for col in columns[15:]:
            col_config = self.error_columns_details[col]
            plc_address = col_config.get("PLC_Memory_Address", "")
            
            if plc_address:  # If PLC address exists and is not empty
                # Convert "DM31651" to "D_31651" format
                register_col = plc_address.replace("M", "_")  # DM31651 -> D_31651

                # Debug print
                # print(f"Looking for: timestamp={timestamp}, machine={machine_name}, reg={register_col}")
        
                # Filter data to get the value
                filtered = self.data.loc[
                    (self.data['Timestamp'] == timestamp) &
                    (self.data['Machine_Name'] == machine_name)
                ][register_col]
                
                # print(f"Found {len(filtered)} rows, value: {filtered.values[0] if not filtered.empty else 'EMPTY'}")
        
                if not filtered.empty:
                    row[col] = filtered.values[0]
                else:
                    row[col] = 0
            else:  # No PLC address
                row[col] = "None"
        
        
        self.output_rows.append(row)
    
    
    def process_register_bits(self, machine_name: str, register: int, 
                              register_value: int, timestamp: datetime):
        """Process all 16 bits of a register for error tracking."""
        machine_code = self.machine_name_code[machine_name]['code']
        pattern = self.machine_name_code[machine_name]['error_pattern']
        
        if machine_name not in self.active_errors:
            self.active_errors[machine_name] = {}
        
        for bit_position in range(16):
            bit_value = self.extract_bit_value(register_value, bit_position)
            
            try:

                bit_number, error_type, _ = get_bit_number(register, bit_position, pattern)
                # print(f"from process register_bits: register: {register}, bit_position: {bit_position}, pattern: {pattern}, bit_number: {bit_number}, error_type: {error_type}")
            except ValueError:
                continue  # Skip if register not in monitoring range
            
            # Check if this bit is currently active
            is_active = bit_number in self.active_errors[machine_name]
            
            if bit_value == 1 and not is_active:
                # print(f"All details - bit number: {bit_number} error_type:{error_type} register value: {register_value}, bit_position: {bit_position}, bit_value: {bit_value}")
                # ===== BIT BECAME 1 (ERROR STARTED) =====
                # Record start time
                self.active_errors[machine_name][bit_number] = {
                    'start_time': timestamp,
                    'error_type': error_type
                }
                
                # Add row with duration = 0
                self.add_output_row(
                    timestamp=timestamp,
                    machine_code=machine_code,
                    machine_name=machine_name,
                    bit_number=bit_number,
                    error_type=error_type,
                    number_status= "on",
                    duration=0
                )
                
            elif bit_value == 0 and is_active:
                # ===== BIT BECAME 0 (ERROR ENDED) =====
                start_info = self.active_errors[machine_name][bit_number]
                start_time = start_info['start_time']
                error_type = start_info['error_type']
                
                # Calculate duration in seconds
                duration_sec = int((timestamp - start_time).total_seconds())
                
                # Add row with calculated duration
                self.add_output_row(
                    timestamp=timestamp,
                    machine_code=machine_code,
                    machine_name=machine_name,
                    bit_number=bit_number,
                    error_type=error_type,
                    number_status= "異常処置終了",
                    duration=duration_sec
                )
                
                # Remove from active errors
                del self.active_errors[machine_name][bit_number]
    
    
    def get_register_range_for_machine(self, machine_name: str) -> List[Tuple[int, int]]:
        """Get the register ranges to monitor for a specific machine."""
        pattern = self.machine_name_code[machine_name]['error_pattern']
        pattern_config = ERROR_PATTERN_TYPES[pattern]
        
        ranges = []
        for error_type, config in pattern_config.items():
            ranges.append((config['register_start'], config['register_end']))
        
        return ranges
    
    
    def process_data(self):
        """Process the entire dataset and track errors."""
        if self.data is None:
            raise ValueError("No data loaded. Please provide data_path.")
        
        # Reset tracking
        self.active_errors = {}
        self.output_rows = []
        
        # Convert Timestamp column to datetime
        self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'])
        
        # Process each row (each cycle)
        for idx, row in self.data.iterrows():
            timestamp = row['Timestamp']
            machine_name = row['Machine_Name']
            
            if machine_name not in self.machine_name_code:
                continue  # Skip unknown machines
            
            # Get register ranges to monitor for this machine
            register_ranges = self.get_register_range_for_machine(machine_name)
            # print("register_ranges:", register_ranges)
            # Check all registers in the monitoring range
            for start_reg, end_reg in register_ranges:
                for register in range(start_reg, end_reg + 1):
                    col_name = f"IO_{register:04d}"  # Format: IO_0550
                    
                    if col_name in row:
                        register_value = row[col_name]
                        self.process_register_bits(machine_name, register, 
                                                   register_value, timestamp)
        
        return self.get_output_dataframe()
    
    
    def get_output_dataframe(self) -> pd.DataFrame:
        """Convert output rows to DataFrame."""
        if not self.output_rows:
            # return pd.DataFrame(columns=['Timestamp', 'machine_code', 'machine_name', 
            #                             'bit_number', '起動時異常', '運転中異常'])
            return pd.DataFrame(columns=self.error_column_names)
        
        df = pd.DataFrame(self.output_rows)
        return df
    
    
    def export_to_csv(self, output_path: str):
        """Export error log to CSV."""
        df = self.get_output_dataframe()
        if not df.empty:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Error log exported to {output_path} ({len(df)} rows)")
        else:
            print("No errors to export")
    
    
    def get_active_errors_summary(self, current_timestamp: datetime = None) -> Dict:
        """Get currently active errors (still ongoing)."""
        if current_timestamp is None:
            current_timestamp = datetime.now()
        
        summary = {}
        for machine, errors in self.active_errors.items():
            summary[machine] = {
                bit_num: {
                    'start_time': info['start_time'],
                    'error_type': info['error_type'],
                    'duration_so_far': (current_timestamp - info['start_time']).total_seconds()
                }
                for bit_num, info in errors.items()
            }
        return summary
    
    
 



if __name__ == "__main__":
        # Machine Configuration
    MACHINE_NAME_CODE = {
        "AM322": {"code": 1, "error_pattern": "pattern_1"}, 
        "AM323": {"code": 2, "error_pattern": "pattern_2"}
    }
    plc_data_file = "Combined_sorted.csv"
    # Initialize the error tracker
    tracker = CreateErrorTableCode(
        machine_name_code=MACHINE_NAME_CODE,
        day_night="昼勤",
        unit_code="10-1719",
        data_path=plc_data_file  # Your CSV file path
    )
    
    # Process the data
    print("Processing data...")
    output_df = tracker.process_data()
    
    # # Display results
    # print("\n=== OUTPUT PREVIEW ===")
    # print(output_df.head(20))
    
    # print("\n=== STATISTICS ===")
    # print(f"Total error events: {len(output_df)}")
    # print(f"Active errors (still ongoing): {sum(len(v) for v in tracker.active_errors.values())}")
    
    # # Export to CSV
    tracker.export_to_csv("proper_output3.csv")
    









        