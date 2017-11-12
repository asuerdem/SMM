from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class SabahSpider(CrawlSpider):
    name = "sabah"
    allowed_domains = ["sabah.com.tr"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(SabahSpider, self).__init__(*args, **kwargs)
        # http://www.sabah.com.tr/timeline/2017/05/20
        begin = pd.Timestamp(yearmonth + "-01")
        end   = pd.Timestamp(begin) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        end   = pd.Timestamp(begin) + pd.DateOffset(days=1)
        date_inds  = [re.findall("[0-9]{4}/[0-9]{2}/[0-9]{2}", d.date().isoformat().replace("-","/"))[0] for d in pd.date_range(begin,end)]
        self.start_urls = ["http://www.sabah.com.tr/timeline/%s" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="masonryFrame"]/div[@class="box"]//a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "sabah"
        category         = hxs.xpath("//div[contains(@class,'haber-header')]/header/span[contains(@class,'category')]//text()").extract()
        date_time        = hxs.xpath("//div[contains(@class,'haber-header')]/div[contains(@class,'info')]/time/text()").extract()
        item["author"]   = ""
        title            = hxs.xpath("//div[contains(@class,'haber-header')]/header/h1/text()").extract()
        intro            = hxs.xpath("//div[contains(@class,'haber-header')]/header/h2/text()").extract()
        new_content      = hxs.xpath("//div[contains(@class,'content')]/div/p/text()").extract()
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
