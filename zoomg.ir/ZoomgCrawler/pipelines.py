from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PreprocessPipeline:
    def process_item(self, item, spider):
        item['date'] = item['date'].split()[1]
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        if item['url'] in self.seen_urls:
            raise DropItem("Repeated items found: %s" % item)
        else:
            self.seen_urls.add(item['url'])
            return item
