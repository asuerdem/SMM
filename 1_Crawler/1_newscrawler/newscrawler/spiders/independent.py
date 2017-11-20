from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class IndependentSpider(CrawlSpider):
    name = "independent"
    allowed_domains = ["independent.co.uk"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(IndependentSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat() for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.independent.co.uk/archive/%s" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ol[@class="margin archive-news-list"]/li/a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "independent"

        title       = hxs.xpath('//h1[@itemprop="headline"]/text()').extract()
        intro       = hxs.xpath('//div[@class="intro"]/p/text()').extract()
        author      = hxs.xpath('//span[@itemprop="name"]/a/text()').extract()
        category    = hxs.xpath('//ol[@class="breadcrumbs clearfix"]//a//text()').extract()
        new_content = hxs.xpath('//div[@itemprop="articleBody"]/p//text()').extract()
        date_time   = hxs.xpath('//ul[@class="caption meta inline-pipes-list"]//time/@datetime').extract()
        #Ahmet added the following for the keywords, might be useful for machine learning
        topic       = hxs.xpath('//ul[@class="inline-pipes-list"]//a//text()').extract() 
                               
        #
        # Processing outputs
        author = [re.sub('^By\s','',a) for a in author]
        author = [re.sub('\sin\s.*','',a) for a in author]
        new_content = [p for p in new_content if not re.search(u'\u2022',p)]
        new_content = [p for p in new_content if not re.search('font-family|background-color:',p)]
        new_content = ' '.join(new_content)
        new_content = re.sub('\n','',new_content)
        item["content"] = re.sub('\s{2,}',' ',new_content)
        author = '|'.join(author)
        item["category"] = '|'.join(category)
        item["intro"]  = ' '.join(intro)
        item["title"]  = ' '.join(title)
        datte    = re.findall('[0-9]+.[0-9]+.[0-9]+',date_time[0])[0]
        tme      = re.findall('[0-9]+:[0-9]+',date_time[0])[0]
        datte    = datte.split('/')
        item["date_time"] = datte[2] + '-'  + datte[1] + '-' + datte[0] + 'T' + tme
        item["author"] = author


        return(item)
