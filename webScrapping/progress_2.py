import os
import time
from yearly import *

# Define the directory path
directory_path = "/Users/manisarthak/Desktop/CGWB/"

# Check if the directory already exists
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Define the filename for the log file
log_file = "log.txt"

# Function to log timestamps and calculate time taken
def log_timestamp(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")

# Define the progress file
progress_file = "progress.txt"

# Initialize variables to store progress information
last_year = 2005
last_state = None
last_district = None

# Check if the progress file exists and read progress information if it does
if os.path.isfile(progress_file):
    with open(progress_file, 'r') as f:
        last_year = int(f.readline().strip())
        last_state = f.readline().strip()
        last_district = f.readline().strip()
    log_timestamp(f"Resuming from year {last_year}, state {last_state}, district {last_district}")

# Define the start time
start_time = time.perf_counter()

# Loop through years
for year in range(last_year, 2004, -1):
    log_timestamp(f"Started processing year {year}")
    dp_year = directory_path + str(year) + '/'

    # Check if the directory already exists
    if not os.path.exists(dp_year):
        os.makedirs(dp_year)

    states = getStates(year)

    # Start from the last state if available
    if last_state:
        states = states[states.index(last_state):]

    for state in states:
        log_timestamp(f"Started processing state {state}")
        dp_state = dp_year + str(state) + '/'

        # Check if the directory already exists
        if not os.path.exists(dp_state):
            os.makedirs(dp_state)

        districts = getDistricts(state, year)

        # Start from the last district if available
        if last_district:
            districts = districts[districts.index(last_district):]

        for district in districts:
            with open(progress_file, 'w') as f:
                f.write(str(year) + '\n')
                f.write(state + '\n')
                f.write(district + '\n')
            log_timestamp(f"Started processing district {district}")
            dp_district = dp_state + str(district) + '/'

            # Check if the directory already exists
            if not os.path.exists(dp_district):
                os.makedirs(dp_district)

            for season in range(5):
                data = getStationsInDistrict(state, district, year, season)
                data = addLatLong(data)
                create_excel(data, year, state, district, dp_district, season)

            log_timestamp(f"Finished processing district {district}")

        log_timestamp(f"Finished processing state {state}")
        last_district = None
    log_timestamp(f"Finished processing year {year}")
    last_state = None

    

# You can also calculate and log the total time taken
log_timestamp("Script finished")
total_time = time.perf_counter() - start_time
log_timestamp(f"Total time taken: {total_time} seconds")
