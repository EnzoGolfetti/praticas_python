# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import MySQLdb
import sqlalchemy
from .items import AmazonSpider1Item

class AmazonSpider1Pipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'enzo_admin',
            password = 'FhZW3A#RKzDn',
            database = 'scrapy_data_amz'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into livros_amz (titulo_livros, autor, preco) values (%s,%s,%s)""",(
            item['titulo_livro'][0],
            item['autor'][0],
            item['preco'][0]
        ))
        self.conn.commit()




