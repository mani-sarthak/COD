import os
import pandas as pd
import glob

# Define the root directory where your data is located
root_directory = '/Users/manisarthak/Desktop/CGWB/'

# Define the years range
start_year = 2010
end_year = 2020

# Initialize an empty DataFrame to store the organized data
merged_data = pd.DataFrame()

# Loop through each year directory
for year in range(start_year, end_year + 1):
    year_directory = os.path.join(root_directory, str(year))
    
    # Check if the year directory exists
    if os.path.exists(year_directory):
        # Find all district directories in the year directory
        district_directories = glob.glob(os.path.join(year_directory, 'Rajasthan/Bhilwara'))
        
        # Initialize an empty list to store DataFrames for this year
        year_data = []
        
        # Loop through each district directory
        for district_directory in district_directories:
            # Find all Excel files in the district directory
            # print(district_directory, end = "\n\n\n\n\n\n")
            excel_files = glob.glob(os.path.join(district_directory, '*.xlsx'))
            
            # Loop through each Excel file in the district directory
            for excel_file in excel_files:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(excel_file)
                
                # Append the data to the list
                # year_data.append(df)
                print(df, end = '\n\n\n\n\n\n')
                
            print("\n\n\n\n\n\n")
        
        # Concatenate all DataFrames for this year
        # if year_data:
            # year_data = pd.concat(year_data)
            # merged_data = pd.concat([merged_data, year_data])
            # print(year_data)

# Reset the index to have a continuous index
merged_data.reset_index(drop=True, inplace=True)

# Save the merged data as a CSV file
merged_data.to_csv('/Users/manisarthak/Desktop/CGWB/bhilwara_time_series_data.csv', index=False)
