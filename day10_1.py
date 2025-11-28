import re
import requests
from lxml import etree
import ddddocr
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

# 定义请求链接
url = 'https://fanqienovel.com/reader/7173216089122439711'

# 发起网络请求
response = requests.get(url, headers=headers)
# print(response.text)

# 转换成树形结构
html_tree = etree.HTML(response.text)

# 筛选小说的文字内容
data_list = html_tree.xpath('//div[@class="muye-reader-content noselect"]/div/p/text()')
# print(data_list)

# 定义正则表达式筛选规则
font_re = r'src:url\((.*?)\)format\("woff2"\)'

# 筛选出字体文件的请求链接
font_url = re.findall(font_re, response.text)[0]
print(font_url)

# 请求字体文件的链接
response = requests.get(font_url, headers=headers)

# 将字体数据保存到字体文件中
with open('../../../../../33期基础/33期基础/day10/font.woff2', 'wb') as file:
    file.write(response.content)

# 读取字体文件
font = TTFont('font.woff2')

# 从字体文件中读取cmap字典映射表
camp_dict = font.getBestCmap()
# print(camp_dict)

# 定义一个映射字典码点值作为键，文字内容作为值
map_key = {}

# 实例化一个光学字符识别对象
ocr = ddddocr.DdddOcr(show_ad=False)

# 遍历cmap_dict字典，得到单个的键
for key in camp_dict:
    # 创建一张大小为150x150的空白图片
    image = Image.new('RGB', (150, 150), color='white')

    # 给创建的空白图片绑定绘制对象，从而能够在空白图片上绘制内容
    draw = ImageDraw.Draw(image)

    # 读取字体文件中所有文字的笔画，并设置字体的大小
    font = ImageFont.truetype('dc027189e0ba4cd.woff2', 100)

    # 将读取出来的文字笔画绘制到空白的图片上
    draw.text((20, 5), chr(key), font=font, fill='black')

    # 使用ocr识别对象来识别图片中的文字
    value = ocr.classification(image)
    # print(key, value)

    # 如果识别成功
    if value:
        # 将码点值作为键，文字内容作为值
        map_key[key] = value
    else:
        # 保存绘制的图片
        image.save(f'./绘制图片/{key}.png')

# print(map_key)

# 遍历列表中的文本数据
for data in data_list:
    # 打印一行字符串数据
    # print(data)

    # 将一行字符串数据遍历成单个的字符
    for data_char in data:

        # 将单个字符使用ord函数还原成码点值
        # print(data_char, ord(data_char))

        # 从得到的映射字典中通过键取值
        data = map_key.get(ord(data_char))
        # print(data)

        # 如果没有取到值，代表当前的符号是正常的，不需要还原
        if data is None:
            print(data_char, end='')
        # 如果取到值了，就需要打印还原后的符号
        else:
            print(data, end='')

    print()
