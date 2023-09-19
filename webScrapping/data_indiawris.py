import requests
import pandas as pd
import time


def get_data(state,district,year,number):
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
    if number==1:
        data = {
            "stnVal": {
                "qry": f"select metadata.station_name, metadata.station_code, coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state}' and lower(metadata.district_name) = lower('{district}') and to_char(businessdata.date, 'yyyy-mm') between '{year}-01' and '{year}-03'  group by metadata.station_name, metadata.station_code"
            }
        }
    elif number==2:
        data = {
            "stnVal": {
                "qry": f"select metadata.station_name, metadata.station_code, coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state}' and lower(metadata.district_name) = lower('{district}') and to_char(businessdata.date, 'yyyy-mm') between '{year}-04' and '{year}-06'  group by metadata.station_name, metadata.station_code"
            }
        }
    elif number==3:
        data = {
            "stnVal": {
                "qry": f"select metadata.station_name, metadata.station_code, coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state}' and lower(metadata.district_name) = lower('{district}') and to_char(businessdata.date, 'yyyy-mm') between '{year}-07' and '{year}-09'  group by metadata.station_name, metadata.station_code"
            }
        }
    elif number == 10:
        data = {"stnVal":{"qry":"select metadata.district_name,count(distinct(businessdata.station_code)), coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'Bihar\' and to_char(businessdata.date, \'yyyy-mm\') between \'2022-09\' and \'2023-09\'  group by district_name"}}
    else:
        data = {
            "stnVal": {
                "qry": f"select metadata.station_name, metadata.station_code, coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = 'CGWB' and metadata.state_name = '{state}' and lower(metadata.district_name) = lower('{district}') and to_char(businessdata.date, 'yyyy-mm') between '{year}-10' and '{year}-12'  group by metadata.station_name, metadata.station_code"
            }
        }
        

    response = requests.post(url, json=data, headers=headers ,verify=False)

    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        if len(json_response) == 0:
            return
        print(json_response)
        df = pd.DataFrame(json_response, columns=["Station", "Station Code", "Level (m)"])

    # Create a Pandas Excel writer using XlsxWriter as the engine.
        excel_file = f"{district} {year} s{number}.xlsx"
        with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            # Add the header in cell A1 with formatting.
            worksheet.write("A1", "Station Ground Water Level Information")
            header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
            worksheet.merge_range('A1:C1', "Station Ground Water Level Information", header_format)

            # Set the column width to auto-adjust based on the content.
            cell_format = workbook.add_format({'bold': True,'align': 'center'})
            worksheet.write('A2', 'Station', cell_format)
            # header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
            worksheet.write("B2", "Station Code",cell_format)
            worksheet.write("C2", "Level (m)",cell_format)
            
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)  # Adding 2 for padding
                worksheet.set_column(i, i, column_len)

        print(f"Data saved to {excel_file}")
    else:
        print(f"Request failed with status code {response.status_code}")



# states=['Karnataka']
# districts=['Mandya']
# years=[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009]
# for state in states:
#     for district in districts:
#         for number in range(1,5):
#             for year in years:
#                 get_data(state,district,year,number)
#                 # time.sleep(15)
                
                
states=['Bihar']
districts=['Ammi']
years=[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009]
for state in states:
    for district in districts:
        for number in range(1,5):
            for year in years:
                get_data(state,district,year,10)
                # time.sleep(15)
                
                

print(get_data(1, 2, 3, 10))



"""
curl 'https://indiawris.gov.in/gwlbusinessdata' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-GB,en;q=0.9' \
  -H 'Access-Control-Allow-Methods: GET,POST' \
  -H 'Access-Control-Allow-Origin: *' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://indiawris.gov.in' \
  -H 'Referer: https://indiawris.gov.in/wdo/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw $'{"stnVal":{"qry":"select metadata.station_name, metadata.station_code,coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'Karnataka\' and lower(metadata.district_name) = lower(\'Mandya\') and to_char(businessdata.date, \'yyyy\') between \'2023\' and \'2023\'  group by metadata.station_name, metadata.station_code"}}' \
  --compressed
"""


"""
curl 'https://indiawris.gov.in/gwlbusinessdata' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-GB,en;q=0.9' \
  -H 'Access-Control-Allow-Methods: GET,POST' \
  -H 'Access-Control-Allow-Origin: *' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://indiawris.gov.in' \
  -H 'Referer: https://indiawris.gov.in/wdo/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw $'{"stnVal":{"qry":"select metadata.station_name, metadata.station_code,coalesce(ROUND(AVG(businessdata.level)::numeric,2), 0) from public.groundwater_station as metadata INNER JOIN public.gwl_timeseries_data as businessdata on metadata.station_code = businessdata.station_code where 1=1  and metadata.agency_name = \'CGWB\' and metadata.state_name = \'Karnataka\' and lower(metadata.district_name) = lower(\'Mandya\') and to_char(businessdata.date, \'yyyy-mm\') between \'2023-01\' and \'2023-03\'  group by metadata.station_name, metadata.station_code"}}' \
  --compressed
"""