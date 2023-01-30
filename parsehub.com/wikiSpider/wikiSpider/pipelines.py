# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import pyttsx3


class PreprocessPipeline:
    def process_item(self, item, spider):
        item['name'] = re.sub("<[^>]*>", " ", item[ 'name' ] )
        item['name'] = re.sub("\s+", " ",  item['name'] )
        item['name'] = re.sub("\.", "\,",  item['name'] )
        item['name'] = re.sub("\!", "\,",  item['name'] )
        item['name'] = re.sub("\:", "\,",  item['name'] )
        return item

class Mp3Creater :
    count = 0
    def process_item(self , item , spider) :
        self.count += 1
        z = str( self.count )
        engine = pyttsx3.init()
        engine.save_to_file( item['name'] , 'article'+z+'.MP3') 
        engine.runAndWait( )
        

        print(item['name'])