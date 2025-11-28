#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):
    """
    超级鹰验证码识别客户端类，用于调用超级鹰平台的验证码识别服务。

    Attributes:
        username (str): 超级鹰平台用户名
        password (str): 经过MD5加密后的密码
        soft_id (str): 软件ID，在超级鹰用户中心获取
        base_params (dict): 基础请求参数，包括用户名、密码和软件ID
        headers (dict): HTTP请求头信息
    """

    def __init__(self, username, password, soft_id):
        """
        初始化超级鹰客户端

        Args:
            username (str): 超级鹰平台用户名
            password (str): 超级鹰平台密码（明文）
            soft_id (str): 软件ID
        """
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        上传图片进行验证码识别

        Args:
            im (bytes): 图片的二进制数据
            codetype (str): 验证码类型代码，参考 http://www.chaojiying.com/price.html

        Returns:
            dict: 识别结果的JSON响应，包含识别结果、图片ID等信息
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        上传Base64编码的图片进行验证码识别

        Args:
            base64_str (str): 图片的Base64编码字符串
            codetype (str): 验证码类型代码，参考 http://www.chaojiying.com/price.html

        Returns:
            dict: 识别结果的JSON响应，包含识别结果、图片ID等信息
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        报告识别错误的验证码图片

        Args:
            im_id (str): 识别错误的验证码图片ID

        Returns:
            dict: 报错结果的JSON响应
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    # 用户中心>>软件ID 生成一个替换 96001
    chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001')
    # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    im = open('a.jpg', 'rb').read()
    # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    print(chaojiying.PostPic(im, 1902))
    #print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码

