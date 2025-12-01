from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
# some of the predefined data 



# # Error Pattern Configuration
# ERROR_PATTERN_TYPES = {
#     'pattern_1': {
#         '起動時異常': {
#             'code': '1',
#             'register_start': 550,
#             'register_end': 564,
#             'bit_number_start': 0,
#             'bits_per_register': 16,
#             'description': 'Pattern 1 起動時異常 registers'
#         },
#         '運転中異常': {
#             'code': '2',
#             'register_start': 565,
#             'register_end': 589,
#             'bit_number_start': 240,
#             'bits_per_register': 16,
#             'description': 'Pattern 1 運転中異常 registers'
#         }
#     },
#     'pattern_2': {
#         '起動時異常': {
#             'code': '1',
#             'register_start': 550,
#             'register_end': 569,
#             'bit_number_start': 0,
#             'bits_per_register': 16,
#             'description': 'Pattern 2 起動時異常 registers'
#         },
#         '運転中異常': {
#             'code': '2',
#             'register_start': 570,
#             'register_end': 589,
#             'bit_number_start': 320,
#             'bits_per_register': 16,
#             'description': 'Pattern 2 運転中異常 registers'
#         }
#     }
# }



class CreateErrorTableCode:
    def __init__(self, machine_name_code=None, day_night="昼勤", 
                 unit_code="10-1719", data_path=None):
        self.day_night = day_night
        self.unit_code = unit_code
        self.machine_name_code = machine_name_code
        self.working_mode = {"502.12": "自動", "502.13": "手動", "502.14": "払出"}
        self.data = None
        
        # Active error tracking: {machine_name: {bit_number: {start_time, error_type}}}
        self.active_errors = {}
        
        # Output rows: List of dictionaries for CSV
        self.output_rows = []
        
        if data_path is not None:
            self.data = pd.read_csv(data_path, encoding="utf-8")
    
    
    def get_bit_number(self, register: int, bit_position: int, pattern: str) -> Tuple[int, str]:
        """
        Calculate absolute bit number and determine error type.
        Returns: (bit_number, error_type)
        """
        pattern_config = ERROR_PATTERN_TYPES[pattern]
        
        for error_type, config in pattern_config.items():
            if config['register_start'] <= register <= config['register_end']:
                register_offset = register - config['register_start']
                bit_number = (register_offset * config['bits_per_register']) + bit_position + config['bit_number_start']
                return (bit_number, error_type)
        
        raise ValueError(f"Register {register} not found in pattern {pattern}")
    
    
    def extract_bit_value(self, register_value: int, bit_position: int) -> int:
        """Extract specific bit value from register value (16-bit integer)."""
        if pd.isna(register_value):
            return 0
        return (int(register_value) >> bit_position) & 1
    
    
    def add_output_row(self, timestamp: datetime, machine_code: int, machine_name: str,
                       bit_number: int, error_type: str, duration: Optional[int]):
        """
        Add a row to output.
        duration: 0 for start, calculated seconds for end, None for other error type
        """
        row = {
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'machine_code': machine_code,
            'machine_name': machine_name,
            'bit_number': bit_number,
            '起動時異常': None,
            '運転中異常': None
        }
        
        # Set duration in appropriate column
        if error_type == '起動時異常':
            row['起動時異常'] = duration
        elif error_type == '運転中異常':
            row['運転中異常'] = duration
        
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
                bit_number, error_type = self.get_bit_number(register, bit_position, pattern)
            except ValueError:
                continue  # Skip if register not in monitoring range
            
            # Check if this bit is currently active
            is_active = bit_number in self.active_errors[machine_name]
            
            if bit_value == 1 and not is_active:
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
            print("register_ranges:", register_ranges)
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
            return pd.DataFrame(columns=['Timestamp', 'machine_code', 'machine_name', 
                                        'bit_number', '起動時異常', '運転中異常'])
        
        df = pd.DataFrame(self.output_rows)
        return df
    
    
    def export_to_csv(self, output_path: str):
        """Export error log to CSV."""
        df = self.get_output_dataframe()
        if not df.empty:
            df.to_csv(output_path, index=False, encoding='utf-8')
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
    
    
    # def export_error_log(self, output_path: str):
    #     """Export error log to CSV."""
    #     df = self.get_error_summary()
    #     if not df.empty:
    #         df.to_csv(output_path, index=False, encoding='utf-8')
    #         print(f"Error log exported to {output_path}")
    #     else:
    #         print("No errors to export")



if __name__ == "__main__":
        # Machine Configuration
    MACHINE_NAME_CODE = {
        "AM322": {"code": 1, "error_pattern": "pattern_2"}, 
        "AM323": {"code": 2, "error_pattern": "pattern_1"}
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
    
    # Display results
    print("\n=== OUTPUT PREVIEW ===")
    print(output_df.head(20))
    
    print("\n=== STATISTICS ===")
    print(f"Total error events: {len(output_df)}")
    print(f"Active errors (still ongoing): {sum(len(v) for v in tracker.active_errors.values())}")
    
    # Export to CSV
    tracker.export_to_csv("error_log_output.csv")
    
    # Example: Filter by machine
    if not output_df.empty:
        am322_errors = output_df[output_df['machine_name'] == 'AM322']
        print(f"\nAM322 errors: {len(am322_errors)} rows")
        
        # Show only completed errors (duration > 0)
        completed_startup = output_df[output_df['起動時異常'].notna() & (output_df['起動時異常'] > 0)]
        print(f"\nCompleted 起動時異常 errors: {len(completed_startup)}")
        
        completed_runtime = output_df[output_df['運転中異常'].notna() & (output_df['運転中異常'] > 0)]
        print(f"Completed 運転中異常 errors: {len(completed_runtime)}")






# # ============================================================================
# # USAGE EXAMPLE
# # ============================================================================

# if __name__ == "__main__":
#     day_night= "昼勤"    
#     unit_code = "10-1719"
#     machine_name_code ={"AM322": {"code": 1, "error_pattern": "pattern_1"}, 
#                         "AM323":{"code": 2, "error_pattern": "pattern_2"}}
#     # Machine Configuration
#     MACHINE_NAME_CODE = {
#         "AM322": {"code": 1, "error_pattern": "pattern_1"}, 
#         "AM323": {"code": 2, "error_pattern": "pattern_2"}
#     }
#     # Initialize the error tracker
#     tracker = CreateErrorTableCode(
#         machine_name_code=MACHINE_NAME_CODE,
#         day_night="昼勤",
#         unit_code="10-1719",
#         data_path="Combined_sorted.csv"  # Your CSV file path
#     )
    
#     # Process the data
#     print("Processing data...")
#     error_summary = tracker.process_data()
    
#     # Display results
#     print("\n=== ERROR SUMMARY ===")
#     print(error_summary)
    
#     print("\n=== ACTIVE ERRORS (Still ongoing) ===")
#     print(tracker.get_active_errors_summary())
    
#     # Export to CSV
#     tracker.export_error_log("error_log_output.csv")
    
#     # Example: Filter errors by machine
#     if not error_summary.empty:
#         am322_errors = error_summary[error_summary['machine_name'] == 'AM322']
#         print("\n=== AM322 ERRORS ===")
#         print(am322_errors)
        
#         # Get errors that lasted more than 60 seconds
#         long_errors = error_summary[error_summary['duration_seconds'] > 60]
#         print("\n=== ERRORS > 60 seconds ===")
#         print(long_errors)


        