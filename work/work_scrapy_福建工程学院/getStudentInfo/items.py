# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetstudentinfoItem(scrapy.Item):
    # 为你的项目定义字段如下:
    
    # 标题
    title = scrapy.Field()
    # 发布时间
    public_date = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()

