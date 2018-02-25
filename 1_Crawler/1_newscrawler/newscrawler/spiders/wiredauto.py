from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
from newsplease import NewsPlease
import pandas as pd
import re


class WiredAutoSpider(CrawlSpider):
    name = "wiredauto"
    allowed_domains = ["wired.com"]
    collection_name = 'wired'

    def __init__(self, begin='', end='', *args, **kwargs):
        super(WiredAutoSpider, self).__init__(*args, **kwargs)
        begin = pd.Timestamp(begin + "-01")
        end   = pd.Timestamp(end + "-01") + pd.DateOffset(months=1)
        date_inds  = [re.findall("[0-9]{4}/[0-9]{2}", d.date().isoformat().replace("-","/"))[0] for d in pd.date_range(begin,end,freq="M")]
        self.start_urls = ["https://www.wired.com/%s/" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li/a[@class="clearfix pad"]',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="next page-numbers"]',)), callback="parse_items", follow= True),
    )


    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        category     = hxs.xpath("//ul[@aria-label='Metadata for article.']//span[@itemprop='articleSection']//text()").extract()
        item["link"] = response.request.url
        article = NewsPlease.from_url(item["link"])
        item["lang"]   = "en"
        item["source"] = "wired"
        item['title']   = article.title
        item['intro']   = article.description
        item["author"]  = '|'.join(article.authors)
        item["content"] = article.text
        item["date_time"] = article.date_publish.isoformat()
        item["category"]   = '|'.join([c for c in category if not re.match('^\s+$',c)])
        return(item)
