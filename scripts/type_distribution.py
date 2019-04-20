import food_search_engine
import matplotlib.pyplot as plt

#get MK restaurant list
search_engine = food_search_engine.Food_Search_Engine("openrice_data.json")
filter_conditions = {"district": ["Mong Kok"]}
search_engine.filter(filter_conditions)
MK_restaurants_list = search_engine.query_result

#count restau of each type
cuisine_list = [] #list of all, one by one
counted_cdict={} #dict of how many/type
sorted_counted_cdict = [] #above in descending
final_cdict = [] #with others

for restaurant in MK_restaurants_list:
    for cuisine in restaurant['cuisine']:
        cuisine_list.append(cuisine)

counted_cdict=[[x,cuisine_list.count(x)] for x in set(cuisine_list)]

#rank them according to populatiry
sorted_counted_cdict = sorted(counted_cdict, key=lambda k: k[1],reverse=True)

#put [11:n] into "others"
i=0
other_counter=0
for item in sorted_counted_cdict:
    if i<10:
        final_cdict.append(item)
    else:
        other_counter+=item[1]
    i+=1

final_cdict.append(['other', other_counter])

#plot graph
labels = []
sizes = []

for item in final_cdict:
    labels.append(item[0])
    sizes.append(int(item[1]))

plt.pie(sizes, labels=labels,autopct='%1.1f%%')

plt.axis('equal')
plt.show()
