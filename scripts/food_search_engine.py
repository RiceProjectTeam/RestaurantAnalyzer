import json
import math
import re

class Food_Search_Engine:
    # original data from crawled json file
    original_data = []
    # the result after filter/ranking
    query_result = []

    def __init__(self, json_file_name):
        self.load_data(json_file_name)
        self.reset()

    def load_data(self, json_file_name):
        with open(json_file_name) as json_data:
            self.original_data = json.load(json_data)

    def reset(self):
        self.query_result = list(self.original_data)
    #==================END RESET=====================================

    def filter(self, filter_cond):
        #filtering name_contains
        a = list()
        if("name_contains" in filter_cond):
            for allowed_name in filter_cond['name_contains']:
                for restaurant in self.query_result:
                    if allowed_name in restaurant['name']:
                        a.append(restaurant)
        else:
            a=self.query_result

        # filtering name
        b = list()
        if ("name" in filter_cond):
            for allowed_exact_name in filter_cond['name']:
                for restaurant in a:
                    if allowed_exact_name == restaurant['name']:
                        b.append(restaurant)
        else:
            b = a

        # filtering district
        c = list()
        if ("district" in filter_cond):
            for allowed_district in filter_cond['district']:
                for restaurant in b:
                    if allowed_district == restaurant['district']:
                        c.append(restaurant)
        else:
            c = b

        # filtering cuisine
        d = list()
        if ("cuisine" in filter_cond):
            for allowed_cuisine in filter_cond['cuisine']:
                for restaurant in c:
                    for cuisine in restaurant['cuisine']:
                        if allowed_cuisine == cuisine:
                            d.append(restaurant)
        else:
            d = c

        # filtering rating
        e = list()
        if ("rating" in filter_cond):
            for restaurant in d:
                if float(restaurant['rating']) >= float(filter_cond['rating']):
                    e.append(restaurant)
        else:
            e = d

        # filtering price
        f = list()
        if ("price-range" in filter_cond):
            possible_price_ranges = ["Below $50", "$51-100", "$101-200", "$201-400", "$401-800", "Above $801"]
            min_p, max_p = filter_cond['price-range'].split('-')
            min_price = int(min_p)
            max_price = int(max_p)
            for restaurant in e:
                if min_price >= 0 and min_price <= 50:
                    start_index = 0
                elif min_price >= 51 and min_price <= 100:
                    start_index = 1
                elif min_price >= 101 and min_price <= 200:
                    start_index = 2
                elif min_price >= 201 and min_price <= 400:
                    start_index = 3
                elif min_price >= 401 and min_price <= 800:
                    start_index = 4
                else:
                    start_index = 5

                if max_price >= 51 and max_price <= 100:
                    end_index = 1
                elif max_price >= 101 and max_price <= 200:
                    end_index = 2
                elif max_price >= 201 and max_price <= 400:
                    end_index = 3
                elif max_price >= 401 and max_price <= 800:
                    end_index = 4
                else:
                    end_index = 5
                while (start_index <= end_index):
                    if (restaurant['price_range'] == possible_price_ranges[start_index]):
                        f.append(restaurant)
                        break
                    start_index += 1
        else:
            f = e

        self.query_result = f
    #==================END FILTER=============================


    def rank(self, ranking_weight):
        # getting score for each restaurant
        for restaurant in self.query_result:
            v = self.getscore(restaurant)

            #======calculating and adding score
            s = v[0]*ranking_weight[0] + v[1]*ranking_weight[1] + v[2]*ranking_weight[2] + v[3]*ranking_weight[3]
            restaurant['score']=s

        #ranking restaurants
        ranked_list = sorted(self.query_result, key=lambda k: k['score'],reverse=True)
        self.query_result=ranked_list
        for restaurant in self.query_result:
            del restaurant['score']    #removing extra vals
    #================END RANK=========================================


    def find_similar(self, restaurant, similiarity_weight, k):
        w=similiarity_weight
        u = self.getscore(restaurant)
        top_k_list=[]

        #get scores of restaurants in list
        for restaurant in self.query_result:
            v=self.getscore(restaurant)
            score = w[0]*abs(u[0]-v[0])+w[1]*abs(u[1]-v[1])+w[2]*abs(u[2]-v[2])+w[3]*abs(u[3]-v[3])
            restaurant['similarity'] = score

        similarity_list = sorted(self.query_result, key=lambda k: k['similarity'], reverse=False)

        threshold_similarity=similarity_list[k]['similarity']

        for restaurant in similarity_list[1:]:
            if restaurant['similarity']<=threshold_similarity:
                top_k_list.append(restaurant)

        for restaurant in self.query_result:
            del restaurant['similarity']    #removing extra vals

        return top_k_list
    #==============END FIND Similar=================================

    def print_query_result(self):
        print('Overall number of query_result: %d' % len(self.query_result))
        for restaurant in self.query_result:
            print(restaurant)
    #================END Query Result============================


    def getscore(self, restaurant):
        # ====getting vals
        rating = float(restaurant['rating'])
        latitude = float(restaurant['address'][0])
        longitude = float(restaurant['address'][1])

        # price
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

        # reviews
        good_reviews = int(restaurant['reviews'][0])
        medium_reviews = int(restaurant['reviews'][1])
        bad_reviews = int(restaurant['reviews'][2])

        # =======processing four vectors's
        v1 = rating  # rating
        v2 = math.sqrt(math.pow(22.417875 - latitude, 2) + math.pow(114.207263 - longitude, 2))  # distance
        v3 = (lowprice + highprice) / 2  # price
        v4 = bad_reviews / (good_reviews + medium_reviews + bad_reviews)

        return ([v1,v2,v3,v4])
    #==========================END GETSCORE======================

#==========test code for Q3.6
'''
search_engine = Food_Search_Engine("openrice_data.json")

#filtration for part 1
filter_conditions = {"district": ["Sha Tin"],
                     "cuisine": ["Japanese"],
                     'price-range': '50-200'}
search_engine.filter(filter_conditions)
#ranking for part 2
search_engine.rank([10,0,0,-1])
search_engine.print_query_result()


#choosing top-10 similar for optional part 3
for restaurant in search_engine.find_similar(search_engine.query_result[0], [2.31,167.11,0.11,-14.63], 10): #rating,distance, price, bad reviews
    print (restaurant)
'''