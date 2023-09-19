import requests

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
    'where': 'station_code = \'254904084413401\'',
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
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
        else:
            print("Latitude or Longitude data is missing.")
    else:
        print("No features found in the JSON data.")

    
else:
    print(f"Request failed with status code {response.status_code}")
