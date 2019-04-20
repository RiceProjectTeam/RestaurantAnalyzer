import numpy as np
import matplotlib.pyplot as plt
import json
from food_search_engine import Food_Search_Engine

#find restaurants in ShaTin
#creating an object of the Food Search Engine
json_file_name = "openrice_data.json"
fse = Food_Search_Engine(json_file_name)
top_10_restaurants_shatin = list()
all_shatin_retaurants = list()

fse.filter({'district':['Sha Tin']})
#fse.print_query_result()

#turning the string list of reviews to int and then finding the sum, adding that to the attributes of the dictionaries in query_results
list_of_reviews = list()
for reviews in fse.query_result:
    temp_list = reviews['reviews']
    temp_list_int = list(map(int,temp_list))
    list_of_reviews.append(sum(temp_list_int))
    #print(temp_list_int)

#sorting the list by number of reviews
i = 0
for restaurants in fse.query_result:
    restaurants['total-reviews'] = list_of_reviews[i]
    i+=1

sorted_list = sorted(fse.query_result, key=lambda k: k['total-reviews'], reverse=True)
#N = 10

#storing the top ten restaurants and their corresponding number of reviews
results = sorted_list[:10]
#print (results)
list_of_most_reviews = list()
list_of_top_restaurants = list()



for items in results:
    list_of_most_reviews.append(items['total-reviews'])
    list_of_top_restaurants.append(items['name'])


list_of_top_restaurants.reverse()
list_of_most_reviews.reverse()
#print(list_of_top_restaurants)
#print(list_of_most_reviews)

#GETTING BAR CHART

plt.barh( range(len(list_of_top_restaurants)), list_of_most_reviews)
plt.yticks(range(len(list_of_top_restaurants)),list_of_top_restaurants)
#plt.yticks( list_of_most_reviews)



plt.xlabel('No of reviews')
plt.title('Most Popular Restaurants in Sha Tin')

plt.show()