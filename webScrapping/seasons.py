import requests
import numpy as np
import pandas as pd
import os

result_arr = []

state_arr = []

pre_monsoon_season_is_season1 = {
    "ANDAMAN & NICOBAR":"season1",
    "ARUNACHAL PRADESH":"season1",
    "ASSAM":"season1",
    "KERALA":"season1",
    "MANIPUR":"season1",
    "MEGHALAYA":"season1",
    "MIZORAM":"season1",
    "NAGALAND":"season1",
    "ODISHA":"season1",
    "SIKKIM":"season1",
    "TRIPURA":"season1",
    "WEST BENGAL":"season1",
}

seasonToSearch = "season4" 
year = "2017"

cookies = {
    'sc_is_visitor_unique': 'rx12644867.1678819081.AD7353D805EB4F50CF68D93BA38DDC20.8.8.8.8.8.8.7.7.7',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'sc_is_visitor_unique=rx12644867.1678819081.AD7353D805EB4F50CF68D93BA38DDC20.8.8.8.8.8.8.7.7.7',
    'Origin': 'https://wdo.indiawris.gov.in',
    # 'Referer': 'https://wdo.indiawris.gov.in/waterdataonline/gis/INDIA;locname=INDIA;loctype=COUNTRY;view=ADMIN;locuuid=00cb31c7-2928-4e6d-adcc-443d478c90d6;component=groundwater;src=STATE_AND_CENTRAL_STATION;type=Depth%20to%20water%20level%20%28DTW%29;format=season;seasonYear=2016;seasonType=season1;ytd=2022;mapOnClickParams=false;sDate=2016;eDate=2016;telementryfilter=All',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

json_data_INDIA = {
    'parentLocName': 'INDIA',
    'locname': 'INDIA',
    'loctype': 'COUNTRY',
    'view': 'ADMIN',
    'locuuid': '00cb31c7-2928-4e6d-adcc-443d478c90d6',
    'component': 'groundwater',
    'src': 'STATE_AND_CENTRAL_STATION',
    'type': 'Depth to water level (DTW)',
    'format': seasonToSearch,
    'seasonYear': year,
    'seasonType': seasonToSearch,
    'ytd': '2022',
    'mapOnClickParams': 'false',
    'sDate': year,
    'eDate': year,
    'telementryfilter': 'All',
    'cType': 'STATE',
    'pUUID': '00cb31c7-2928-4e6d-adcc-443d478c90d6',
    'lUUID': '00cb31c7-2928-4e6d-adcc-443d478c90d6',
    'lType': 'COUNTRY',
    'summary': False,
}

response_all_states = requests.post('https://wdo.indiawris.gov.in/api/gw/gwTable', cookies=cookies, headers=headers, json=json_data_INDIA, verify=False)

all_states = response_all_states.json()

for state in all_states:

    if 'uuid' not in state:
        continue

    state_name = state['name']
    state_uuid = state['uuid']

    num_in_state=0

    json_data_state = {
        'parentLocName': 'INDIA',
        'locname': state_name,
        'loctype': 'STATE',
        'view': 'ADMIN',
        'locuuid': state_uuid,
        'component': 'groundwater',
        'src': 'STATE_AND_CENTRAL_STATION',
        'type': 'Depth to water level (DTW)',
        'format': seasonToSearch,
        'seasonYear': year,
        'seasonType': seasonToSearch,
        'ytd': '2022',
        'mapOnClickParams': 'true',
        'sDate': year,
        'eDate': year,
        'telementryfilter': 'All',
        'cType': 'DISTRICT',
        'pUUID': state_uuid,
        'lUUID': state_uuid,
        'lType': 'STATE',
        'summary': False,
    }

    response_all_districts = requests.post('https://wdo.indiawris.gov.in/api/gw/gwTable', cookies=cookies, headers=headers, json=json_data_state, verify=False)

    all_districts = response_all_districts.json()

    for district in all_districts:

        if 'uuid' not in district:
            continue

        district_name = district['name']
        district_uuid = district['uuid']

        file_after_monsoon = state_name + "_" + district_name + "_" + district_uuid + "_" + seasonToSearch + "_" + year + ".csv"
        file_before_monsoon = state_name + "_" + district_name + "_" + district_uuid + "_" + "season2" + "_" + year + ".csv"
        if state_name in pre_monsoon_season_is_season1:
            file_before_monsoon = state_name + "_" + district_name + "_" + district_uuid + "_" + "season1" + "_" + year + ".csv"
        
        if(os.path.isfile(file_before_monsoon) and os.path.isfile(file_after_monsoon)):
            df_before = pd.read_csv(file_before_monsoon)
            df_after = pd.read_csv(file_after_monsoon)

            #print(df_before)
            #print(df_after)

            arr1 = df_before.to_numpy()
            arr2 = df_after.to_numpy()

            arr3 = []

            for station in arr1:
                for station2 in arr2:
                    if station[2]==station2[2]:
                        arr3.append([])
                        arr3[-1].append(station[1])
                        arr3[-1].append(station[2])
                        arr3[-1].append(station[3])
                        arr3[-1].append(station[4])
                        arr3[-1].append(station[5])
                        arr3[-1].append(station[6])
                        arr3[-1].append(station[7])
                        arr3[-1].append(station2[7])
                        break
            
            result_arr.append([])
            result_arr[-1].append(district_name)
            result_arr[-1].append(district_uuid)
            result_arr[-1].append(state_name)
            result_arr[-1].append(state_uuid)
            result_arr[-1].append(len(arr3))
            num_in_state += len(arr3)
            if len(arr3)==0:
                continue
            arr3 = np.array(arr3)
            df = pd.DataFrame(arr3,columns=["STATION_NAME","STATION_UUID","LATITUDE","LONGITUDE","STATE","DISTRICT","WATER LEVEL BEFORE MONSOON","WATER LEVEL AFTER MONSOON"])
            df.to_csv( "intersection/"  + state_name + "_" + district_name + "_" + district_uuid + "_" + year + ".csv")

            
    
    state_arr.append([])
    state_arr[-1].append(state_name)
    state_arr[-1].append(state_uuid)
    state_arr[-1].append(num_in_state)

    


if(len(result_arr)>0):
    result_arr = np.array(result_arr)
    df = pd.DataFrame(result_arr,columns=["DISTRICT_NAME","DISTRICT_UUID","STATE_NAME","STATE_UUID","NUMBER OF DATA POINTS IN DISTRICT"])
    df.to_csv("all_districts_count_" + year + ".csv")

if(len(state_arr)>0):
    state_arr = np.array(state_arr)
    df = pd.DataFrame(state_arr,columns=["STATE_NAME","STATE_UUID","NUMBER OF DATA POINTS IN STATE"])
    df.to_csv("all_states_count_" + year + ".csv")







    