import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains

#保存图片
def load_pic(name,link):
    resp = requests.get(link)
    img = resp.content

    filepath = './image/%s.png'%name
    print(filepath)
    with open(filepath,'wb') as f:
        f.write(img)

driver = webdriver.Chrome()

#最大化页面
driver.maximize_window()
#隐式等待
driver.implicitly_wait(10)

driver.get('https://i.qq.com/')
#找到ifram并且点击进入
driver.switch_to.frame("login_frame")
driver.find_element_by_id('switcher_plogin').click()
time.sleep(5)

#输入账号密码
driver.find_element_by_id('u').send_keys('1212121')
time.sleep(1)
driver.find_element_by_id('p').send_keys('1212121')
time.sleep(2)
driver.find_element_by_id('login_button').click()
time.sleep(3)

# 进入滑块页面,进入滑块页面的iframe
driver.switch_to.frame('tcaptcha_iframe')
# 找到锁块与锁框图片的地址
slideBlock = driver.find_element_by_id('slideBlock')
slideBg = driver.find_element_by_id('slideBg')

src_slideBlock = slideBlock.get_attribute('src')
src_slideBg = slideBg.get_attribute('src')

#将图片进行保存
load_pic('slideBlock',src_slideBlock)
load_pic('slideBg',src_slideBg)

#获取页面源代码
# html = driver.execute_script("return document.documentElement.outerHTML")
# print(html)

# 网站上的图片宽度
w2 = slideBg.size['width']
# print('w2',w2)



import cv2
# 借助opencv识别
def image_recognition(slideBlock_path,slideBg_path):
    #图片读取,获取的图片与网站图片大小不一致，网站图片经过前端处理
    image_rgb = cv2.imread(slideBlock_path)
    #图片灰度处理
    image_gray = cv2.cvtColor(image_rgb,cv2.COLOR_BGR2GRAY)
    #读取模块图片
    bg_rgb = cv2.imread(slideBg_path,0)

    # 获取原图宽度
    w1 = bg_rgb.shape[1]

    #匹配模块位置
    match_loc = cv2.matchTemplate(image_gray,bg_rgb,cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(match_loc)
    print('value:',value)
    print('value[2][0]:',value[2][0])

    #
    return value[2][0],w1


slideBlock_path = './image/slideBlock.png'
slideBg_path = './image/slideBg.png'


def offsetDis(slideBlock_path,slideBg_path):
    # 得到滑块凹槽与左侧图片的宽度
    x, w1 = image_recognition(slideBlock_path, slideBg_path)
    # 缩放之后的宽度
    x = x * w2 / w1
    # 腾讯滑块偏移量。 x减去左边界透明部分的长度,视图上的左边界透明部分长度为原图左边界透明部分长度乘以w2/w1。
    # 之后再减去滑块左侧的长度
    x = x + 9.3 - 32
    # print('x:',x)
    # print('w2 / w1:',w2 / w1)
    return x

x = offsetDis(slideBlock_path,slideBg_path)

#设置滑块拖动
action = ActionChains(driver)
#按住模块,使其生效
action.click_and_hold(slideBlock).perform()
#拖动多少像素
action.move_by_offset(x,0)
#松开鼠标
action.release().perform()


time.sleep(10)
driver.quit()
