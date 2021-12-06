# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GetstudentinfoPipeline:
    def process_item(self, item, spider):
        with open('./test.txt', 'a+', encoding='utf-8') as fp:
            fp.write(f'{item}, \n')
        return item