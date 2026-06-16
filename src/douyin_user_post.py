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



class DouyinUserPosted:
    """抖音用户主页作品采集模块

    负责：
    1. 遍历用户链接列表
    2. 调用 aweme/post/ API 分页获取作品列表
    3. 解析作品信息（标题、标签、互动数据等）
    4. CSV输出和可选视频下载
    """

    def __init__(self, user_link_list, top_num, down_tag, txt_msglist, logger):
        self.txt_msglist = txt_msglist
        self.logger = logger
        self.describe = []
        self.cookie_val = self.get_cookie()
        self.user_link_list = user_link_list
        self.top_num = int(top_num)
        self.down_tag = down_tag
        self.wait_sec = self.get_config_pub()
        # 当前时间戳
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 保存文件名
        self.result_file = '抖音博主视频_{}.csv'.format(now)

    def tk_show(self, context):
        """线程安全的日志输出到Tkinter Text控件"""
        self.logger.info(context)
        self.txt_msglist.delete('1.0', 'end')
        self.describe.append(context)
        self.txt_msglist.insert('insert', '\n'.join(self.describe))
        self.txt_msglist.see("end")

    def _safe_showinfo(self, title, message):
        """线程安全弹窗：子线程通过 after 回到主线程，并加入提示音"""
        try:
            if threading.current_thread() is threading.main_thread():
                self.txt_msglist.bell()
                messagebox.showinfo(title, message)
            else:
                self.txt_msglist.after(0, lambda: (self.txt_msglist.bell(), messagebox.showinfo(title, message)))
        except Exception as e:
            self.logger.error(f'[safe_showinfo] {e}')

    def _safe_showerror(self, title, message):
        """线程安全弹窗：子线程通过 after 回到主线程，并加入提示音"""
        try:
            if threading.current_thread() is threading.main_thread():
                self.txt_msglist.bell()
                messagebox.showerror(title, message)
            else:
                self.txt_msglist.after(0, lambda: (self.txt_msglist.bell(), messagebox.showerror(title, message)))
        except Exception as e:
            self.logger.error(f'[safe_showerror] {e}')

    def trans_time(self, v_timestamp):
        """10位时间戳转换为时间字符串"""
        timeArray = time.localtime(v_timestamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def trans_top(self, v_str):
        """转换-是否置顶"""
        if str(v_str) == '1':
            return '是'
        elif str(v_str) == '0':
            return '否'
        else:
            return '未知'

    def get_cookie(self):
        """从 cookie.txt 读取cookie，验证是否已配置"""
        try:
            with open('cookie.txt', mode='r', encoding='utf8') as f:
                ck_str = f.read().strip()
                if '换成自己的' in ck_str:
                    self._safe_showerror("警告", "检测到未配置cookie！先用《cookie小工具》配置好cookie，再运行采集！")
                    sys.exit()
            self.tk_show(f'cookie.txt读取成功, 5s后开始采集！')
            time.sleep(5)
        except Exception as e:
            ck_str = ''
            self.tk_show('cookie读取失败! 先用《cookie小工具》配置好cookie，再运行采集！')
            self._safe_showerror("警告", "cookie读取失败! 先用《cookie小工具》配置好cookie，再运行采集！")
            print(str(e))
            sys.exit()
        ck_str = str(ck_str).strip()
        return ck_str

    def get_config_pub(self):
        """读取公开配置文件 config_pub.json，获取等待间隔"""
        try:
            with open('config_pub.json', 'r') as file:
                text = json.load(file)
            # 读取等待时长
            wait_sec = text['wait_sec']
            if wait_sec < 1:
                self.tk_show('\n等待时长需至少1秒，请重新配置！')
                exit(1)
            self.tk_show(f'\n读取config_pub成功, 等待间隔是:{wait_sec}s')
        except Exception as e:
            wait_sec = ''
            self.tk_show('\n读取config_pub失败！请检查config_pub.json')
            self.tk_show(str(e))
            exit(1)
        return wait_sec

    def init_csv(self, csv_header):
        """初始化csv文件"""
        with open(self.result_file, 'a+', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
        self.tk_show('csv初始化完成')

    def down_dy_video(self, v_dir_name, douyin_video_url, video_url=''):
        """下载抖音视频mp4文件（带进度显示和去水印）"""
        # 原实现约40行：流式HTTP下载 + 进度条显示 + 异常处理
        pass

    def get_user_post(self):
        """[专有代码已移除] 采集用户主页作品列表

        原实现核心流程：
        1. 初始化CSV（17列：页码、作者昵称、uid、sec_uid、作者链接、粉丝数、
           视频标题、标签、链接、发布时间、时长、是否置顶、点赞/评论/收藏/推荐/转发数）
        2. 遍历用户链接列表，从URL提取 sec_uid
        3. 构造 aweme/v1/web/aweme/post/ API的30+个请求参数
        4. 构造请求认证参数
        5. 请求 API，解析 aweme_list 中的每个作品
        6. 提取作品详细信息（标题、标签话题、互动数据、视频地址等）
        7. 按 max_cursor 分页循环，控制每个博主的前N条作品
        8. 可选下载视频文件（去水印：playwm -> play）
        9. 实时写入CSV
        """
        # 初始化csv
        column_list = ['页码', '作者昵称', 'uid', 'sec_uid', '作者链接', '作者粉丝数',
                       '视频标题', '视频标签', '视频链接', '发布时间', '视频时长', '是否置顶',
                       '点赞数', '评论数', '收藏数', '推荐数', '转发数']
        self.init_csv(csv_header=column_list)
        self.tk_show('\n[专有代码已移除] 用户作品采集功能需要专有实现')

        self.tk_show('==软件作者：马哥python说==')
        self._safe_showinfo('提示', '用户作品采集功能需要专有实现，未包含在本开源版本中')
