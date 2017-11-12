from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re

# Changes according to the newspaper
class DailyMailSpider(CrawlSpider):
    name = "dailymail" #could be dmspider as well
    allowed_domains = ["dailymail.co.uk"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(DailyMailSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01") # Don't change
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1) # Dont change
        # changes according to the logic of the archive link generating method
        # i.e. below isoformat is 2017-07-01 and we transformed it by adding .replace("-","") (replace - with nothing)
        # to convert it to 20170701
        # http://www.dailymail.co.uk/home/sitemaparchive/day_20170701.html
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.dailymail.co.uk/home/sitemaparchive/day_%s.html" % d for d in date_inds]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="archive-articles debate link-box"]//a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "en"
        item["source"] = "dailymail"

        title       = hxs.xpath('//div[@class="js-article-text"]/h1/text()').extract()
        intro       = ""
        author      = hxs.xpath('//p[@class="author-section byline-plain"]/a/text()').extract()
        category    = hxs.xpath('//ol[@class="breadcrumbs clearfix"]//a//text()').extract()
        new_content = hxs.xpath('//div[@itemprop="articleBody"]/p//text()').extract()
        date_time   = hxs.xpath('//ul[@class="caption meta inline-pipes-list"]//time/@datetime').extract()
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
