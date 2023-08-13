import requests





response = requests.post("https://arc.indiawris.gov.in/server/rest/services/Common/Administrative_SOI/MapServer/1?f=json").json()

states = response["fields"][2]['domain']['codedValues']

for key in states :
    response = requests.post("https://arc.indiawris.gov.in/server/rest/services/Common/Administrative_SOI/MapServer/1/query?f=json&orderByFields=district&outFields=*&spatialRel=esriSpatialRelIntersects&where=state%20%3D%20%27{}%27".format(key['code'])).json()
    print(key['name'], key['code'], len(str(response).encode('utf-8')))
    if (key['code'] == 'DD'):
        # print(response)
        print (10 )


# """
# https://arc.indiawris.gov.in/server/rest/services/NWIC/WQ_Station/MapServer/4/query?f=json&orderByFields=sub_basin&outFields=*&spatialRel=esriSpatialRelIntersects&where=bacode%20%3D%20%2718%27
# """