import cv2
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains

class TencentSilder():
    def __init__(self,driver):
        self.url = 'https://i.qq.com/'   #网站链接地址
        self.driver = driver
        #滑块和背景图片存储路径
        self.slideBlock_path = './image/slideBlock.png'
        self.slideBg_path = './image/slideBg.png'
        self.w1 = 0   #真实图片的宽度
        self.w2 = 0   #网站上的图片宽度
        self.x = 0    #滑动偏移量

        self.slideBlock = '' #定义滑动模块

    #保存图片
    def load_pic(self,name,link):
        '''

        :param name: 传入的图片名称
        :param link: 图片的下载链接地址
        :return:
        '''
        resp = requests.get(link)
        img = resp.content
        self.filepath = './image/%s.png'%name
        with open(self.filepath,'wb') as f:
            f.write(img)
        return

    # 借助opencv识别
    def image_recognition(self, slideBlock_path, slideBg_path):
        """
        
        :param slideBlock_path: 滑块图片存储地址
        :param slideBg_path: 滑块背景图片存储地址
        :return: value[2][0]，匹配到的距离左侧的长度, w1：真实图片的宽度。
        """
        # 图片读取,获取的图片与网站图片大小不一致，网站图片经过前端处理
        image_rgb = cv2.imread(slideBlock_path)
        # 图片灰度处理
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        # 读取模块图片
        bg_rgb = cv2.imread(slideBg_path, 0)
        # 获取原图宽度
        w1 = bg_rgb.shape[1]

        # 匹配模块位置
        match_loc = cv2.matchTemplate(image_gray, bg_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(match_loc)
        return value[2][0], w1

    def offsetDis(self,slideBlock_path,slideBg_path):
        # 得到滑块凹槽与左侧图片的宽度
        x, self.w1 = self.image_recognition(slideBlock_path, slideBg_path)
        # 缩放之后的宽度
        x = x * self.w2 / self.w1
        # 腾讯滑块偏移量。 x减去左边界透明部分的长度,视图上的左边界透明部分长度为原图左边界透明部分长度乘以w2/w1。
        # 之后再减去滑块左侧的长度
        x = x + 9.3 - 32
        # print('w2 / w1:',w2 / w1)
        return x

    def sildeBlock(self):
        # 滑块移动
        print('self.x:', self.x)
        # 设置滑块拖动
        action = ActionChains(self.driver)
        # 按住模块,使其生效
        action.click_and_hold(self.slideBlock).perform()
        # 拖动多少像素
        action.move_by_offset(self.x, 0)
        # 松开鼠标
        action.release().perform()
        time.sleep(3)
        return

    def getPage(self,url):
        '''
        获取页面并保存图片
        :return:
        '''
        #最大化页面
        self.driver.maximize_window()
        #隐式等待
        self.driver.implicitly_wait(10)
        self.driver.get(url)

        # 找到ifram并且点击进入
        self.driver.switch_to.frame("login_frame")
        self.driver.find_element_by_id('switcher_plogin').click()
        time.sleep(5)

        # qq页面的账号密码输入
        self.driver.find_element_by_id('u').send_keys('1212121')
        time.sleep(1)
        self.driver.find_element_by_id('p').send_keys('1212121')
        time.sleep(2)
        self.driver.find_element_by_id('login_button').click()
        time.sleep(3)

        # 进入滑块页面,进入滑块页面的iframe
        self.driver.switch_to.frame('tcaptcha_iframe')
        # 找到锁块与锁框图片的地址
        self.slideBlock = self.driver.find_element_by_id('slideBlock') #将滑块设置为全局
        slideBg = self.driver.find_element_by_id('slideBg')

        src_slideBlock = self.slideBlock.get_attribute('src')
        src_slideBg = slideBg.get_attribute('src')

        # 将图片进行保存
        self.load_pic('slideBlock', src_slideBlock)
        self.load_pic('slideBg', src_slideBg)

        w2 = slideBg.size['width']
        # 获取页面源代码
        # html = self.driver.execute_script("return document.documentElement.outerHTML")
        # print(html)

        return w2

    def run(self):
        self.w2 = self.getPage(self.url)     #获取页面并保存图片,返回网站上图片的宽度
        self.x = self.offsetDis(self.slideBlock_path, self.slideBg_path)   #计算偏移量
        self.sildeBlock()      #滑动模块
        # print(x)
        #关闭浏览器
        self.driver.quit()
        # 网站上的图片宽度



if __name__ == '__main__':
    driver = webdriver.Chrome()
    t = TencentSilder(driver)
    t.run()