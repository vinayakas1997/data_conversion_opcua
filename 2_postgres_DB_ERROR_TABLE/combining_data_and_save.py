

import pandas as pd

data_path1 = "2_postgres_DB/Vina_data/AM322_parsed_output.csv"
data_path2 = "2_postgres_DB/Vina_data/AM323_parsed_output.csv"
output_path = "2_postgres_DB/Combined_sorted_parsed_output.csv"

# Read both CSV files
df1 = pd.read_csv(data_path1)
df2 = pd.read_csv(data_path2)

# Concatenate the dataframes
combined_df = pd.concat([df1, df2], ignore_index=True)

# Sort by 'Timestamp' column
combined_df = combined_df.sort_values(by='Timestamp')

# Save to output file
combined_df.to_csv(output_path, index=False)

print(f"Combined and sorted data saved to {output_path}")
print(f"Total rows: {len(combined_df)}")