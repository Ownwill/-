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





