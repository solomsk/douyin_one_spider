import random
import time
import requests
from urllib.parse import quote
import json
import pandas as pd
import os
import datetime
import re
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
from douyin_search_comment import DouyinSearchSpider
from douyin_user_post import DouyinUserPosted
from douyin_trans import DyTransSpider



class Log_week():
    def get_logger(self):
        self.logger = logging.getLogger(__name__)
        # 日志格式
        formatter = '[%(asctime)s-%(filename)s][%(funcName)s-%(lineno)d]--%(message)s'
        # 日志级别
        self.logger.setLevel(logging.DEBUG)
        # 控制台日志
        sh = logging.StreamHandler()
        log_formatter = logging.Formatter(formatter, datefmt='%Y-%m-%d %H:%M:%S')
        # info日志文件名
        info_file_name = time.strftime("%Y-%m-%d") + '.log'
        # 将其保存到特定目录
        case_dir = r'./logs/'
        info_handler = TimedRotatingFileHandler(filename=case_dir + info_file_name,
                                                when='MIDNIGHT',
                                                interval=1,
                                                backupCount=7,
                                                encoding='utf-8')
        self.logger.addHandler(sh)
        sh.setFormatter(log_formatter)
        self.logger.addHandler(info_handler)
        info_handler.setFormatter(log_formatter)
        return self.logger


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


def open_sugg():
    webbrowser.open("https://docs.qq.com/sheet/DVGxzT0VVSkVzSW1u?tab=981dng", new=0)


