from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re


class GoogleNewsSpider(CrawlSpider):
    name = "googlenews" # this will be used to call scrapy crawl ... code
    allowed_domains = ["news.google.com"]

    def __init__(self, query='', *args, **kwargs):
        ## LINK GENERATOR:
        #  The archive pages that we usually generate by using Excel
        super(GoogleNewsSpider, self).__init__(*args, **kwargs)
        query = query.replace("_","%20")
        starturl = 'https://news.google.com/news/search/section/q/' + query + '/' + query + '?hl=en&gl=US&ned=us'
        self.start_urls = [starturl] # This will be the list of archive pages
        #needs updating according to the following format: https://www.theguardian.com/world/2015/nov/09/all
        
        
    rules = (# Locates individual news page urls from each day's in archive
         #Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="fc-item__container"]/a',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="deQdld"]//a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "googlenews"
        ### The following lines does not change amongst newspapers, BEGIN ###
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        try:
            dtime = article.date_publish.isoformat()
        except:
            dtime = ''
        item["date_time"] = dtime
        ### END ###
        return(item)
