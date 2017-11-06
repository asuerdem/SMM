from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class PeoplesChinaSpider(CrawlSpider):
    name = "peopleschina"
    allowed_domains = ["people.cn"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(PeoplesChinaSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://en.people.cn/review/%s.html" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="p1_left fl"]//a',
        '//div[@class="p1_right fr"]//a',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(deny=('//div[@class="ad02 clear"]/a'), restrict_xpaths=()), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "PeoplesChina"

        title       = hxs.xpath('//span[@id="p_title"]/text()').extract()
        if not title:
            title = hxs.xpath('//div[@class="w980 wb_10 clear"]/h1//text()').extract()
        if not title:
            title = hxs.xpath('//div[@id="p_title"]//text()').extract()

        intro       = ""
        author      = hxs.xpath('//div[@class="wb_1 clear"]//text()').extract()
        if not author:
            author  = hxs.xpath('//div[@class="w980 wb_10 clear"]/div//text()').extract()
        category    = hxs.xpath('//div[@class="w980 wbnav wbnav2 clear"]//a//text()').extract()
        if not category:
            category    = hxs.xpath('//div[@id="p_navigator"]//text()').extract()

        new_content = hxs.xpath('//div[@id="p_content"]/p//text()').extract()
        if not new_content:
            new_content = hxs.xpath('//div[@class="wb_12 clear"]/p//text()').extract()
        if not new_content or len("".join(new_content))<10:
            new_content = hxs.xpath('//span[@id="p_content"]/text()').extract()
        if not new_content or len("".join(new_content))<10:
            new_content = hxs.xpath('//div[@id="p_content"]//text()').extract()
        if not new_content or len("".join(new_content))<10:
            new_content = hxs.xpath('//font[@class="fbody"]//text()').extract()



        author      = "".join(author)
        date_time   = author
        if not date_time or len(date_time)<2:
            date_time = hxs.xpath('//div[@id="p_publishtime"]//text()').extract()
            date_time = "".join(date_time)

        if not date_time or len(date_time)<2:
            date_time = hxs.xpath('//span[@id="p_publishtime"]//text()').extract()
            date_time = "".join(date_time)

        print date_time

        if not author:
            author = hxs.xpath('//h3[@class="wb_2 clear"]//text()').extract()
            author      = "".join(author)

        #
        # Processing outputs
        author = re.findall('^.*[)]',author)
        author = [re.sub('^By\s','',a) for a in author]

        new_content = [p for p in new_content if not re.search(u'\u2022',p)]
        new_content = [p for p in new_content if not re.search('font-family|background-color:',p)]
        new_content = ' '.join(new_content)
        new_content = re.sub('\n','',new_content)
        item["content"] = re.sub('\s{2,}',' ',new_content)
        author      = re.sub("[)()]","",'|'.join(author))
        item["category"] = '|'.join(category)
        item["intro"]  = ""
        item["title"]  = ' '.join(title)
        date_time = re.findall('[0-9]+:[0-9]{2}.*',date_time)
        item["date_time"] = ''.join(date_time)
        item["author"] = author


        return(item)
