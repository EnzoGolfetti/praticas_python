# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonSpider1Item(scrapy.Item):
    # define the fields for your item here like:
    titulo_livro = scrapy.Field()
    autor = scrapy.Field()
    preco = scrapy.Field()

