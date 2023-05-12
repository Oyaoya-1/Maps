import requests
from math import radians, cos, sin, asin, sqrt

access_token = "pk.eyJ1IjoibW9vbmExIiwiYSI6ImNsZnl0ZWtucTBxa3Iza21rZmE4cTN0dmYifQ.NsR-Z8cBogNeJYsanz5xwQ"

#fungsi untuk menghitung jarak antara dua titik geografis
def distance(lat1, lat2, lon1, lon2):
     
    # Modul matematika bermuat fungsi bernama
    # radian yang mengonversi dari derajat ke radian.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # formula Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius bumi dalam kilometer. Gunakan 3956 untuk mil
    r = 6371
      
    # kalkulasikan hasil
    return(c * r)

#fungsi untuk mengkonversi km ke mil
def km_mil(km):
    return km *0.621371

#endpoint api spacex untuk mendapat daftar peluncuran
launches_url = "https://api.spacexdata.com/v4/launches"
response = requests.get(launches_url)
launches = response.json()[-20:] #untuk mengambil 20 data terakhir

# loop setiap peluncuran
for launch in launches:
    launchpad_id = launch["launchpad"]
    #untuk mendapatkan fullname peluncuran
    launchpad_url = f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}"
    response = requests.get(launchpad_url)
    launchpad = response.json()
    launchpad_fullname = launchpad["full_name"]
    launchpad_lat, launchpad_lon = launchpad["latitude"], launchpad["longitude"]
    #endpoint geocoding mapbox untuk mendapatkan koordinat geografis launchpad
    geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{launchpad_fullname}.json?access_token={access_token}"
    geo_response = requests.get(geo_url)
    geo_json = geo_response.json()
    if len(geo_json["features"]) == 0:
        print(f"koordinat untuk {launchpad_fullname} tidak ditemukan")
        continue
    mapbox_lat, mapbox_lon = geo_json["features"][0]["center"]
    #perbedaan dalam km antara hasil geocoding mapbox dan posisi spacex
    distance_km = distance(mapbox_lat, launchpad_lat, mapbox_lon, launchpad_lon)
    distance_mil = km_mil(distance_km)

    #hasil
    print(f"tanggal peluncuran: {launch['date_local']}")
    print(f"fullname peluncuran: {launchpad_fullname}")
    print(f"perbedaan dalam mil: {distance_mil:.2f}")
    print(f"perbedaan dalam km; {distance_km:.2f}\n")
