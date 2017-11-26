from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re


class PeoplesChinaSpider(CrawlSpider):
    name = "peopleschina"
    allowed_domains = ["people.cn"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(PeoplesChinaSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=0) + pd.DateOffset(days=0)
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://en.people.cn/review/%s.html" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="p1_left fl"]//a',
        '//div[@class="p1_right fr"]//a','//div[@class="p2_left fl"]//a',
        '//div[@class="p1_c fl"]//a','//div[@class="p1_c2 fl"]//a',),deny=('//div[@class="ad02 clear"]/a')), callback="parse_items", follow= False),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "peopleschina"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]  = ''
        return(item)
