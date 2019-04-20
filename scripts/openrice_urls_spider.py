import scrapy


class OpenriceIDSpider(scrapy.Spider):
    name = "OpenriceIDSpider"

    def start_requests(self):
        headers = {
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control': 'max-age=0',
        }
        base = 'https://www.openrice.com/en/hongkong/restaurants'
        where_vec = ['?where=shatin&', '/district/mong-kok?', '/district/tsim-sha-tsui?', '/district/causeway-bay?']
        for where in where_vec:
            for page in range(1, 18):
                url = base + where + 'page=' + str(page)
                yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        output_filename = 'openrice_urls.txt'
        restaurant_list_selector = "html.or-web"
        restaurant_link_selector = "h2.title-name a::attr(href)"
        i=1
        for restaurant in response.css(restaurant_list_selector):
            restaurant_linklist = response.css(restaurant_link_selector).extract()
            for restaurant_link in restaurant_linklist:

                with open(output_filename, 'a') as output_file:  # you should delete the intermediate file before you run the code
                    output_file.write('https://www.openrice.com'+restaurant_link + '\n')

#to test spider
from scrapy import cmdline
cmdline.execute("scrapy runspider openrice_urls_spider.py".split())