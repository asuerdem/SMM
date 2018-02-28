from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ..items import NewsItem
from datetime import datetime
import pandas as pd
from newsplease import NewsPlease
import re


class IndependentUrlSpider(CrawlSpider):
    # handle_httpstatus_list = [400]
    name = "independentauto"
    allowed_domains = ["independent.co.uk"]
    collection_name = 'independent'

    def __init__(self, yearmonth='', *args, **kwargs):
        super(IndependentUrlSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat() for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.independent.co.uk/archive/%s" % d for d in date_inds]

    rules = (
         Rule(LinkExtractor(allow=(), restrict_xpaths=('//ol[@class="margin archive-news-list"]//a',)), callback="parse_items", follow= False),)


    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "independent"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]  = ''
        return(item)
