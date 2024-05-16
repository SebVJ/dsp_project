import pandas as pd
import requests
import json

df = pd.read_csv('latlongnew.csv')
df.info()
df.address


for i, row in df.iterrows():
    apiAddress = str(df.at[i, 'address']) + str(df.at[i, 'city'])

    parameters = {
            "key" : "UO8uxH6vNJ0BgSXSFD3G9I9pEvJv8BcE",
            "location" : apiAddress
    }

    response = requests.get("https://www.mapquestapi.com/geocoding/v1/address", params= parameters)
    data = json.loads(response.text)['results']
    
    lat = data[0]['locations'][0]['latLng']['lat']
    lng = data[0]['locations'][0]['latLng']['lng']
    df.at[i, 'lat'] = lat
    df.at[i, 'lng'] = lng
    print(lat, lng)

df.to_csv('geopoints.csv')
