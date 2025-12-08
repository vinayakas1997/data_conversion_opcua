from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES, get_bit_number
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class CreateErrorTableCode:
    def __init__(self, machine_name_code=None, day_night="昼勤", 
                 unit_code="10-1719", work_date=None, data_path=None):
        self.day_night = day_night
        self.unit_code = unit_code
        self.machine_name_code = machine_name_code
        self.work_date = work_date  # Format: "YYYY/MM/DD"
        self.data = None

        # Initialize ERROR_TABLE
        self.ERROR_TABLE = ERROR_TABLE
        self.error_columns_details = self.ERROR_TABLE.get("columns", {})
        self.error_column_names = list(self.error_columns_details.keys())
        
        # Active error tracking: {machine_name: {bit_number: {start_time, error_type}}}
        self.active_errors = {}
        
        # Output rows: List of dictionaries for CSV
        self.output_rows = []
        
        if data_path is not None:
            self.data = pd.read_csv(data_path, encoding="utf-8", dtype=str)
            # Parse custom timestamp format: HH:MM:SS:mmm
            time_parsed = pd.to_datetime(
                self.data['Timestamp'].str.replace(':', '.', n=2),
                format='%H.%M.%S:%f'
            )
            
            # Combine with work_date if provided
            if self.work_date:
                date_obj = pd.to_datetime(self.work_date, format='%Y/%m/%d')
                self.data['Timestamp'] = pd.to_datetime(
                    date_obj.strftime('%Y-%m-%d') + ' ' + 
                    time_parsed.dt.strftime('%H:%M:%S.%f')
                )
            else:
                self.data['Timestamp'] = time_parsed
            
            print(f"Data loaded: {len(self.data)} rows")
    
    
    def extract_bit_value(self, register_value, bit_position: int) -> int:
        """Extract specific bit value from register value (hex string)."""
        if pd.isna(register_value) or register_value in ('nan', ''):
            return 0

        if isinstance(register_value, str):
            cleaned = register_value.lower().replace('0x', '')
            if not all(c in '0123456789abcdef' for c in cleaned):
                return 0
            if len(cleaned) > 4:
                return 0
            cleaned = cleaned.zfill(4)
            register_value = int(cleaned, 16)

        return (int(register_value) >> bit_position) & 1

    
    def get_operation_mode(self, timestamp: datetime, machine_name: str) -> str:
        """Get operation mode from IO_0502 register."""
        filtered = self.data.loc[
            (self.data['Timestamp'] == timestamp) &
            (self.data['Machine_Name'] == machine_name) &
            (self.data['reg_address'] == 'IO_0502')
        ]["value"]
        
        if filtered.empty:
            return "None"
        
        mode_value = filtered.values[0]
        
        mode_map = {
            "9000": "自動",
            "A000": "手動",
            "8000": "払出"
        }
        
        return mode_map.get(mode_value, "None")
    
    
    def add_output_row(self, timestamp: datetime, machine_code: int, machine_name: str,
                       bit_number: int, error_type: str, number_status: str, duration: Optional[int]):
        """Add a row to output."""
        columns = self.error_column_names
        timestamp_str = timestamp.strftime("%Y/%m/%d %H:%M:%S")
        date_str = timestamp.date().strftime("%Y/%m/%d")
        
        row = {
            columns[0]: timestamp_str,                          # 日付
            columns[1]: date_str,                               # 勤務日付軸
            columns[2]: self.day_night,                         # 昼夜勤
            columns[3]: self.unit_code,                         # ユニットコード
            columns[4]: machine_code,                           # 工程順番
            columns[5]: machine_name,                           # 機番
            columns[6]: "-",                                    # 時間帯
            columns[7]: "--",                                   # 作業者
            columns[8]: self.get_operation_mode(timestamp_str, machine_name),  # 運転モード
            columns[9]: error_type,                             # 異常種類
            columns[10]: bit_number,                            # 異常№
            columns[11]: "need_data",                           # 異常内容
            columns[12]: number_status,                         # ON/OFF
        }
        
        # 起動時異常 and 運転中異常
        if error_type == "起動時異常":
            row[columns[13]] = duration
            row[columns[14]] = 0
        elif error_type == "運転中異常":
            row[columns[13]] = 0
            row[columns[14]] = duration
        else:
            row[columns[13]] = 0
            row[columns[14]] = 0
        
        # # Fill remaining columns with None
        # for col in columns[15:]:
        #     row[col] = "None"

        for col in columns[15:]:
            col_config = self.error_columns_details[col]
            plc_address = col_config.get("PLC_Memory_Address", "")
            
            if plc_address:  # If PLC address exists and is not empty
                # Convert "DM31651" to "D_31651" format
                register_col = plc_address.replace("M", "_")  # DM31651 -> D_31651

                # Debug print
                print(f"Looking for: timestamp={timestamp}, machine={machine_name}, reg={register_col}")
        
                # Filter data to get the value
                filtered = self.data.loc[
                                (self.data['Machine_Name'] == machine_name) &
                                (self.data['reg_address'] == register_col) &
                                (self.data['Timestamp'] <= timestamp)
                            ].sort_values('Timestamp', ascending=False)  # Sort by timestamp descending
                                    
                # print(f"Found {len(filtered)} rows, value: {filtered.values[0] if not filtered.empty else 'EMPTY'}")
        
                if not filtered.empty:
                    # row[col] = filtered.values[0]['value']
                    row[col] = filtered.iloc[0]['value']
                else:
                    row[col] = "None"
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
        
        found_errors = False
        for bit_position in range(16):
            bit_value = self.extract_bit_value(register_value, bit_position)
            
            try:
                bit_number, error_type, _ = get_bit_number(register, bit_position, pattern)
            except ValueError:
                continue  # Skip if register not in monitoring range
            
            # Debug: Print when we find a bit set to 1
            if bit_value == 1:
                if not found_errors:
                    # print(f"[DEBUG] Found error bit: Machine={machine_name}, Register={register}, Bit={bit_position}, BitNum={bit_number}, Type={error_type}, Time={timestamp}")
                    found_errors = True
            
            is_active = bit_number in self.active_errors[machine_name]
            
            if bit_value == 1 and not is_active:
                # ERROR STARTED
                # print(f"[ERROR START] Bit {bit_number} ({error_type}) started at {timestamp}")
                self.active_errors[machine_name][bit_number] = {
                    'start_time': timestamp,
                    'error_type': error_type
                }
                
                self.add_output_row(
                    timestamp=timestamp,
                    machine_code=machine_code,
                    machine_name=machine_name,
                    bit_number=bit_number,
                    error_type=error_type,
                    number_status="on",
                    duration=0
                )
                
            elif bit_value == 0 and is_active:
                # ERROR ENDED
                start_info = self.active_errors[machine_name][bit_number]
                start_time = start_info['start_time']
                error_type = start_info['error_type']
                
                # Calculate duration with millisecond precision
                duration_sec = (timestamp - start_time).total_seconds()
                duration_sec = round(duration_sec, 3)  # Round to 3 decimal places
                
                # print(f"[ERROR END] Bit {bit_number} ({error_type}) ended at {timestamp}, Duration: {duration_sec}s")
                
                self.add_output_row(
                    timestamp=timestamp,
                    machine_code=machine_code,
                    machine_name=machine_name,
                    bit_number=bit_number,
                    error_type=error_type,
                    number_status="異常処置終了",
                    duration=duration_sec
                )
                
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
        
        # DEBUG: Check data structure
        print(f"Columns in data: {self.data.columns.tolist()}")
        print(f"Sample data:\n{self.data.head(10)}")
        print(f"Unique machines: {self.data['Machine_Name'].unique()}")
        
        # Group data by timestamp and machine to reconstruct rows
        grouped = self.data.groupby(['Timestamp', 'Machine_Name'])
        
        print(f"\nTotal timestamp-machine groups: {len(grouped)}")
        
        # Process each timestamp-machine combination
        for (timestamp, machine_name), group in grouped:
            
            if machine_name not in self.machine_name_code:
                continue
            
            # Convert group to a dictionary of register:value pairs
            register_values = {}
            for _, row in group.iterrows():
                reg_col = row['reg_address']  # e.g., 'IO_0550'
                register_values[reg_col] = row['value']
            
            # Get register ranges to monitor for this machine
            register_ranges = self.get_register_range_for_machine(machine_name)
            
            # Check all registers in the monitoring range
            registers_checked = 0
            for start_reg, end_reg in register_ranges:
                for register in range(start_reg, end_reg + 1):
                    col_name = f"IO_{register:04d}"
                    
                    if col_name in register_values:
                        registers_checked += 1
                        register_value = register_values[col_name]
                        self.process_register_bits(machine_name, register, 
                                                   register_value, timestamp)
        
        print(f"\nProcessed {len(grouped)} timestamp groups")
        print(f"Registers checked: {registers_checked}")
        print(f"Output rows generated: {len(self.output_rows)}")
        
        return self.get_output_dataframe()
    
    
    def get_output_dataframe(self) -> pd.DataFrame:
        """Convert output rows to DataFrame."""
        if not self.output_rows:
            return pd.DataFrame(columns=self.error_column_names)
        
        return pd.DataFrame(self.output_rows)
    
    
    def export_to_csv(self, output_path: str):
        """Export error log to CSV."""
        df = self.get_output_dataframe()
        if not df.empty:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"✓ Error log exported to {output_path} ({len(df)} rows)")
        else:
            print("⚠ No errors to export")
    
    
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
    
    plc_data_file = "2_postgres_DB/Combined_sorted_parsed_output.csv"
    work_date = "2025/11/27"  # Specify your work date here
    
    # Initialize the error tracker
    tracker = CreateErrorTableCode(
        machine_name_code=MACHINE_NAME_CODE,
        day_night="昼勤",
        unit_code="10-1719",
        work_date=work_date,  # Pass the date
        data_path=plc_data_file
    )
    
    # Process the data
    print("Processing data...")
    output_df = tracker.process_data()
    
    print(f"\n=== STATISTICS ===")
    print(f"Total error events: {len(output_df)}")
    print(f"Active errors (still ongoing): {sum(len(v) for v in tracker.active_errors.values())}")
    
    # Export to CSV
    tracker.export_to_csv("2_postgres_DB/d_error_output.csv")