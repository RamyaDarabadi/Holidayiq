"""This crawler will extract data from holidayiq"""
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
import MySQLdb
class Holiday(BaseSpider):
    name = 'holiday_browse'
    start_urls = ['http://www.holidayiq.com/holiday-packages/'] 
    def __init__(self, *args, **kwargs):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="holidaydb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()
    def parse(self, response):
        sel = Selector(response)
        #nodes = sel.xpath('//div/uli[@class="grid cs-style-3"]')
        nodes = sel.xpath('//div[@class="pkg-top-images-section"]/ul[@class="grid cs-style-3"]/li/a')
        for node in nodes:
            url_text = "".join(node.xpath('./@href').extract())
            url = 'http://www.holidayiq.com' + url_text
            image = "".join(node.xpath('./figure/img/@src').extract())
            title = "".join(node.xpath('./figure/span[@class="pkg-grid-txt"]/text()').extract())
            qry = 'insert into holi(title, image ,link) values (%s, %s, %s) on duplicate key update title = %s'
            values = (title, image, url, title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()
