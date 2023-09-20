import os
from yearly import *
directory_path = "/Users/manisarthak/Desktop/CGWB/"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

progress_file = "progress.txt"

last_year = 2023
last_state = None
last_district = None

if os.path.isfile(progress_file):
    with open(progress_file, 'r') as f:
        last_year = int(f.readline().strip())
        last_state = f.readline().strip()
        last_district = f.readline().strip()
print(last_year, last_state, last_district)
for year in range(last_year, 2000, -1):
    dp_year = directory_path + str(year) + '/'
    if not os.path.exists(dp_year):
        os.makedirs(dp_year)

    states = getStates()

    if last_state:
        states = states[states.index(last_state):]

    for state in states:
        dp_state = dp_year + str(state) + '/'
        if not os.path.exists(dp_state):
            os.makedirs(dp_state)

        districts = getDistricts(state)

        if last_district:
            districts = districts[districts.index(last_district):]

        for district in districts:
            with open(progress_file, 'w') as f:
                f.write(str(year) + '\n')
                f.write(state + '\n')
                f.write(district + '\n')
            dp_district = dp_state + str(district) + '/'
            if not os.path.exists(dp_district):
                os.makedirs(dp_district)

            for season in range(5):
                data = getStationsInDistrict(state, district, year, season)
                data = addLatLong(data)
                create_excel(data, year, state, district, dp_district, season)

        last_district = None
    last_state = None
