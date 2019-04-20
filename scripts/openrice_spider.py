import scrapy
import json

class OpenriceSpider(scrapy.Spider):
    name = 'openrice'
    allowed_domains = ['www.openrice.com']
    details_list = []

    def start_requests(self):
        headers = {
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control': 'max-age=0',
        }
        source_file = open("openrice_urls.txt", "r")

        url_list = source_file.read().splitlines()

        for site in url_list:
            yield scrapy.Request(url=site, headers=headers, callback=self.parse)
    #============end of start

    def parse(self, response):
        restaurant_list_selector = "html.or-web"

        details = {}

        #css blocks
        restaurant_title_selector = "title::text"
        restaurant_cuisine_selector = "div.header-poi-categories.dot-separator a::text"
        restaurant_price_range_selector = "div.header-poi-price.dot-separator a::text"
        restaurant_rating_selector = "div.header-score::text"
        restaurant_latitude_selector = "div.mapview-warper.js-mapview-warper div::attr(data-latitude)"
        restaurant_longitude_selector = "div.mapview-warper.js-mapview-warper div::attr(data-longitude)"
        restaurant_score_selector = "div.score-div::text"
        restaurant_location_selector = "div.header-poi-district.dot-separator a::text"
        restaurant_url_selector = "div.main-menu.table-center a.active::attr(href)"

        #extractiing details
        i=0
        for restaurant in response.css(restaurant_list_selector):
            restaurant_name = (response.css(restaurant_title_selector).extract_first()).partition(" - ")[0]
            restaurant_cuisine_list = response.css(restaurant_cuisine_selector).extract()
            restaurant_price_range = response.css(restaurant_price_range_selector).extract_first()
            restaurant_rating = response.css(restaurant_rating_selector).extract_first()
            restaurant_latitude = response.css(restaurant_latitude_selector).extract_first()
            restaurant_longitude = response.css(restaurant_longitude_selector).extract_first()
            restaurant_address = list()
            restaurant_address.append(restaurant_latitude)
            restaurant_address.append(restaurant_longitude)
            restaurant_score = response.css(restaurant_score_selector).extract()
            restaurant_location = response.css(restaurant_location_selector).extract_first()
            restaurant_url = response.css(restaurant_url_selector).extract_first()


            details["name"] = restaurant_name
            details["cuisine"] = restaurant_cuisine_list
            details["price_range"] = restaurant_price_range
            details["address"] = restaurant_address
            details["rating"] = restaurant_rating
            details["reviews"] = restaurant_score
            details["district"] = restaurant_location
            details["url"] = "www.openrice.com"+restaurant_url

            self.details_list.append(details)

            with open('openrice_data.json', 'w') as output_file:
                json.dump(self.details_list, output_file, indent=4)

    #===================END of PARSE========================


#==============to test spider
#from scrapy import cmdline
#cmdline.execute("scrapy runspider openrice_spider.py".split())