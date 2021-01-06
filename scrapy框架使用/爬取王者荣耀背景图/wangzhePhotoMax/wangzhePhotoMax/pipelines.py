# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ImgPileLine(ImagesPipeline):
    # 接收item且将item中存储的img_src进行请求发送
    def get_media_requests(self, item, info):
        print('&'*50)
        print(item['skin_url'])
        yield scrapy.Request(url=item['skin_url'],meta={'hero_name':item['hero_name'],
                                                        'skin_name':item['skin_name'],
                                                        'skin_url':item['skin_url']
                                                        })

    # 指定数据存储的路径(文件夹【在配置文件中指定】+图片名称【该方法中返回】)
    def file_path(self, request, response=None, info=None):
        # img_name = request.url.split('/')[-1]
        img_name = request.meta['hero_name'] + '_' + request.meta['skin_name'] + '.jpg'
        print(img_name)
        return img_name

    def item_completed(self, result, item, info):
        return item
