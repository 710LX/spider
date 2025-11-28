from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from chaojiying import Chaojiying_Client

# 初始化浏览器
driver = webdriver.Chrome()
# 将浏览器最大化
driver.maximize_window()
driver.get('https://www.chaojiying.com/user/login/?url=/user/mysoft/')
# 缓存2秒
time.sleep(2)
# 定位账号输入框，并输入账号
driver.find_element(By.XPATH,'//input[@name="user"]').send_keys('laihao710')
# 缓存2秒
time.sleep(2)
# 定位密码输入框，并输入密码
driver.find_element(By.XPATH,'//input[@name="pass"]').send_keys('1sx2ro9w')
# 缓存2秒
time.sleep(2)
# 定位验证码图片位置，并截图保存
driver.find_element(By.XPATH,'//form[@name="fm2"]/div/img').screenshot('code.png')
# 缓存2秒
time.sleep(2)
# 使用超级鹰识别验证码图片内容
chaojiying = Chaojiying_Client('laihao710', '1sx2ro9w', '972670')
image = open('code.png', 'rb').read()
data = chaojiying.PostPic(image, 1902)

# 定位验证码输入框，并输入验证码
driver.find_element(By.XPATH,'//input[@name="imgtxt"]').send_keys(data['pic_str'])
# 缓存2秒
time.sleep(2)
# 点击登录按钮
driver.find_element(By.XPATH,'//input[@type="submit"]').click()
time.sleep(10)



