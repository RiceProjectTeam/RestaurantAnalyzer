import food_search_engine
import re
import matplotlib.pyplot as plt

#get MK restaurants
search_engine = food_search_engine.Food_Search_Engine("openrice_data.json")
filter_conditions = {"district": ["Mong Kok"]}
search_engine.filter(filter_conditions)
MK_restaurants_list = search_engine.query_result

#getting list of prices and review no
var_list = [] #[[price,no reviews]]
for restaurant in MK_restaurants_list:
    #get price
    price_str = restaurant['price_range']
    pricerangelist = re.findall(r'\d+', price_str)

    # for above 800 and below 50
    if (len(pricerangelist) < 2):
        if (re.findall(r'Below', price_str)):
            lowprice = 0
            highprice = float(pricerangelist[0])
        if (re.findall(r'Above', price_str)):
            lowprice = float(pricerangelist[0])
            highprice = 1000
    else:
        lowprice = float(pricerangelist[0])
        highprice = float(pricerangelist[1])
    price = (lowprice + highprice) / 2

    #get no of reviews
    no_of_reviews = int(restaurant['reviews'][0]) + int(restaurant['reviews'][1])+int(restaurant['reviews'][2])

    var_list.append([price,no_of_reviews])

#scatter plot
x=[]
y=[]
for item in var_list:
    x.append(item[0])
    y.append(item[1])

# Plotting
plt.scatter(x, y, alpha=0.2)
plt.title('Price vs Popularity')
plt.xlabel('Price(HK$)')
plt.ylabel('No. of reviews')
plt.show()