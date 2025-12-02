# read the csv and add the column called as the machine_name in the last column as defualt value "what the input is given" 
import pandas as pd


# step 1: 
def add_default_value_column(csv_file_path, output_csv_file_path, column_name, default_value):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Drop the column if "running is present in the name of the columns Ex P6_running"
    df = df.loc[:, ~df.columns.str.contains('running', case=False)]

    def clean_column(col):
        parts = col.split('_')
        if len(parts) >= 3:
            return '_'.join(parts[1:-1])  # drop first and last
        return col


    # change the column names to EX : P6_IO_0500_C, P6_D_31734_C --> IO_0500_C, D_31734_C
    df.columns = [clean_column(col) for col in df.columns ]

     
    # Add the new column with the default value
    df[column_name] = default_value


    # Save the modified DataFrame back to a new CSV file
    df.to_csv(output_csv_file_path, index=False)
    print(f"Added column '{column_name}' with default value '{default_value}' to {output_csv_file_path}")

# add_default_value_column(r"Vina_data/Triton_AM323_192_168_16_2.csv", "AM323.csv", "Machine_Name", "AM323")

# step2: 
# 2 csv files read it and combine the data into csv file and arranged by the time stamp column
def combine_and_sort_csv(csv_file_path1, csv_file_path2, output_csv_file_path):
    df1 = pd.read_csv(csv_file_path1)
    df2 = pd.read_csv(csv_file_path2)

    df = pd.concat([df1, df2], ignore_index=True)
    df = df.sort_values(by='Timestamp')
    df.to_csv(output_csv_file_path, index=False)
    print(f"Combined and sorted data saved to {output_csv_file_path}")

combine_and_sort_csv("AM322.csv", "AM323.csv", "Combined_sorted.csv")