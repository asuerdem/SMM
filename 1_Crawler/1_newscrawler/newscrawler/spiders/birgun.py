from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class BirgunSpider(CrawlSpider):
    name = "birgun"
    allowed_domains = ["birgun.net"]
    # CHECK THE FOLLOWING
    def __init__(self, starturl='', *args, **kwargs):
        super(BirgunSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.birgun.net/haber-detay/birgun-almanak-2014-un-en-zaytung-halleri-73348.html']
        # self.start_urls = [start_url]
        # http://www.birgun.net/ara?q=selahattin+demirta%C5%9F&c=&fd=2017-08-01&td=2017-08-29&a=

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="pagination"]/a[@class="next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "birgun"
        author       = hxs.xpath("//article[@class='haber-detay']/div[@class='author']//span[class='author-name']/text()").extract()
        if author:
            title     = hxs.xpath("//article/div[@class='article-name']/text()").extract()
            date_time = hxs.xpath("//article[@class='haber-detay']/div[@class='author']//time/text()").extract()
            category  = ['column']
        else:
            author = hxs.xpath("//div[@class='body fw']/p//strong/text()").extract()
            title    = hxs.xpath("//article[@class='haber-detay']/div[@class='title']/text()").extract()
            date_time    = hxs.xpath("//article[@class='haber-detay']/div[@class='line']/span[@class'date']/text()").extract()
            category     = hxs.xpath("//article[@class='haber-detay']/div[@class='line']/a[@class'category']/text()").extract()

        intro            = hxs.xpath("//article/div[@class='description']/text()").extract()
        new_content      = hxs.xpath("//article/div[@class='body fw']/p/text()").extract()
        image_url        = hxs.xpath("//article[@class='haber-detay']//img/@src").extract()
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        item["author"]     = '|'.join(author)
        item['image_urls'] = [image_url]
        return(item)
