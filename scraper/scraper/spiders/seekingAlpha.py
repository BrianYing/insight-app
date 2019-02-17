# -*- coding: utf-8 -*-
import scrapy

from scraper.items import ScraperItem


class SeekingalphaSpider(scrapy.Spider):
    name = 'seekingAlpha'
    allowed_domains = ['nasdaq.com']
    start_urls = ['https://www.nasdaq.com/symbol/oxy']

    def parse(self, response):
        # filename = "page.html"
        # open(filename, 'w').write(response.body.decode("utf-8"))
        stock_price = response.xpath('//*[@id="qwidget_lastsale"]/text()').re_first(r'\S+')
        share_volume = response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[3]/div[2]/text()').re_first(r'\S+')
        market_cap = response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[7]/div[2]/text()').re_first(r'\S+')

        item = ScraperItem()
        item['stock_price'] = stock_price
        item['share_volume'] = share_volume
        item['market_cap'] = market_cap

        return item
