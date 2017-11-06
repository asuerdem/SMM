from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class CumhuriyetSpider(CrawlSpider):
    name = "cumhuriyet"
    allowed_domains = ["cumhuriyet.com.tr"]

    def __init__(self, begin='', end='', *args, **kwargs):
        super(CumhuriyetSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.cumhuriyet.com.tr/arama/?page=%s" % d for d in range(int(begin),int(end)+1)]

    rules = (
        Rule(LinkExtractor(allow=(),deny=('.*/video/.*',), restrict_xpaths=('//ul[@id="result-list"]/li/a[@class="result"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "cumhuriyet"
        category         = hxs.xpath("//div[@id='breadcrumb']/div[@itemprop='child']//a/text()").extract()
        date_time        = hxs.xpath("//div[@class='publish-date']/div[@class='right']/span/text()").extract()
        item["author"]   = ""
        title            = hxs.xpath("//div[@id='news-header']//h1[@class='news-title']/text()").extract()
        intro            = hxs.xpath("//div[@id='news-header']//div[@class='news-short']/text()").extract()
        new_content      = hxs.xpath("//div[@id='news-body']/p/text()").extract()
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)


        return(item)
