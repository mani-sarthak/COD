import requests

seasonToSearch = "season4" # 'season1' is Jan-March 'season2' is Apr-Jun 'season4' is Oct-Dec
year = "2018" # year 

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

all_states = response_all_states.json()  # All States data and uuid

for state in all_states:

    if 'uuid' not in state:
        continue

    state_name = state['name']
    state_uuid = state['uuid']

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

    all_districts = response_all_districts.json()  # All districts in the state

    for district in all_districts:

        if 'uuid' not in district:
            continue

        district_name = district['name']
        district_uuid = district['uuid']  # distict uuid

        json_data_district = {
            'parentLocName': 'INDIA',
            'locname': district_name,
            'loctype': 'DISTRICT',
            'view': 'ADMIN',
            'locuuid': district_uuid,
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
            'cType': 'STATION',
            'pUUID': district_uuid,
            'lUUID': district_uuid,
            'lType': 'DISTRICT',
            'summary': False,
        }

        response_all_stations = requests.post('https://wdo.indiawris.gov.in/api/gw/gwTable', cookies=cookies, headers=headers, json=json_data_district, verify=False)

        all_stations = response_all_stations.json()   # All the stations in the district

        arr = []

        for station in all_stations:
            #print(station)
            if 'uuid' not in station:
                continue
            if 'groundWaterObject' not in station:
                continue
            arr.append([])
            arr[-1].append(station['name'])
            arr[-1].append(station['uuid'])
            arr[-1].append(station['lat'])
            arr[-1].append(station['lng'])
            arr[-1].append(station['st'])
            arr[-1].append(station['dt'])
            if 'groundWaterObject' in station:
                arr[-1].append(station['groundWaterObject']['currentLevel'])
            else:
                arr[-1].append('-')
        
        import numpy as np
        arr = np.array(arr)
        import pandas as pd
        if len(arr)==0:
            continue
        df = pd.DataFrame(arr,columns=["STATION_NAME","STATION_UUID","LATITUDE","LONGITUDE","STATE","DISTRICT","CURRENT WATER LEVEL"])
        df.to_csv( state_name + "_" + district_name + "_" + district_uuid + "_" + seasonToSearch + "_" + year + ".csv")  #Save file with the name





    