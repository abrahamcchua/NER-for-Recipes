import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ["https://www.budgetbytes.com/recipe-catalog/"]

    
    def parse(self, response):
        for post in response.css('div.site-container'):
            yield {
                    'title': post.css('h3::text').getall(),
                    'costing': post.css('div.post-summary__content').css('span::text').getall(),
                    'link': post.css('div.archive-post-listing a::attr(href)').getall()
                    }
                