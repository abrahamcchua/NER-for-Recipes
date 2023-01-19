import scrapy



class linkSpider(scrapy.Spider):
    # Name is used for the scrapy shell
    name = 'link'
    # There were 119 different recipe-catalog pages when this data parser was made
    start_urls = [ "https://www.budgetbytes.com/recipe-catalog/page/"+str(i)+"/" for i in range(1, 119)]

    
    def parse(self, response):
        for item in response.css('article.post-summary'):
            title = item.css('h3::text').get()
            costing = item.css('div.post-summary__content').css('span::text').get(),
            link = item.css('a::attr(href)').get()
            # Assumes that if costing is not available then the link is not a recipe (Link could contain suggestions for other recipes)
            if costing[0] != None:
                yield {
                        'title': title,
                        'costing': costing,
                        'link': link
                        }
            else:
                continue