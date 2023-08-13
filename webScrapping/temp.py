import requests


response = requests.post("https://arc.indiawris.gov.in/server/rest/services/Common/Administrative_SOI/MapServer/1/query?f=json&orderByFields=district&outFields=*&spatialRel=esriSpatialRelIntersects&where=state%20%3D%20%27DD%27")


"""

https://arc.indiawris.gov.in/server/rest/services/Common/Administrative_SOI/MapServer/1?f=json
"""




response = requests.post("https://arc.indiawris.gov.in/server/rest/services/Common/Administrative_SOI/MapServer/1?f=json").json()

states = response["fields"][2]['domain']['codedValues']

for ky in states :
    print(ky['name'], ky['code'])


# """
# https://arc.indiawris.gov.in/server/rest/services/NWIC/WQ_Station/MapServer/4/query?f=json&orderByFields=sub_basin&outFields=*&spatialRel=esriSpatialRelIntersects&where=bacode%20%3D%20%2718%27
# """