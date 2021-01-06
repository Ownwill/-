### 创建项目

创建项目命令：scrapy startproject wangzhePhotoMax

创建爬虫：scrapy genspider WangZheCrawl https://pvp.qq.com

更改settings.py中的设置：

```python
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

下载图片需要安装PIL，安装命令：pip install pillow

设置图片的存储路径

```python
# 设置图片存储路径
IMAGES_STORE='./imgs'
```

更改存储管道，更换为存储图片的管道

```python
# 更改存储管道，更换为存储图片的管道
ITEM_PIPELINES = {
   'wangzhePhoto.pipelines.ImgPileLine': 300,
}
```

下载时间设置

```python
DOWNLOAD_DELAY = 2
```

### spiders文件下爬虫的书写

进行代码书写，将图片的网上链接地址，和图片的名称返回

WangZheCrawl.py文件

```python
import bs4
import time
import scrapy
from wangzhePhotoMax.items import WangzhephotomaxItem

class WangzhecrawlSpider(scrapy.Spider):
    name = 'WangZheCrawl'
    allowed_domains = ['pvp.qq.com','game.gtimg.cn']
    start_urls = []

    start_urls.append("https://pvp.qq.com/web201605/herolist.shtml")
    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text,'html.parser')
        ul_bs = bs.find('ul',class_="herolist clearfix")
        hero_li = ul_bs.find_all('li')
        for hero in hero_li:
            a_link = hero.find('a')
            next_url = 'https://pvp.qq.com/web201605/' + a_link['href']
            # 英雄的名字
            name = a_link.text
            # print(next_url)
            yield scrapy.Request(next_url,callback=self.next_page_parse,meta={
                'next_url':next_url,
                'name':name
            })
            time.sleep(1)

    def next_page_parse(self,response):
        # print('****************' * 20)
        bs = bs4.BeautifulSoup(response.text,'html.parser')
        # 提取图片的链接地址
        style_bs = bs.find('div',class_="zk-con1 zk-con")['style']
        part_url = style_bs.replace("background:url('//",'').replace("') center 0",'')
        # print('part_url:',part_url)

        # 获取某个英雄的皮肤个数
        data_imgname = bs.find('ul',class_='pic-pf-list pic-pf-list3')['data-imgname']
        count_skins = data_imgname.count('|') + 1
        name_list = data_imgname.split('|')

        for i in range(count_skins):
            skin_url = 'https://' + part_url.replace('1.jpg','%s.jpg'%(i+1))
            name = name_list[i].split('&')[0]

            # 将数据返回
            item = WangzhephotomaxItem()

            item['hero_name'] = response.meta['name']
            item['skin_url'] = skin_url
            item['skin_name'] = name
            yield item
```

items.py ：它定义 Item 数据结构，所有的 Item 的定义都可以放这里，在这里定义的item可以供上面WangZheCrawl.py调用。

items.py

```python
import scrapy


class WangzhephotomaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hero_name = scrapy.Field()
    skin_url = scrapy.Field()
    skin_name = scrapy.Field()
```

### 在pipelines.py中设置

设置图片的存储

```python
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
```

### 启动爬虫

进入到项目根目录（包含settings.py文件的目录）下输入启动爬虫命令：scrapy crawl WangZheCrawl

### 爬取结果

![image-20210106110705983](readme.assets/image-20210106110705983.png)




