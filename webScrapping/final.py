import os
from createTimeSeries import getYearlyDataForDistricts, mergeThroughYears, modifyDataForCSV, writeInCSV



directory_path = '/Users/manisarthak/Desktop/CGWB/'

def getYears(path):
    items = os.listdir(directory_path)
    directories = [int(item) for item in items if os.path.isdir(os.path.join(directory_path, item)) and item[0] != '.']
    directories.sort()
    return directories

years = getYears(directory_path)
# print(years)

def getStates(year):
    path = directory_path + str(year)+'/'
    items = os.listdir(path)
    directories = [item for item in items if os.path.isdir(os.path.join(path, item)) ]
    directories.sort()
    return directories



states = getStates(years[-1])
# print(states)


def getDistricts(state, year):
    path = directory_path + str(year)+'/'+str(state)+'/'
    items = os.listdir(path)
    directories = [item for item in items if os.path.isdir(os.path.join(path, item)) ]
    directories.sort()
    return directories



year = 2023
for state in states:
    print(f"starting state: {state}")
    districts = getDistricts(state, year)
    for district in district:
        data = mergeThroughYears(state, district, years[0], years[-1])
        data = modifyDataForCSV(data)
        writeInCSV(data, f"/Users/manisarthak/Desktop/CGWB/timeSeries/{state}_{district}.csv")
        break