class DouyinSpiderTool:
    def __init__(self, root):
        self.root = root
        self.root.title('爬抖音聚合软件v1.7 | 马哥python说 | 公众号: 老男孩的平凡之路')
        self.root.minsize(width=850, height=715)
        # 设置图标
        try:
            self.root.iconbitmap('mage.ico')
        except:
            pass
        # 创建菜单栏
        self.create_menu()
        # 创建Tab页
        self.create_tabs()
        # 创建底部信息
        self.create_bottom_info()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="关于软件", command=self.show_about)
        file_menu.add_command(label="使用协议", command=self.show_agreement)
        if 'open_sugg' in globals():
            file_menu.add_command(label="意见收集", command=open_sugg)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_tabs(self):
        # 创建Notebook控件
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # 创建三个Tab页
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        # 添加Tab页到Notebook
        self.notebook.add(self.tab1, text="采集评论")
        self.notebook.add(self.tab2, text="采集主页作品")
        self.notebook.add(self.tab3, text="链接转换")

        # 初始化每个Tab页的内容
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()

    def init_tab1(self):
        """初始化抖音搜索评论Tab页"""
        # Tab页1：采集评论 - 包含关键词搜索、作品链接采集、评论筛选等UI控件
        # 原实现约190行Tkinter布局代码，此处用pass替代
        pass


    def init_tab2(self):
        """初始化用户帖子Tab页"""
        # Tab页2：采集主页作品 - 包含用户链接输入、下载设置等UI控件
        # 原实现约58行Tkinter布局代码，此处用pass替代
        pass


    def init_tab3(self):
        """初始化抖音转换工具Tab页"""
        # Tab页3：链接转换 - 包含三个子Tab（主页链接→抖音号、抖音号→主页链接、App→PC链接）
        # 原实现约98行Tkinter布局代码，此处用pass替代
        pass


    def create_bottom_info(self):
        # 免责声明
        claim = tk.Label(self.root,
                         text='免责声明: 禁止使用该软件从事任何违法活动，否则由此产生的一切法律后果由软件使用者自行承担，与软件开发作者无关！',
                         font=('微软', 10), fg='red')
        claim.place(x=50, y=660)
        # 版权信息
        copyright = tk.Label(self.root, text='@马哥python说 All rights reserved.', font=('仿宋', 10), fg='grey')
        copyright.place(x=290, y=675)

    def task1(self, txt_msglist):
        """[专有代码已移除] 抖音搜索任务：从UI提取参数，调用 DouyinSearchSpider.get_douyin_search()"""
        # 原实现：
        #   1. 从 self.entry_kw_video 等UI控件读取关键词、时间范围、排序等参数
        #   2. 处理 placeholder 文本
        #   3. 调用 DouyinSearchSpider(...).get_douyin_search() 启动搜索采集
        txt_msglist.delete('1.0', 'end')
        txt_msglist.insert('insert', '[专有代码已移除] 搜索采集功能需要专有实现')

    def task2(self, txt_msglist):
        """[专有代码已移除] 用户帖子任务：从UI提取参数，调用 DouyinUserPosted.get_user_post()"""
        # 原实现：
        #   1. 从 self.entry_nt 等UI控件读取用户链接列表
        #   2. 读取 top_num、下载视频开关等参数
        #   3. 调用 DouyinUserPosted(...).get_user_post() 启动作品采集
        txt_msglist.delete('1.0', 'end')
        txt_msglist.insert('insert', '[专有代码已移除] 用户作品采集功能需要专有实现')

    def task3(self, txt_msglist):
        """[专有代码已移除] 作品链接评论任务：从UI提取参数，调用 DouyinSearchSpider.get_douyin_urls()"""
        # 原实现：
        #   1. 从 self.entry_nu 等UI控件读取作品链接列表
        #   2. 解析作品ID（支持 video/note 两种类型）
        #   3. 调用 DouyinSearchSpider(...).get_douyin_urls() 启动评论采集
        txt_msglist.delete('1.0', 'end')
        txt_msglist.insert('insert', '[专有代码已移除] 作品评论采集功能需要专有实现')

    def open_url1(self, event):  # cookie小工具演示
        webbrowser.open("https://mp.weixin.qq.com/s/_tL0nYK7_VjH8QRs1VeH-w", new=0)

    def open_url3(self, event):  # PC端抖音视频链接获取方法
        webbrowser.open("https://docs.qq.com/doc/DVENicHFFbXpDZU5m", new=0)

    def open_url4(self, event):  # 过验证码
        webbrowser.open("https://mp.weixin.qq.com/s/DOYI9koeLrs6M_kXc30_7g", new=0)

    def open_url5(self, event):  # 手动取cookie
        webbrowser.open("https://www.bilibili.com/video/BV1HW421R7en", new=0)

    def show_about(self):
        messagebox.showinfo("关于软件",
                            '版本记录:\nv1.0: 发布聚合版，三软件合一\nv1.1: 新增输入框提示&mac版支持arm64\nv1.2: ck未配置提示&提示音弹窗\nv1.3: 集成自动取ck&修复只采集一页nv1.4: 新增注册入口&自定义等待\nv1.5: 新增详情采集&tab1页下载视频&改为session请求&发布时间增加月选项\nv1.6: 修复视频下载失败\nv1.6a1: 评论去除重复\nv1.7: 修复搜索验证码问题\n\n最新版软件包获取：\n公众号 "老男孩的平凡之路" 后台回复：爬抖音聚合软件')

    def show_agreement(self):
        messagebox.showinfo("使用协议",
                            """欢迎使用本软件！在使用前，请仔细阅读以下使用协议：

授权与许可：本软件仅授权用户用于合法的个人或商业用途。禁止使用本软件进行任何违法活动，包括但不限于未经授权的数据采集、侵犯知识产权和侵犯隐私权等。
责任限制：本软件开发者不对用户因使用本软件而导致的任何直接或间接损失负责。用户在使用过程中应遵守相关法律法规，并自行承担因使用本软件而产生的风险和责任。
数据隐私：本软件不会收集、存储或分享用户的个人数据。用户采集的数据应严格遵守数据保护法律和目标网站的使用政策。
更新与维护：我们有权随时对本软件进行更新和维护，用户应及时下载并安装更新，以确保软件的正常使用。
协议修改：我们保留随时修改本使用协议的权利，修改后的协议将在发布后立即生效。用户继续使用本软件即表示接受新的协议条款。

作为软件使用者，您默认接受以上协议条款。感谢理解与支持。如有疑问，请联系作者。""")


# ==================== 主窗口与Tab整合 ====================
def create_spider_root():
    # 创建日志目录
    work_path = os.getcwd()
    if not os.path.exists(work_path + "/logs"):
        os.makedirs(work_path + "/logs")
    # 创建主窗口
    root = tk.Tk()
    app = DouyinSpiderTool(root)

    # 运行主循环
    root.mainloop()


