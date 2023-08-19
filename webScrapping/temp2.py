import requests

seasonToSearch = "season4" # 'season1' is Jan-March 'season2' is Apr-Jun 'season4' is Oct-Dec
year = "2018" # year 

cookies = {
    'sc_is_visitor_unique': 'rx12644867.1691945728.DD595E9F2C834F669C296050D901D4C1.2.2.2.2.2.2.2.2.2',
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
    print(state)