import os
import pandas as pd
import glob

# Define the root directory where your data is located
root_directory = '/Users/manisarthak/Desktop/CGWB/'

# Initialize an empty DataFrame to store the organized data
merged_data = pd.DataFrame()

# Loop through each year directory
for year_directory in glob.glob(os.path.join(root_directory, '*')):
    # Loop through each state directory
    for state_directory in glob.glob(os.path.join(year_directory, '*')):
        # Check if the state directory is Rajasthan
        if 'Rajasthan' in state_directory:
            # Find all Excel files in the Bhilwara district directory
            bhilwara_directory = os.path.join(state_directory, 'Bhilwara')
            excel_files = glob.glob(os.path.join(bhilwara_directory, '*.xlsx'))
            
            # Loop through each Excel file in the Bhilwara directory
            for excel_file in excel_files:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(excel_file)
                
                # Extract the relevant columns
                df = df[['station_id', 'lat', 'long', 'water_level (in m)']]
                
                # Get the year from the directory name
                year = os.path.basename(year_directory)
                
                # Rename the water level column to include the year
                df.rename(columns={'water_level (in m)': f'water_level_{year}'}, inplace=True)
                
                # Merge the data into the merged_data DataFrame based on 'station_id'
                if merged_data.empty:
                    merged_data = df
                else:
                    merged_data = pd.merge(merged_data, df, on=['station_id', 'lat', 'long'], how='outer')

# Save the merged data as a CSV file
output_path = '/Users/manisarthak/Desktop/CGWB/bhilwara_time_series_data.csv'
merged_data.to_csv(output_path, index=False)
