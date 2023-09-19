import requests
import urllib3

# Disable SSL/TLS-related warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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




data = {"stnVal":{"qry":"select metadata.state_name, count(distinct(metadata.station_code)), coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and to_char(businessdata.date, \'yyyy-mm\') between \'2022-09\' and \'2023-09\'  group by metadata.state_name order by metadata.state_name"}}

response = requests.post(url, json=data, headers=headers, verify=False)

if response.status_code == 200:
    states = []
    response = response.json()
    for state_name in response:
        states.append(state_name[0])
    # print(states)
    for state_name in states:
        if (state_name != 'Bihar'):
            continue
        data = {
            "stnVal": {
                "qry": f"select metadata.district_name,count(distinct(businessdata.station_code)), coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state_name}' and to_char(businessdata.date, 'yyyy-mm') between '2022-09' and '2023-09'  group by district_name"
            }
        }
        response = requests.post(url, json=data, headers=headers, verify=False)
        if response.status_code == 200:
            response = response.json()
        else:
            print(state_name, "couldn't be found !")
            
        districts = []
        for district in response:
            districts.append(district[0])
        # print(state_name, districts)
        for district in districts:
            data = {"stnVal":{"qry":f"select metadata.station_name, metadata.station_code,coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'{state_name}\' and lower(metadata.district_name) = lower(\'{district}\') and to_char(businessdata.date, \'yyyy-mm\') between \'2022-09\' and \'2023-09\'  group by metadata.station_name, metadata.station_code"}}
            
            if state_name == 'Bihar':
                stations = requests.post(url, json=data, headers=headers, verify=False)
                if stations.status_code == 200:
                    stations = stations.json()
                    # print(district, stations)
                else:
                    print(state_name, "couldn't be found !")
            if district == 'Saran':
                print(stations)
                number = len(stations)
                final = []
                
                for i in range(number):
                    dp = stations[i]
                    
                    
                    
                    url = 'https://arc.indiawris.gov.in/server/rest/services/NWIC/GroundwaterLevel_Stations/MapServer/0/query'

                    headers = {
                        'authority': 'arc.indiawris.gov.in',
                        'accept': '*/*',
                        'accept-language': 'en-GB,en;q=0.9',
                        'origin': 'https://indiawris.gov.in',
                        'referer': 'https://indiawris.gov.in/',
                        'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'sec-gpc': '1',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                    }

                    params = {
                        'f': 'json',
                        'outFields': '*',
                        'spatialRel': 'esriSpatialRelIntersects',
                        'where': f'station_code = \'{str(int(dp[1]))}\'',
                    }
                    
                    response = requests.get(url, headers=headers, params=params)
                    
                    if response.status_code == 200:
                        print(response.json())
                        response = response.json()
                        # Assuming 'response' contains the JSON data you provided
                        data = response

                        # Access the 'features' list
                        features = data.get('features', [])

                        # Check if there are any features
                        if features:
                            # Extract the latitude and longitude from the first feature
                            first_feature = features[0]
                            attributes = first_feature.get('attributes', {})
                            
                            # Extract the latitude and longitude
                            latitude = attributes.get('lat')
                            longitude = attributes.get('long')
                            
                            if latitude is not None and longitude is not None:
                                # print(f"Latitude: {latitude}")
                                # print(f"Longitude: {longitude}")
                                dp.append(latitude)
                                dp.append(longitude)
                            else:
                                print("Latitude or Longitude data is missing.")
                        else:
                            print("No features found in the JSON data.")

                        
                    else:
                        print(f"Request failed with status code {response.status_code}")
                        
                    final.append(dp)
                print(final)


                
        
        
else:
    print(f"Request failed with status code {response.status_code}")



"""
curl 'https://arc.indiawris.gov.in/server/rest/services/NWIC/GroundwaterLevel_Stations/MapServer/0/query?f=json&outFields=*&spatialRel=esriSpatialRelIntersects&where=station_code%20%3D%20%27254904084413401%27' \
  -H 'authority: arc.indiawris.gov.in' \
  -H 'accept: */*' \
  -H 'accept-language: en-GB,en;q=0.9' \
  -H 'origin: https://indiawris.gov.in' \
  -H 'referer: https://indiawris.gov.in/' \
  -H 'sec-ch-ua: "Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
  --compressed
"""