import gmplot
import requests
import food_search_engine
import re

key = " AIzaSyCKZ5Ui1UJZmgvkCiRu0Siv1nvDIePGnuU "

#restaurant IN SHA TIN
search_engine = food_search_engine.Food_Search_Engine("openrice_data.json")
filter_conditions = {"district": ["Sha Tin"]}
search_engine.filter(filter_conditions)
shatin_restaurants_list = search_engine.query_result

#========adding distance var tp restaurants

min_35_restaurants=[]
min_60_restaurants=[]

def add_time_var(restaurant, gmaps_json):
    try:
        time_str = gmaps_json['rows'][0]['elements'][0]['duration']['text']
        time = int(re.search(r'\d+', time_str).group())

        if 'hour' in time_str:
            time +=59

        restaurant['time'] = time

        if restaurant['time'] <= 35:
            min_35_restaurants.append(restaurant['address'])
        elif restaurant['time'] <= 60:
            min_60_restaurants.append(restaurant['address'])
    except:
        None
#==========END ranking

# you might want a for loop to send and receive the query
for restaurant in shatin_restaurants_list:
    query = "units=metric&origins=22.4179252,114.2027235&destinations="\
            +restaurant['address'][0]+","+restaurant['address'][1]\
            +"&mode=transit&departure_time=1512102900"\
            +"&key="+key
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + query
    response = requests.get(url).json()

    add_time_var(restaurant,response)

#get latlng
latitude_list35=[]
longitude_list35=[]
for latlng in min_35_restaurants:
    latitude_list35.append(float(latlng[0]))
    longitude_list35.append(float(latlng[1]))

latitude_list60=[]
longitude_list60=[]
for latlng in min_60_restaurants:
    latitude_list60.append(float(latlng[0]))
    longitude_list60.append(float(latlng[1]))

#plot scatter of ShaTin restaurants
gmap = gmplot.GoogleMapPlotter(22.395607,114.1963153, 14)

gmap.scatter(latitude_list35, longitude_list35, '#0000ff', size=40, marker=False)
gmap.scatter(latitude_list60, longitude_list60, '#ff0000', size=40, marker=False)

gmap.draw("Restaurant Radius.html")

