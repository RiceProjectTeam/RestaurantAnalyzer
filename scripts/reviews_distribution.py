import food_search_engine
import matplotlib.pyplot as plt

#get TST rest
search_engine = food_search_engine.Food_Search_Engine("openrice_data.json")
filter_conditions = {"district": ["Tsim Sha Tsui"]}
search_engine.filter(filter_conditions)
TST_restaurants_list = search_engine.query_result


#x-axis is the number of reviews
no_of_reviews_list = []
for restaurant in TST_restaurants_list:
    #get no of reviews
    no_of_reviews = int(restaurant['reviews'][0]) + int(restaurant['reviews'][1])+int(restaurant['reviews'][2])

    no_of_reviews_list.append(no_of_reviews)

#plot histogram
num_bins = 10
n, bins, patches = plt.hist(no_of_reviews_list,  num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Number of reviews')
plt.ylabel('Number of restaurants')
plt.title('Distribution of number of reviews in TST')
plt.show()