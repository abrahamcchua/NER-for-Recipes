import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


#https://www.budgetbytes.com/recipe-catalog/2/

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ["https://www.budgetbytes.com/recipe-catalog/page/2/"]
    # rules = (
        
    # )
    
    def parse(self, response):
        for item in response.css('article.post-summary'):
            title = item.css('h3::text').get()
            costing = item.css('div.post-summary__content').css('span::text').get(),
            link = item.css('a::attr(href)').get()
            if costing[0] != None:
                yield {
                        'title': title,
                        'costing': costing,
                        'link': link
                        }
            else:
                continue