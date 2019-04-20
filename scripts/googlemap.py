import food_search_engine
import gmplot

#get Jap restaurant list
search_engine = food_search_engine.Food_Search_Engine("openrice_data.json")
filter_conditions = {"cuisine": ["Japanese"]}
search_engine.filter(filter_conditions)
jap_restaurant_list = search_engine.query_result

#get latlng
latitude_list=[]
longitude_list=[]
for restaurant in jap_restaurant_list:
    latitude_list.append(float(restaurant['address'][0]))
    longitude_list.append(float(restaurant['address'][1]))

#plot heatmap of Japanese cusine in all areas

gmap = gmplot.GoogleMapPlotter(22.325222,114.1664163, 12)
#gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)

gmap.heatmap(latitude_list,longitude_list )

gmap.draw("Japanese Restaurant Heatmap.html")
