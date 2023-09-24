import requests
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    print ("response asked !!")
    if response.status_code == 200:
        response = response.json()
        # print(response)
    else:
        print(state_name, "couldn't be found !")
        
    districts = [x[0] for x in response]
    return districts



def getStationsInDistrict(state_name, district, year, code):
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
    if code == 0:
        data = {"stnVal":{"qry":f"select metadata.station_name, metadata.station_code,coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'{state_name}\' and lower(metadata.district_name) = lower(\'{district}\') and to_char(businessdata.date, \'yyyy\') between \'{year}\' and \'{year}\'  group by metadata.station_name, metadata.station_code"}}
    else :
        x = [(None, None), ("01", "03"), ("04", "06"), ("07", "09"), ("10", "12")]
        data = {"stnVal":{"qry":f"select metadata.station_name, metadata.station_code,coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'{state_name}\' and lower(metadata.district_name) = lower(\'{district}\') and to_char(businessdata.date, \'yyyy-mm\') between \'{year}-{x[code][0]}\' and \'{year}-{x[code][1]}\'  group by metadata.station_name, metadata.station_code"}}
    
    stations = requests.post(url, json=data, headers=headers, verify=False)
    if stations.status_code == 200:
        stations = stations.json()
        # print(district, stations)
    else:
        print(state_name, "couldn't be found !")  
        
    return stations  
        


        
def getLatLong(station_id):
    
    # station_id = int(station_id)
    
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
        'where': f'station_code = \'{station_id}\'',
    }
    
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response = response.json()
        data = response
        features = data.get('features', [])
        if features:
            first_feature = features[0]
            attributes = first_feature.get('attributes', {})
            latitude = attributes.get('lat')
            longitude = attributes.get('long')
            if latitude is not None and longitude is not None:
                return latitude, longitude
    return None, None
    

def addLatLong(data):
    #   ['Ammi', '254430084574501', 4.35]
    new_data = []
    for x in data:
        station_id = x[1]
        (lat, long) = getLatLong(station_id)
        new_data.append(x + [lat, long])
    return new_data

# print(getStates())
# print(getDistricts('Bihar'))
# print(getStationsInDistrict('Bihar', 'Saran'))
# print(getLatLong(254904084413401))


def create_excel(data, year, state, district, loc, season = None):
    columns = ["station_name", "station_id", "water_level (in m)", "lat", "long"]
    df = pd.DataFrame(data, columns = columns)
    if season != 0:
        excel_file = loc + f"{district}_{state}_{year}_{season}.xlsx"
    else:
        excel_file = loc + f"{district}_{state}_{year}_yearly.xlsx"
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        # print(df)
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    print("file written", loc)
        
# print(getLatLong('CGWHYD0398'))

if __name__ == "__main__":
    import os
    directory_path = "/Users/manisarthak/Desktop/CGWB/"
    os.makedirs(directory_path)
    for year in range(2023, 2000, -1):
        dp_year = directory_path + str(year) + '/'
        os.makedirs(dp_year)
        states = getStates()
        for state in states:
            # if state != 'Karnataka':
            #     continue
            dp_state = dp_year + str(state) + '/'
            os.makedirs(dp_state)
            districts = getDistricts(state)
            for district in districts:
                # if district != 'Mandya':
                #     continue
                dp_district = dp_state + str(district) + '/'
                os.makedirs(dp_district)
                for season in range(5):
                    data = getStationsInDistrict(state, district, year, season)
                    data = addLatLong(data)
                    create_excel(data, year, state, district, dp_district, season)
                    
                    
                
                
    
    
    