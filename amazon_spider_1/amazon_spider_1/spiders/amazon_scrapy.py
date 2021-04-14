import scrapy
from ..items import AmazonSpider1Item

class AmazonScrapySpider(scrapy.Spider):
    name = 'amazon_scrapy'
    allowed_domains = ['amazon.com.br']
    start_urls = ['https://www.amazon.com.br/s?bbn=6740748011&rh=n%3A6740748011%2Cp_n_publication_date%3A5560469011&dc&qid=1618338121&rnid=5560468011&ref=lp_7841278011_nr_p_n_publication_date_1',
                  'https://www.amazon.com.br/s?i=stripbooks&bbn=7841278011&rh=n%3A6740748011%2Cn%3A7841775011%2Cp_n_publication_date%3A5560469011&dc&qid=1618338615&rnid=7841278011&ref=sr_nr_n_14'
                  ]
    page_number = 2
    page_number_2 = 2

    def parse(self, response):
        items_amz = AmazonSpider1Item()

        titulo_livro = response.css('.a-color-base.a-text-normal::text').extract()
        autor = response.css('.a-color-secondary .a-size-base+ .a-size-base::text').extract()
        preco = response.css('.a-price-whole::text').extract()

        items_amz['titulo_livro'] = titulo_livro
        items_amz['autor'] = autor
        items_amz['preco'] = preco

        yield items_amz


        next_page = 'https://www.amazon.com.br/s?i=stripbooks&bbn=6740748011&rh=n%3A6740748011%2Cp_n_publication_date%3A5560469011&dc&page='+ str(AmazonScrapySpider.page_number) +'&qid=1618338130&rnid=5560468011&ref=sr_pg_2'
        next_page_2 = 'https://www.amazon.com.br/s?i=stripbooks&bbn=7841278011&rh=n%3A6740748011%2Cn%3A7841775011%2Cp_n_publication_date%3A5560469011&dc&page='+ str(AmazonScrapySpider.page_number_2) +'&qid=1618339263&rnid=7841278011&ref=sr_pg_2'
        if AmazonScrapySpider.page_number <= 75 and AmazonScrapySpider.page_number_2 <= 26:
            AmazonScrapySpider.page_number += 1
            AmazonScrapySpider.page_number_2 +=1
            yield response.follow(next_page, callback=self.parse)
            yield response.follow(next_page_2, callback=self.parse)
