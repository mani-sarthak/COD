from yearly import *
import copy
import pandas as pd

start_year = 2010
end_year = 2011




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
        scam = getStationsInDistrict(state, district, year, season)
        # scam = addLatLong(scam)
        # create_excel(scam, year, state, district, season)
        
        scam = addLatLong(scam)
        print(year, state, district, season, 'done\n')
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
            
    return data



def mergeThroughYears(state, district, start_year=2010, end_year=2012)   :
    data = dict()
    data['station_id'] = ['station_name', 'latitude', 'longitude']
    temp_data = []
    for year in range(start_year, end_year):
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
            data['station_id'].append(f"{year}_{season}")
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
            
            
    return data
                
        
                 
            
            
            
if __name__ == "__main__":
    data = mergeThroughYears( 'Rajasthan', 'Bhilwara')
    df = pd.DataFrame(data)
    print(df)
    df = pd.DataFrame.from_dict(data, orient='index')
    print(df)
    excel_file = 'Bhilwara_Rajasthan.xlsx'
    df.to_excel(excel_file, sheet_name="Sheet1", index=False)
    try:
        df.to_csv('Bhilwara_Rajasthan.csv', index=False)
    except:
        print("csv not done")
        
    try:
        df.to_json('Bhilwara_Rajasthan.json', orient='records')
    except:
        print("json not done")