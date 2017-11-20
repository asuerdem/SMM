from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class WiredSpider(CrawlSpider):
    name = "wired"
    allowed_domains = ["wired.com"]

    def __init__(self, begin='', end='', *args, **kwargs):
        super(WiredSpider, self).__init__(*args, **kwargs)
        begin = pd.Timestamp(begin + "-01")
        end   = pd.Timestamp(end + "-01") + pd.DateOffset(months=1)
        date_inds  = [re.findall("[0-9]{4}/[0-9]{2}", d.date().isoformat().replace("-","/"))[0] for d in pd.date_range(begin,end,freq="M")]
        self.start_urls = ["https://www.wired.com/%s/" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li/a[@class="clearfix pad"]',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="next page-numbers"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "wired"
        category     = hxs.xpath("//li/span[@itemprop='articleSection']//text()").extract()
        date_time    = hxs.xpath("//ul/meta[@itemprop='datePublished']/@content").extract()
        author       = hxs.xpath("//ul/li/span[@itemprop='author']//text()").extract()
        title            = hxs.xpath("//header/h1[@data-js='postTitle']/text()").extract()
        intro            = ""
        new_content      = hxs.xpath("//article[@data-js='content']/p//text()").extract()
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        category           = list(set([c for c in category if re.search("\S",c)]))
        item["category"]   = '|'.join(category)
        date_time          = " ".join(date_time)
        item["author"]     = " ".join(author).strip()
        item["date_time"]  = date_time.split("+")[0]

        return(item)
