# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NewsItem(Item):
    link = Field()
    lang = Field()
    source = Field()
    category = Field()
    date_time = Field()
    author = Field()
    title = Field()
    intro = Field()
    content = Field()
    image_urls = Field()
    topic = Field()

class UrlItem(Item):
    link     = Field()
    lang     = Field()
    source   = Field()
    newslink = Field()