def create_login_root():
    # 创建主窗口
    root_login = tk.Tk()
    root_login.title('爬抖音聚合软件v1.7 | 马哥python说')
    # 设置窗口大小
    root_login.minsize(width=400, height=300)
    # 左上角图标
    try:
        root_login.iconbitmap('mage.ico')
    except:
        pass
    # 菜单
    menu_bar = tk.Menu(root_login)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="关于软件", command=lambda: messagebox.showinfo("关于软件",
                          '版本记录:\nv1.0: 发布聚合版，三软件合一\nv1.1: 新增输入框提示&mac版支持arm64\nv1.2: ck未配置提示&提示音弹窗\nv1.3: 集成自动取ck&修复只采集一页nv1.4: 新增注册入口&自定义等待\nv1.5: 新增详情采集&tab1页下载视频&改为session请求&发布时间增加月选项\nv1.6: 修复视频下载失败\nv1.6a1: 评论去除重复\nv1.7: 修复搜索验证码问题\n\n最新版软件包获取：\n公众号 "老男孩的平凡之路" 后台回复：爬抖音聚合软件'))
    file_menu.add_command(label="使用协议", command=lambda: messagebox.showinfo("使用协议",
                          """欢迎使用本软件！在使用前，请仔细阅读以下使用协议：

授权与许可：本软件仅授权用户用于合法的个人或商业用途。禁止使用本软件进行任何违法活动，包括但不限于未经授权的数据采集、侵犯知识产权和侵犯隐私权等。
责任限制：本软件开发者不对用户因使用本软件而导致的任何直接或间接损失负责。用户在使用过程中应遵守相关法律法规，并自行承担因使用本软件而产生的风险和责任。
数据隐私：本软件不会收集、存储或分享用户的个人数据。用户采集的数据应严格遵守数据保护法律和目标网站的使用政策。
更新与维护：我们有权随时对本软件进行更新和维护，用户应及时下载并安装更新，以确保软件的正常使用。
协议修改：我们保留随时修改本使用协议的权利，修改后的协议将在发布后立即生效。用户继续使用本软件即表示接受新的协议条款。

作为软件使用者，您默认接受以上协议条款。感谢理解与支持。如有疑问，请联系作者。"""))
    if 'open_sugg' in globals():
        file_menu.add_command(label="意见收集", command=open_sugg)
    menu_bar.add_cascade(label="File", menu=file_menu)
    root_login.config(menu=menu_bar)
    # 标题标签
    label_title = ttk.Label(root_login, text="用户登录", font=("Helvetica", 20, "bold"), background="#f0f4f7")
    label_title.pack(pady=20)
    # 控件
    # 用户名标签和输入框
    frame_username = ttk.Frame(root_login)
    frame_username.pack(pady=10)
    label_username = ttk.Label(frame_username, text="账号:", font=("Helvetica", 12), width=10)
    label_username.pack(side="left", padx=5)
    entry_username = ttk.Entry(frame_username, font=("Helvetica", 12), width=20)
    entry_username.pack(side="right")
    # 密码标签和输入框
    frame_password = ttk.Frame(root_login)
    frame_password.pack(pady=10)
    label_password = ttk.Label(frame_password, text="密码:", font=("Helvetica", 12), width=10)
    label_password.pack(side="left", padx=5)
    entry_password = ttk.Entry(frame_password, font=("Helvetica", 12), width=20, show="*")
    entry_password.pack(side="right")
    # 读取上次登录用户（开源版本跳过远程验证）
    if os.path.exists('./userinfo.txt'):
        try:
            with open('./userinfo.txt', 'r') as f:
                userinfos = f.readlines()
                last_username = str(userinfos[0]).strip()
                last_password = str(userinfos[1]).strip()
                entry_username.insert(0, last_username)
                entry_password.insert(0, last_password)
        except:
            pass

    def login():
        """[专有代码已移除] 原实现通过 check_user() 连接远程数据库验证许可证"""
        # 开源版本：直接跳过登录进入主界面
        username = entry_username.get()
        print('username:', username)
        password = entry_password.get()
        print('password:', password)
        # [专有代码已移除] 远程许可证验证
        messagebox.showinfo('登录成功', '开源版本无需验证，直接进入主界面')
        root_login.destroy()
        create_spider_root()

    # 按钮框架
    frame_buttons = ttk.Frame(root_login)
    frame_buttons.pack(pady=20)
    # 登录按钮
    btn_login = ttk.Button(frame_buttons, text="登录", command=login, width=10)
    btn_login.grid(row=0, column=0, padx=10)
    # 退出按钮
    btn_quit = ttk.Button(frame_buttons, text="退出", command=root_login.quit, width=10)
    btn_quit.grid(row=0, column=1, padx=10)

    # 版权信息
    copyright = tk.Label(root_login, text='@马哥python说 All rights reserved.', font=('仿宋', 10), fg='grey')
    copyright.place(x=80, y=275)

    # 循环消息
    root_login.mainloop()


if __name__ == "__main__":
    # 创建日志目录
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log = Log_week()
    logger = log.get_logger()
    # 开启主程序
    create_login_root()
