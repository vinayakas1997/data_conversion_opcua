import pandas as pd
from datetime import datetime

class TableFormatter:
    def __init__(self, datapath: str, device_name: str = None, start_time: str = None, end_time: str = None):
        self.filepath = datapath
        self.df = None
        self.device_name = device_name
        self.start_time = start_time
        self.end_time = end_time
        self.to_ignore_columns = ['id', 'device_name', 'recorded_at']
        self.running_column = None
        self.parsed_data = []  # Store parsed records

        try: 
            self.df = pd.read_csv(self.filepath)
            print("Original DataFrame:")
            print(self.df.head())
            print(f"\nOriginal shape: {self.df.shape}")
            
            # Process the data
            self._process_data()
            
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            self.df = pd.DataFrame()
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            self.df = pd.DataFrame()
    
    def _process_data(self):
        """Process the dataframe according to filtering requirements"""
        if self.df.empty:
            return
        
        # Step 1: Find the 'running' column
        self.running_column = self._find_running_column()
        if self.running_column is None:
            print("Warning: No 'running' column found")
            return
        
        print(f"\nFound running column: {self.running_column}")
        
        # Step 2: Filter rows where running == True
        self.df = self.df[self.df[self.running_column] == True].copy()
        print(f"After filtering running==True: {self.df.shape}")
        
        # Step 3: Filter by time range if provided
        if self.start_time or self.end_time:
            self._filter_by_time()
        
        # Step 4: Drop ignored columns
        self._drop_columns()
        
        print("\nProcessed DataFrame:")
        print(self.df.head())
        print(f"Final shape: {self.df.shape}")
        
        # Step 5: Parse each column's values
        self._parse_columns()
    
    def _find_running_column(self):
        """Find column name containing 'running' (case-insensitive)"""
        for col in self.df.columns:
            if 'running' in col.lower():
                return col
        return None
    
    def _filter_by_time(self):
        """Filter dataframe by start and end time"""
        # Convert recorded_at to datetime (it already has timezone info from CSV)
        self.df['recorded_at'] = pd.to_datetime(self.df['recorded_at'])
        
        # Get the timezone from the dataframe
        tz = self.df['recorded_at'].dt.tz
        
        if self.start_time:
            # Convert start_time to datetime and localize to the same timezone
            start_dt = pd.to_datetime(self.start_time)
            if start_dt.tz is None and tz is not None:
                # If start_dt has no timezone but data has timezone, localize it
                start_dt = start_dt.tz_localize(tz)
            elif start_dt.tz is not None and tz is not None:
                # If both have timezones, convert to match
                start_dt = start_dt.tz_convert(tz)
            
            self.df = self.df[self.df['recorded_at'] >= start_dt]
            print(f"After filtering start_time >= {self.start_time}: {self.df.shape}")
        
        if self.end_time:
            # Convert end_time to datetime and localize to the same timezone
            end_dt = pd.to_datetime(self.end_time)
            if end_dt.tz is None and tz is not None:
                # If end_dt has no timezone but data has timezone, localize it
                end_dt = end_dt.tz_localize(tz)
            elif end_dt.tz is not None and tz is not None:
                # If both have timezones, convert to match
                end_dt = end_dt.tz_convert(tz)
            
            self.df = self.df[self.df['recorded_at'] <= end_dt]
            print(f"After filtering end_time <= {self.end_time}: {self.df.shape}")
    
    def _drop_columns(self):
        """Drop ignored columns and running column"""
        columns_to_drop = self.to_ignore_columns.copy()
        
        # Add running column to drop list
        if self.running_column and self.running_column in self.df.columns:
            columns_to_drop.append(self.running_column)
        
        # Only drop columns that exist in the dataframe
        columns_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        
        self.df = self.df.drop(columns=columns_to_drop)
        print(f"Dropped columns: {columns_to_drop}")
    
    def _extract_reg_address(self, column_name):
        """
        Extract register address from column name
        Example: P6_IO_0500_C -> IO_0500
        """
        parts = column_name.split('_')
        
        # Remove first part (e.g., P6) and last part (e.g., C)
        if len(parts) >= 3:
            # Join middle parts
            reg_address = '_'.join(parts[1:-1])
            return reg_address
        
        return column_name  # Return original if pattern doesn't match
    
    def _parse_columns(self):
        """Parse each column's values and create structured records"""
        print("\n" + "="*80)
        print("Parsing columns...")
        
        for index, row in self.df.iterrows():
            for column in self.df.columns:
                cell_value = row[column]
                
                # Skip if value is NaN or empty
                if pd.isna(cell_value) or cell_value == '':
                    continue
                
                # Check if value contains '&&'
                if '&&' in str(cell_value):
                    parts = str(cell_value).split('&&')
                    
                    if len(parts) == 2:
                        value = parts[0]
                        timestamp = parts[1]
                        reg_address = self._extract_reg_address(column)
                        
                        record = {
                            'Timestamp': timestamp,
                            'Machine_Name': self.device_name,
                            'reg_address': reg_address,
                            'value': value, 
                        }
                        
                        self.parsed_data.append(record)
        
        print(f"Total records parsed: {len(self.parsed_data)}")
        
        # Create a new dataframe from parsed data
        if self.parsed_data:
            self.parsed_df = pd.DataFrame(self.parsed_data)
            print("\nParsed DataFrame sample:")
            print(self.parsed_df.head(10))
            print(f"\nParsed DataFrame shape: {self.parsed_df.shape}")
        else:
            print("No data was parsed!")
            self.parsed_df = pd.DataFrame()
    
    def save_to_csv(self, output_path: str):
        """Save the parsed dataframe to CSV file"""
        if hasattr(self, 'parsed_df') and not self.parsed_df.empty:
            try:
                self.parsed_df.to_csv(output_path, index=False)
                print(f"\n✓ Successfully saved to: {output_path}")
                print(f"  Total records saved: {len(self.parsed_df)}")
            except Exception as e:
                print(f"\n✗ Error saving to CSV: {e}")
        else:
            print("\n✗ No parsed data to save!")


if __name__ == "__main__":
    data_path = "2_postgres_DB/Vina_data/AM322_postgres_old.csv"
    formatter = TableFormatter(
        datapath=data_path, 
        device_name="AM322",
        start_time="2025-11-27 14:00:00",
        end_time="2025-11-27 14:40:00"
    )
    # Save to CSV
    output_path = "2_postgres_DB/Vina_data/AM322_parsed_output.csv"
    formatter.save_to_csv(output_path)

    data_path = "2_postgres_DB/Vina_data/AM323_postgres_old.csv"
    formatter = TableFormatter(
        datapath=data_path, 
        device_name="AM323",
        start_time="2025-11-27 14:00:00",
        end_time="2025-11-27 14:40:00"
    )
    # Save to CSV
    output_path = "2_postgres_DB/Vina_data/AM323_parsed_output.csv"
    formatter.save_to_csv(output_path)