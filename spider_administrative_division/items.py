# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import attr


@attr.s
class SpiderAdministrativeDivisionItem:
    # define the fields for your item here like:
    # name = scrapy.Field()
    hierarchy = attr.ib()  # 区域级别
    higher_id = attr.ib()  # 上级id
    area_id = attr.ib()  # 区域id
    area_name = attr.ib()  # 区域名称
