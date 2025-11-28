import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import ddddocr
from PIL import Image, ImageDraw

# 实例化Options对象来关闭自动化特性
options = Options()
# 使用Options关闭自动化扩展，防止被检测到是使用其他工具驱动的浏览器
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 使用add_argument禁用浏览器自动化特性，防止被检测到是使用其他工具驱动的浏览器
options.add_argument('--disable-blink-features=AutomationControlled')
# 忽略证书错误，防止因为证书错误导致访问失败
options.add_argument('ignore-certificate-errors')

derive = webdriver.Chrome(options)
derive.get("https://passport.fang.com/?backurl=https%3A%2F%2Fcd.newhouse.fang.com%2Fhouse%2Fs%2F")
derive.maximize_window()
# 停止2秒
time.sleep(2)
derive.find_element(By.XPATH, '//div[@class="login-cont"]/dt/span[2]').click()
# 停止2秒
time.sleep(2)
derive.find_element(By.XPATH, '//p[@class="login-member"]/input[@id="username"]').send_keys("abcmx710")
# 停止2秒
time.sleep(2)
derive.find_element(By.XPATH, '//p[@class="login-password"]/input[@id="password"]').send_keys("qwCMX710")
# 停止2秒
time.sleep(2)
derive.find_element(By.XPATH, '//span/button[@id="loginWithPswd"]').click()
# 停止2秒
time.sleep(2)
derive.find_element(By.XPATH, '//div[@class="drag-handler verifyicon center-icon"]')
# 停止3秒
time.sleep(3)
# 定位验证码图片链接
img_backgroud_url = derive.find_element(By.XPATH, '//div[@class="img-holder"]/img[@class="img-bg"]').get_attribute("src")
img_url = derive.find_element(By.XPATH, '//div[@class="img-holder"]/img[@class="img-block"]').get_attribute("src")

# 通过图片链接下载图片，并保存
img_backgroud = requests.get(img_backgroud_url)
img_block = requests.get(img_url)
with open("image_groud.png", "wb") as file:
    file.write(img_backgroud.content)
# 实例化DdddOcr对象
cor = ddddocr.DdddOcr(show_ad=False)
# 使用cor对象调用slide_match方法，识别验证码坐标
data = cor.slide_match(img_block.content, img_backgroud.content)
print(data)
target = data['target']
x = target[0]
y = target[1]

# 使用图片处理库，绘画返回的坐标红点
image = Image.open("image_groud.png")
draw = ImageDraw.Draw(image)
box = (x-5, y-5, x + 5, y + 5)
draw.ellipse(box, fill='red')
image.save("image_groud1.png")

# 创建ActionChains动作链对象
action = webdriver.ActionChains(derive)
# 定位小滑块
slider = derive.find_element(By.XPATH, '//div[@class="drag-handler verifyicon center-icon"]')
# 长按小滑块
action.click_and_hold(slider)
# 计算鼠标移动距离
end_x = x - (slider.size["width"] * 0.5)
# 移动小滑块, 释放鼠标
action.move_by_offset(end_x, 0).release().perform()

time.sleep(15)