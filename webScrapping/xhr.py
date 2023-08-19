import requests
requests.packages.urllib3.disable_warnings()  # Disable SSL warnings
url = "https://indiawris.gov.in/wris/#/groundWater"  # Replace with the actual XHR request URL



response = requests.get(url, verify = False)

if response.status_code == 200:
    # data = response.json()  # Use .text for raw text or .json() for JSON response
    print(response.text)
else:
    print("Request failed with status code:", response.status_code)
