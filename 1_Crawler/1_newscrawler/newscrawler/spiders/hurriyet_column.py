from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class HurriyetColumnSpider(CrawlSpider):
    name = "hurriyetcolumn"
    allowed_domains = ["hurriyet.com.tr"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(HurriyetColumnSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(years=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.hurriyet.com.tr/index/?d=%s" % d for d in date_inds]      

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="special-author-loop author-items"]/div[@class="author"]//a',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="paging"]/a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"]         = response.request.url
        item["lang"]        = "tr"
        item["source"]    = "hurriyet"
        category             = ["koseyazisi"]
        date_time           = hxs.xpath("//div[@class='article-date']/text()").extract()
        author                = hxs.xpath("//div[@class='author-info-content']/div[@class='name']//a/text()").extract()
        title                     = hxs.xpath("//h1[@class='article-title']/text()").extract()
        intro                    = hxs.xpath("//div[@class='article-content news-description']/p/text()").extract()
        new_content       = hxs.xpath("//div[@class='article-content news-text']/p/text()").extract()
        new_content         = ' '.join(new_content)
        new_content         = re.sub('\n',' ',new_content)
        if not new_content:
            new_content       = hxs.xpath("//div[@class='article-content news-text']//text()").extract()
            new_content         = ' '.join(new_content)
            new_content         = re.sub('\n',' ',new_content)

        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]           = ' '.join(title)
        item["content"]     = re.sub('\s{2,}',' ',new_content)
        item["category"]    = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        item["author"]       = " ".join(author)
        return(item)
