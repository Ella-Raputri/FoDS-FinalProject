import pandas as pd
import os

# Specify the folder containing the CSV files
folder_path = 'wiki/wikidata'  # Adjust the path as needed

# List to hold all DataFrames
dataframes = []

# Iterate over all files in the specified folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):  # Check for CSV files
        file_path = os.path.join(folder_path, file)  # Get the full file path
        try:
            df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
            if not df.empty:  # Check if the DataFrame is not empty
                dataframes.append(df)  # Append the DataFrame to the list
            else:
                print(f"Warning: The file {file} is empty.")
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Check if there are any DataFrames to merge
if dataframes:
    # Start merging from the first DataFrame
    combined_df = dataframes[0]

    # Merge remaining DataFrames
    for df in dataframes[1:]:
        combined_df = combined_df.merge(df, on='Date', how='outer')  # Adjust 'on' to your key column(s)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('ombined_wikidata.csv', index=False)
    
else:
    print("No valid CSV files were found to merge.")
