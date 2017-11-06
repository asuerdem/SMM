from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class MirrorSpider(CrawlSpider):
    name = "mirror"
    allowed_domains = ["mirror.co.uk"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(TimesSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat().replace("-","/") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.mirror.co.uk/archive/%s/" % d for d in date_inds]


    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="search-results"]/h3//a',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="pagination clearfix"]//a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "mirror"
        category     = hxs.xpath("//div[@class='col-md-12']/div[@class='breadcrumb-body clr']/span//text()").extract()
        date_time    = hxs.xpath("//span[@class='modify-date']/text()").extract()
        item["author"]   = ""
        title            = hxs.xpath("//h1[@class='news-detail-title selectionShareable']/text()").extract()
        intro            = hxs.xpath("//div[@class='news-detail-spot news-detail-spot-margin']/h2/text()").extract()
        new_content      = hxs.xpath("//div[@class='news-box']/p/text()").extract()
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        category           = category[1:-1]
        category           = [c for c in category if not c==">"]
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)

        return(item)
