from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class GuardianSpider(CrawlSpider):
    name = "guardian" # this will be used to call scrapy crawl ... code
    allowed_domains = ["theguardian.com"]
        
       
    def __init__(self, yearmonth='', *args, **kwargs):
        ## LINK GENERATOR:
        #  The archive pages that we usually generate by using Excel
        super(GuardianSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=0) + pd.DateOffset(days=1) 
        #for 30 days months need a solution, either delete duplicates or regex
        date_inds  = [d.date().isoformat().replace("-","/") for d in pd.date_range(begin_date,end_date)]
        month_dict = {'01':'jan', '02':'feb', '03':'mar', '04':'april', '05':'may',
        '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec' }
        months = [month_dict[ re.findall('[0-9]{4}/([0-9]{2})/[0-9]{2}',d)[0] ] for d in date_inds]
        date_inds = [re.sub('/[0-9]{2}/',"/" + month_dict[re.findall('[0-9]{4}/([0-9]{2})/[0-9]{2}',d)[0] ] + "/",d)  for d in date_inds]
       
        category_list = ["education"]
        urls_list = [["https://www.theguardian.com/%s/%s/all" % (c,d) for c in category_list] for d in date_inds]
        self.start_urls = sum(urls_list,[]) # This will be the list of archive pages
        
        
    rules = (# Locates individual news page urls from each day's in archive
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="fc-item__container"]/a',)), callback="parse_items", follow= False),
        # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@data-link-name="article"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "guardian"

        
        title       = hxs.xpath('//div[@class="gs-container"]//h1[@itemprop="headline"]/text()').extract()
        intro       = hxs.xpath('//div[@class="gs-container"]//div[@class="content__standfirst"]//text()').extract()
        author      = hxs.xpath('//span[@itemprop="name"]/a/text()').extract()
        category    = hxs.xpath('//ul[@class="signposting"]//a/text()').extract()
        new_content = hxs.xpath('//div[@itemprop="articleBody"]/p//text()').extract()
        date_time   = hxs.xpath('//p[@class="content__dateline"]//time[@itemprop="datePublished"]/@datetime').extract()
        topic       = hxs.xpath('//ul[@class="submeta__links"]//a/text()').extract()
      
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        category           = category[1:]
        category           = [c for c in category if not c==">"]
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        item["author"]     = '|'.join(author)
        item["topic"]   = '|'.join(topic)
        return(item)
