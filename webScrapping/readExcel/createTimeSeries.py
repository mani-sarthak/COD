import os
import glob
import csv
from yearly import *
import copy
import pandas as pd
import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = "/Users/manisarthak/Library/CloudStorage/OneDrive-IITDelhi/ACADEMICS/Semester5/COD/webScrapping/timeSeriesData/"


def readFromExcel(state, district, year, season, directory_path = "/Users/manisarthak/Desktop/CGWB/"):
    excel_path = directory_path + f"{year}/{state}/{district}/{district}_{state}_{year}_{season}.xlsx"
    scam = []
    try:
        df = pd.read_excel(excel_path, header=None)
        scam = df.values.tolist()[1:]
    except Exception as e:
        print("Error --- \n", year, state, district, season)
        print(e)
    return scam

## single district single year

def getYearlyDataForDistricts(year, state, district):
    """
    Returns a dictionary containing the station_id as 
    key and a list of station_name, lat, long, water_level
    for each season as value.
    
    None means data not available for that well in that season
    """
    data = dict()
    temp_data = []
    for season in range(1, 5):
        scam = readFromExcel(state, district, year, season)
        print(year, state, district, season, 'done')
        # print(scam, end = "\n\n\n\n")
        temp_data.append(scam)
        for x in scam:
            station_id = x[1]
            station_name = x[0]
            strtion_latitude = x[3]
            station_longitude = x[4]
            water_level = x[2]
            if station_id not in data:
                data[station_id] = [station_name, strtion_latitude, station_longitude]
            elif data[station_id][0] !=  station_name:
                print("some big error in the website or data fetching !!   check data")
                print(year, state, district, season)
                
    for seasonally in temp_data:
        data_cpy = copy.deepcopy(data)
        for x in seasonally:
            station_id = x[1]
            water_level = x[2]
            if station_id in data:
                data[station_id].append(water_level)
                data_cpy.pop(station_id)
        for x in data_cpy:
            data[x].append(None)
            # for k in data:
            #     print(k, data[k][3:])        
    print(year, state, district, 'done\n\n') 
    return data


# single district through years

def mergeThroughYears(state, district, start_year=2010, end_year=2012)   :
    data = dict()
    data['station_id'] = ['station_name', 'latitude', 'longitude']
    temp_data = []
    for year in range(start_year, end_year+1):
        yearly_data_dict = getYearlyDataForDistricts(year, state, district)
        temp_data.append(yearly_data_dict)
        for x in yearly_data_dict:
            station_id = x
            station_name = yearly_data_dict[x][0]
            strtion_latitude = yearly_data_dict[x][1]
            station_longitude = yearly_data_dict[x][2]
            if station_id not in data:
                data[station_id] = [station_name, strtion_latitude, station_longitude]
            elif data[station_id][0] !=  station_name:
                print("some big error in the website or data fetching !!   check data")
                print(year, state, district)
                break
    year = start_year
    for yearly in temp_data:
        data_cpy = copy.deepcopy(data)
        for season in range(1, 5):
            data['station_id'].append(f"{year}_season{season}")
        for x in yearly:
            station_id = x
            water_level = yearly[x][3:]
            season += 1
            if station_id in data:
                data[station_id] += water_level
                data_cpy.pop(station_id)
        for x in data_cpy:
            if x != 'station_id':
                data[x] += ([None]*4)
        year+=1
    print(state, district, f'done from {start_year} to {end_year}\n\n\n\n')        
    return data
       
       
def modifyDataForCSV(data):
    final_dict = dict()
    final_dict['station_id'] = []
    idx_dict = dict()
    i = 0
    for k in data['station_id']:
        idx_dict[i] = k
        i += 1
        final_dict[k] = []
    for k in data:
        if k == 'station_id':
            continue
        final_dict['station_id'].append(k)
        for i in range(len(data[k])):
            final_dict[idx_dict[i]].append(data[k][i])
    return final_dict
       


def writeInCSV(data, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the dict
        for i in range(len(data['station_id'])):
            row = {field: data[field][i] for field in fieldnames}
            writer.writerow(row)

    print(f'Data saved to {csv_file}')






# # say calculating for bhilwara
# state = 'Rajasthan'
# district = 'Bhilwara'
# data = mergeThroughYears(state, district, 2010, 2011)
# data = modifyDataForCSV(data)
# writeInCSV(data, path+f"{state}_{district}.csv")




def getStates(year):
    url = 'https://indiawris.gov.in/gwlbusinessdata'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Access-Control-Allow-Methods': 'GET,POST',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://indiawris.gov.in',
        'Referer': 'https://indiawris.gov.in/wdo/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }



    data = {"stnVal":{"qry":f"select metadata.state_name, count(distinct(metadata.station_code)), coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and to_char(businessdata.date, \'yyyy-mm\') between \'{year}-01\' and \'{year}-12\'  group by metadata.state_name order by metadata.state_name"}}

    response = requests.post(url, json=data, headers=headers, verify=False)

    states = []
    if response.status_code == 200:
        response = response.json()
        for state_name in response:
            states.append(state_name[0])
    return states


def getDistricts(state_name, year):
    url = 'https://indiawris.gov.in/gwlbusinessdata'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Access-Control-Allow-Methods': 'GET,POST',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://indiawris.gov.in',
        'Referer': 'https://indiawris.gov.in/wdo/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    
    
    data = {
            "stnVal": {
                "qry": f"select metadata.district_name,count(distinct(businessdata.station_code)), coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state_name}' and to_char(businessdata.date, 'yyyy') between '{year}' and '{year}'  group by district_name"
            }
        }
    
    
    response = requests.post(url, json=data, headers=headers, verify=False)
    if response.status_code == 200:
        response = response.json()
        # print(response)
    else:
        print(state_name, "couldn't be found !")
        
    districts = [x[0] for x in response]
    return districts

progress_file = path + "progress.txt"
log_file = path + "log.txt"
last_state = None
last_district = None


# Function to log timestamps and calculate time taken
def log_timestamp(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")



if os.path.isfile(progress_file):
    with open(progress_file, 'r') as f:
        last_state = f.readline().strip()
        last_district = f.readline().strip()
    log_timestamp(f"Resuming from district {last_district}, state {last_state}")



current_year = 2023
# states = getStates(current_year)
states = ['Madhya Pradesh']
d = set()
# print(states)
# if last_state:
#     states = states[states.index(last_state):]
for state in states:
    # if state != 'Rajasthan':
    #     continue
    # districts = getDistricts(state, current_year)
    districts = ['Guna', 'Khandwa']
    # districts = ['Dumka', 'Ramgarh']
    # print(districts)
    # if last_district:
    #     districts = districts[districts.index(last_district):]
    for district in districts:
        # if district != 'Bhilwara':
        #     continue
        d.add((state, district))
        try:
            data = mergeThroughYears(state, district, 2010, 2021)
            data = modifyDataForCSV(data)
            with open(progress_file, 'w') as f:
                f.write(state + '\n')
                f.write(district + '\n')
            log_timestamp(f"Started processing district {district} of state {state}")
            writeInCSV(data, path+f"{state}_{district}.csv")
            # d.clear((state, district))
        except Exception as e:
            print(e)
            print("error in writing csv file for district ", district, " of state ", state)
            # print(data)
            break
print("districts left to be processed\n\n\n\n\n")
for k in d:
    print(k)        
            














