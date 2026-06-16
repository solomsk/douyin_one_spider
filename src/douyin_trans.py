import random
import time
import requests
from urllib.parse import quote
import json
import pandas as pd
import os
import datetime
import re
import sys
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
from urllib import parse
import urllib.parse
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import csv
from functools import partial
import subprocess
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')



class DyTransSpider:
    """抖音链接转换模块

    提供三种转换功能：
    1. 主页链接 → 抖音号（通过 user/profile/other/ API）
    2. 抖音号 → 主页链接/uid/sec_uid（通过 discover/search/ API）
    3. App端作品链接 → PC端作品链接（通过HTTP重定向跟踪）
    """

    def __init__(self):
        self.cookie = self.get_cookie()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Cookie': self.cookie
        }
        # 统一使用 Session，复用连接与 cookie 上下文
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        # 保存文件名
        self.result_file = None

    def get_cookie(self):
        """从 cookie.txt 读取cookie"""
        cookie_text = ''
        try:
            with open('cookie.txt', 'r', encoding='utf8') as f:
                cookie_text = f.read().strip()
                if '换成自己的' in cookie_text:
                    messagebox.showerror("警告", "检测到未配置cookie！先用《cookie小工具》配置好cookie，再运行采集！")
                    sys.exit()
        except Exception as e:
            cookie_text = ''
            print('cookie读取失败！先用《cookie小工具》配置好cookie，再运行采集！')
            messagebox.showerror("警告", "cookie读取失败! 先用《cookie小工具》配置好cookie，再运行采集！")
            print(str(e))
            sys.exit()
        return cookie_text

    def init_csv(self, csv_header):
        """初始化csv文件"""
        with open(self.result_file, 'a+', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)

    def trans_appURL_to_pcURL(self, v_url):
        """[专有代码已移除] 把App端链接转换为PC端链接

        原实现：发送HTTP GET请求（allow_redirects=False），
        从 Location 响应头提取重定向目标URL，
        将 iesdouyin.com 替换为 douyin.com，清洗URL参数和末尾斜杠
        """
        # [专有代码已移除] HTTP重定向跟踪 + URL清洗逻辑
        return "转换功能需要专有实现"

    def trans_url_to_dyid(self, v_url):
        """[专有代码已移除] 把主页链接转换成抖音号

        原实现核心流程：
        1. 从URL提取 user_id（sec_uid）
        2. 构造 user/profile/other/ API的30+个请求参数
        3. 构造请求认证参数
        4. 请求 API，从JSON响应中提取 unique_id 或 short_id
        """
        # [专有代码已移除] API调用 + JSON解析
        return "转换功能需要专有实现"

    def trans_dyid_to_url(self, v_id):
        """[专有代码已移除] 把抖音号转换成主页链接、uid等

        原实现核心流程：
        1. 构造 discover/search/ API的30+个请求参数
        2. 请求搜索接口获取用户列表
        3. 从 user_list[0].user_info 提取 sec_uid 和 uid
        4. 拼接主页链接 https://www.douyin.com/user/{sec_uid}
        5. 异常处理：区分"搜索频繁"和"需验证码"两种错误
        """
        # [专有代码已移除] API搜索 + JSON解析 + 异常分类
        return "转换异常", "转换异常", "转换异常"
