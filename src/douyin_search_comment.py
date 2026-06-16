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


class DouyinSearchSpider:
    """抖音搜索与评论采集模块

    负责：
    1. 关键词搜索视频列表（搜索接口）
    2. 采集视频详情（分享页解析）
    3. 采集视频评论（一级+二级评论）
    4. CSV输出与数据过滤
    """

    def __init__(self, search_keyword_list, time_range, sort, detail_tag, video_tag, max_page_video, video_id_list,
                 kw_cmt_list,
                 start_date, end_date, ip_list, max_page_cmt, max_count, level2_val, cmt_tag_val, txt_msglist, logger):
        self.txt_msglist = txt_msglist
        self.logger = logger
        self.describe = []
        self.cookie = self.get_cookie()
        self.wait_sec = self.get_config_pub()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Cookie': self.cookie,
        }
        # 统一使用 Session，复用连接与cookie上下文
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.search_keyword_list = search_keyword_list
        self.time_range = time_range
        self.sort_type = sort
        self.detail_tag = detail_tag
        self.video_tag = video_tag
        self.max_page_video = max_page_video
        self.kw_cmt_list = kw_cmt_list
        self.start_date = start_date
        self.end_date = end_date
        self.ip_list = ip_list
        self.max_page_cmt = max_page_cmt
        self.max_count = max_count
        self.video_id_list = video_id_list
        self.level2 = level2_val
        self.cmt_tag = cmt_tag_val
        # 当前时间戳
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 保存文件名1
        self.result_file1 = '抖音搜索_{}.csv'.format(now)
        # 保存文件名2
        self.result_file2 = '抖音评论_{}.csv'.format(now)
        # 保存文件名3（抖音详情）
        self.result_file3 = '抖音详情_{}.csv'.format(now)

    def tk_show(self, context):
        """线程安全的日志输出到Tkinter Text控件"""
        self.logger.info(context)
        self.txt_msglist.delete('1.0', 'end')
        self.describe.append(context)
        self.txt_msglist.insert('insert', '\n'.join(self.describe))
        self.txt_msglist.see("end")

    def _safe_showinfo(self, title, message):
        """线程安全弹窗：子线程通过 after 切回主线程执行"""
        try:
            if threading.current_thread() is threading.main_thread():
                self.txt_msglist.bell()
                messagebox.showinfo(title, message)
            else:
                self.txt_msglist.after(0, lambda: (self.txt_msglist.bell(), messagebox.showinfo(title, message)))
        except Exception as e:
            self.logger.error(f'[safe_showinfo] {e}')

    def _safe_showerror(self, title, message):
        """线程安全弹窗：子线程通过 after 切回主线程执行"""
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

    def trans_sort_type(self, v_str):
        """转换排序方式：中文标签 -> API数值"""
        if v_str == '综合排序':
            return 0
        elif v_str == '最多点赞':
            return 1
        elif v_str == '最新发布':
            return 2
        else:
            return 0

    def trans_time_range(self, v_str):
        """转换时间范围：中文标签 -> 天数"""
        if v_str == '不限':
            return 0
        elif v_str == '一天内':
            return 1
        elif v_str == '一周内':
            return 7
        elif v_str == '一月内':
            return 31
        elif v_str == '三月内':
            return 90
        elif v_str == '半年内':
            return 180
        elif v_str == '一年内':
            return 365
        else:
            return 0

    # ==================== 反爬检测（专有代码已移除） ====================

    def is_search_verify_response(self, json_data, response_text):
        """[专有代码已移除] 判断搜索接口是否返回验证码/风控页面"""
        # 原实现：检查响应文本和JSON中是否包含 captcha/verify_center/fp_verify 等关键词
        return False

    def format_search_status(self, json_data):
        """[专有代码已移除] 提取搜索接口状态信息（status_code/status_msg/has_more/logid）"""
        return ""

    def extract_search_aweme_info(self, post_item):
        """[专有代码已移除] 兼容 general/search/single 返回的两种作品数据结构"""
        # 原实现：处理 aweme_info 和 aweme_mix_info.mix_items 两种嵌套方案
        return {}

    # ==================== Cookie工具函数 ====================

    def parse_cookie_string(self, cookie_text):
        """把 cookie 字符串转成 dict，便于和 Session 新 cookie 合并"""
        cookies = {}
        for item in str(cookie_text or '').split(';'):
            item = item.strip()
            if not item or '=' not in item:
                continue
            key, val = item.split('=', 1)
            key = key.strip()
            if key:
                cookies[key] = val.strip()
        return cookies

    def build_cookie_header(self):
        """合并 cookie.txt 与预热网页返回的 Session cookie"""
        cookies = self.parse_cookie_string(self.cookie)
        for ck in self.session.cookies:
            if ck.name and ck.value is not None:
                cookies[ck.name] = ck.value
        cookie_header = '; '.join([f'{k}={v}' for k, v in cookies.items()])
        if cookie_header:
            self.session.headers.update({'Cookie': cookie_header})
        return cookie_header

    # ==================== 搜索预热与请求（专有代码已移除） ====================

    def warmup_search_session(self, search_keyword, ua):
        """[专有代码已移除] 模拟浏览器访问搜索页以获取动态cookie（ttwid等）"""
        # 原实现：请求 https://www.douyin.com/search/{keyword}?type=video
        # 使用 Sec-Fetch-* 系列请求头模拟浏览器行为
        pass

    def request_search_json(self, url, headers, params, label):
        """[专有代码已移除] 请求搜索接口并返回JSON，含验证码检测"""
        # 原实现：session.get() + JSON解析 + 验证码检测 + 错误诊断
        return None, None

    def get_cookie_value(self, name):
        """[专有代码已移除] 从 cookie.txt 和 Session 中读取指定cookie值"""
        for ck in self.session.cookies:
            if ck.name == name:
                return ck.value
        return self.parse_cookie_string(self.cookie).get(name, '')

    def get_search_webid(self):
        """[专有代码已移除] 从 s_v_web_id cookie 中提取搜索接口 webid"""
        return ''

    def build_general_search_params(self, search_keyword, cursor, count, sort_val, time_val, search_id=''):
        """[专有代码已移除] 构造 general/search/single 接口的完整请求参数

        原实现包含约30+个参数：device_platform, aid, channel, search_channel,
        keyword, offset, count, version_code, screen_width/height, browser_*,
        os_*, cpu_core_num, device_memory, platform, webid, msToken 等
        """
        params = {}
        return params

    # ==================== Cookie/配置读取 ====================

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

    # ==================== 视频下载（通用工具，完整保留） ====================

    def down_dy_video(self, v_dir_name, douyin_video_url, direct_video_url=''):
        """[专有代码已移除] 下载抖音视频mp4文件"""
        pass

    # ==================== 数据过滤（通用工具，完整保留） ====================

    def filter_data(self):
        """[专有代码已移除] 筛选评论数据：按关键词、时间范围、IP属地过滤，去重，截取最大量"""
        pass

    # ==================== 评论采集（专有代码已移除） ====================

    def get_douyin_comment(self, v_video_id_list):
        """[专有代码已移除] 采集抖音视频评论（一级+二级）

        原实现核心流程：
        1. 遍历视频ID列表
        2. 构造评论API请求参数（约30个设备指纹参数）
        3. 构造请求认证参数
        4. 请求 aweme/v1/web/comment/list/ 接口
        5. 解析JSON提取：评论内容、评论者信息、IP属地、点赞数等
        6. 二级评论通过 aweme/v1/web/comment/list/reply/ 接口递归获取
        7. 分页循环，控制最大页数和最大采集量
        8. 实时写入CSV，每页后执行 filter_data()
        """
        self.tk_show('\n[专有代码已移除] 评论采集功能需要专有实现')

        self._safe_showinfo('提示', '评论采集功能需要专有实现，未包含在本开源版本中')

    # ==================== 详情采集（专有代码已移除） ====================

    def get_douyin_detail(self, v_keyword='', v_video_url=''):
        """[专有代码已移除] 采集抖音视频详情

        原实现核心流程：
        1. 解析视频ID（支持URL和纯ID两种输入）
        2. 通过 iesdouyin.com/share/video/{id}/ 分享页获取作品JSON
        3. 从 HTML 中提取 videoInfoRes JSON 对象
        4. 解析作者信息（昵称、签名、抖音号、粉丝数、IP属地）
        5. 调用 user/profile/other/ API 补全缺失的作者uid和粉丝数
        6. 提取视频信息（标题、时长、封面、音乐、标签话题）
        7. 按码率选择最高清晰度视频下载地址
        8. 可选下载视频文件
        9. 支持批量模式和单条模式
        10. 实时写入CSV，列包含20+个字段
        """
        self.tk_show('\n[专有代码已移除] 详情采集功能需要分享页解析和API调用')
        self.tk_show('请自行实现详情采集逻辑')
        return [] if not v_video_url else {}

    # ==================== 搜索采集（专有代码已移除） ====================

    def get_douyin_search(self):
        """[专有代码已移除] 关键词搜索视频列表

        原实现核心流程：
        1. 遍历搜索关键词列表
        2. warmup_search_session() 模拟浏览器搜索页访问，获取动态cookie
        3. build_general_search_params() 构造30+个设备指纹参数
        4. 请求 aweme/v1/web/general/search/single/ 接口
        5. 解析JSON提取：视频标题、链接、作者信息、互动数据
        6. 分页循环，控制最大页数
        7. 实时写入CSV，去重后可选触发评论采集
        """
        self.tk_show('\n[专有代码已移除] 搜索采集功能需要专有实现')
        self.tk_show('请自行配置相关组件后恢复此功能')
        self._safe_showinfo('提示', '搜索采集功能需要专有实现，未包含在本开源版本中')

    def get_douyin_urls(self):
        """[专有代码已移除] 根据作品链接采集评论/详情

        原实现：根据用户选择，依次调用 get_douyin_detail() 和 get_douyin_comment()
        """
        self.tk_show('\n[专有代码已移除] 作品链接采集功能需要专有实现')
        self.tk_show('请自行配置相关组件后恢复此功能')
        self._safe_showinfo('提示', '作品链接采集功能需要专有实现，未包含在本开源版本中')
