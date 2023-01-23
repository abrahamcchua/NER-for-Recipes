# Create the scrapy project with all required files
scrapy startproject <project_name>

# Load Scrapy cli for debugging
scrapy shell
#   Parse certain website
    fetch('<URL>')
#   Determining what part of the html to be parsed:
#   Using css tags
    response.css('<css_tag>')
#       To get all of the tags in the link with that tag
        response.css('<css_tag>').getall()
#   Using xml tags
    response.xpath("<xml_mapping>")
#       To get all of the tags in the link with that tag
        response.xpath("<xml_mapping>").getall()

# Create the scrapy spider with arbitrary name
scrapy genspider spider output.com

# Running the spiders to crawl the websites and where its corresponding output
scrapy crawl <spider.name> -o <filename>.<file_extension>