import string
import json

import scrapy

class RecipesSpider(scrapy.Spider):
    name = 'recipes'
    with open('links.json', 'r') as f:
        data = json.load(f)
    start_urls = [data_iter['link'] for data_iter in data]
    
    
    def preprocess(self, instruction):
        # Combines lists and removes punctuations
        instruction = ' '.join(instruction)
        return instruction.translate(str.maketrans('', '', string.punctuation))
     
    
    def remove_space(self, list):
        # Removes leading and trailing space
        return [sentence.strip() for sentence in list]
    
    
    def parse(self, response):
        # For cases where the css format is not the same 
        alternative_format_list = response.css("li.wprm-recipe-instruction").css("div.wprm-recipe-instruction-text").css('span::text').getall()
        instruction = response.css('div.wprm-recipe-instruction-text::text').getall() + alternative_format_list
        instruction = self.preprocess(self.remove_space(instruction))
        # Don't parse the website if there are no instructions
        if len(instruction) != 0:
            yield {
                "link": response.xpath("//meta[@property='og:url']/@content").extract()[0],
                "Recipe Name" : response.css('h1::text').get(),
                "Time" : response.css('span.wprm-recipe-details::text')[-1].get() + " " 
                + response.css('span.wprm-recipe-details-unit::text')[-1].get(),
                "Instructions" : instruction
            }


