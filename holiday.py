"""This code helps to gather all information from holidayiq.com"""

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
import MySQLdb
class Holiday(BaseSpider):
    name = 'holiday'
    #start_urls = ['http://www.holidayiq.com/holiday-packages/'] 
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="holidaydb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()
    def start_requests(self):
        qry = 'select title,image,link from holi limit 1'
        self.cur.execute(qry)
        rows = self.cur.fetchall()
        for row in rows:
            title, image, link = row
            yield Request(link, callback=self.parse_place, meta={'image':image, 'title':title, 'link':link})
    def parse_place(self, response):
        sel = Selector(response)
        image = response.meta['image']
        place = response.meta['title']
        link = response.meta['link']
        nodes = sel.xpath('//div[@class="pkg-listing-right-main-section"]/div[@class="row"]')
        for node in nodes:
            image_pkg = "".join(node.xpath('./div[@class="image_hidden col-xs-12 col-sm-12 col-md-4 col-lg-4"]/span/text()').extract())
            title_pkg = "".join(node.xpath('./div[@class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]/div[@class="row"]//h2[@class="pkg-list-hotel-name"]/a/text()').extract())
            name = title_pkg.replace("\n", "")
            price = "".join(node.xpath('.//div[@class="pkg-list-price-right"]/h4[@class="pkg-list-hotel-name"]/text()').extract())
            qry = 'insert into holidayiq_hotels(name, image, link, price, place) values (%s,%s, %s, %s, %s)on duplicate key update name = %s'
            values = (name, image_pkg, link, price, place, name)
            self.cur.execute(qry, values)
            self.conn.commit()
