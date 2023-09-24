from yearly import *


# get states (year)
# get districts (state, year)
# get station in districts (state, district, year, season)
# get latLong (station_id)




start_year = 2010
end_year = 2020


for year in range(start_year, end_year):
    states = getStates(year)
    # print(states, len(states), end = "\n\n")
    for state in states:
        if (state != 'Rajashtan'):
            # print(state)
            continue
        print(state)
        districts = getDistricts(state, year)
        # print(districts)
        for district in districts:
            if (district != 'Bhilwara'):
                continue
            for season in range(1, 5):
                data = getStationsInDistrict(state, district, year, season)
                # data = addLatLong(data)
                # create_excel(data, year, state, district, season)
                print(year, state, district, season)
                print(data, end = "\n\n\n\n")
    