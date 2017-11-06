from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class YenisafakSpider(CrawlSpider):
    name = "yenisafak"
    allowed_domains = ["yenisafak.com"]

    def __init__(self, begin='', end='', *args, **kwargs):
        super(YenisafakSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.yenisafak.com/arama/?page=%s&type=News" % d for d in range(int(begin),int(end)+1)]

    rules = (
        Rule(LinkExtractor(allow=(), deny=(["/etiket/","/foto-galeri"]), restrict_xpaths=('//section[@class="list-box"]/article/a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "yenisafak"
        category         = hxs.xpath("//div[contains(@class,'haber-header')]/header/span[contains(@class,'category')]//text()").extract()
        date_time        = hxs.xpath("//div[contains(@class,'haber-header')]/div[contains(@class,'info')]/time/text()").extract()
        item["author"]   = ""
        title            = hxs.xpath("//div[contains(@class,'haber-header')]/header/h1/text()").extract()
        intro            = hxs.xpath("//div[contains(@class,'haber-header')]/header/h2/text()").extract()
        new_content      = hxs.xpath("//div[contains(@class,'content')]/div/p/text()").extract()
        if not re.sub("\s",""," ".join(new_content)):
            new_content      = hxs.xpath("//div[contains(@class,'content')]/div//text()").extract()
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
