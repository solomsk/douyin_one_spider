# Douyin One Spider - Douyin Data Collection Tool

**Author:** [@马哥python说](https://github.com/mashukui)  
**Version:** v1.0  
**License:** Commercial Software  
**Language:** Python 3.x

---

## 🌐 Language Switcher

**中文 / English**

This project supports bilingual interface with instant language switching:

**[中文版 README](README.md)** | **[English README](README.en.md)**

### 🔄 How to Switch Language

1. **Read in English** - Use this README for English documentation
2. **Read in Chinese** - Switch to Chinese version for localized content

Both versions contain the same features and documentation, just in different languages.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [Usage](#usage)
- [Pricing](#pricing)
- [Technical Details](#technical-details)
- [FAQ](#faq)

---

## 🎯 Overview

**Douyin One Spider** is a comprehensive data collection tool for Douyin (TikTok China), designed for researchers, marketers, and content creators. This GUI application integrates three essential functions into one platform:

- 📝 **Comment Collection** - Scrape comments from search results or specific videos
- 🎬 **User Post Collection** - Extract posts from any Douyin user's homepage
- 🔗 **Link & UID Conversion** - Convert between different Douyin link formats and user IDs

---

## ✨ Features

### Feature 1: Comment Collection

Collect comments from Douyin search results or specific videos.

**Collected Data Fields (11 fields):**
- Target URL
- Page Number
- Commenter Nickname
- Commenter ID
- Commenter UID
- Commenter Profile Link
- Comment Time
- Comment IP Location
- Comment Likes
- Comment Level
- Comment Content

**Sample Data:**
```csv
目标链接,页码,评论者昵称,评论者id,评论者uid,评论者主页链接,评论时间,评论IP属地,评论点赞数,评论级别,评论内容
https://www.douyin.com/video/7123456789,1,张三,zhangsan,7123456789,https://www.douyin.com/user/7123456789,2026-03-10 08:00:00,北京市,128,1,这个视频很不错！
```

### Feature 2: User Post Collection

Extract all posts from any Douyin user's homepage.

**Collected Data Fields (17 fields):**
- Page Number
- Author Nickname
- UID
- Sec_UID
- Author Link
- Followers Count
- Video Title
- Video Tags
- Video Link
- Publish Time
- Video Duration
- Is Pinned
- Likes
- Comments
- Favorites
- Shares
- Recommendations

**Sample Data:**
```csv
页码,作者昵称,uid,sec_uid,作者链接,作者粉丝数,视频标题,视频标签,视频链接,发布时间,视频时长,是否置顶,点赞数,评论数,收藏数,推荐数,转发数
1,科技达人,7123456789,MS4wLjABAAAA7123456789...,https://www.douyin.com/user/7123456789,125800,Python爬虫教程,编程,https://www.douyin.com/video/7123456789,2026-03-10 07:00:00,03:45,是,12500,890,3200,4500,6700
```

### Feature 3: Link & UID Conversion

Convert between different Douyin link formats and user IDs.

**Supported Conversions:**
1. Homepage URL → Douyin ID (UID)
2. Douyin ID → Homepage URL (with UID)
3. App Link → PC Link

---

## 💡 Use Cases

This tool is ideal for:

- **Lead Generation:** Collect target users from comment sections of popular posts in your niche
- **Data Analysis:** Scrape Douyin topic data for sentiment analysis, social media research, and trend tracking
- **Content Research:** Analyze top creators' content styles and trending topics for inspiration
- **Douyin Operations:** Convert between different link formats for cross-platform collaboration

---

## 🚀 Installation

### System Requirements

- **Operating System:** Windows 10/11 or macOS 10.15+
- **Python:** 3.7+ (not required - application includes Python runtime)
- **RAM:** 4GB minimum
- **Storage:** 500MB free space

### Installation Steps

1. **Download the latest version:**
   - Visit: [https://github.com/mashukui/douyin_one_spider](https://github.com/mashukui/douyin_one_spider)
   - Or scan the QR code in the "老男孩的平凡之路" (Old Boy's Ordinary Path) official account

2. **Extract the package:**
   - Extract `douyin_one_spider_v1.0.zip` to your desired location

3. **Run the application:**
   - Double-click `douyin_one_spider.exe` (Windows) or `DouyinOneSpider.app` (macOS)
   - No additional configuration required

---

## 📖 Usage

### Step-by-Step Guide

#### 1. Login

Launch the application and log in with your Douyin account.

**Cookie Auto-Configuration:**
The tool includes a built-in "Cookie Helper" that automatically configures your login cookies.

1. Click "Cookie Helper" button
2. Login to Douyin through the browser popup
3. Cookie is automatically saved to `cookie.txt`
4. No manual cookie editing required!

![Cookie Helper](https://private-user-images.githubusercontent.com/228842838/544637247-1ce912fd-1123-4ae2-8fa9-4618dc3d96e9.jpg)

#### 2. Select Function

Choose one of three modes:
- 🔍 Search Comments (search by keyword)
- 👤 User Posts (extract posts from homepage)
- 🔄 Link Conversion (convert link formats)

#### 3. Configure Parameters

**For Comment Collection:**
- Enter keywords to search
- Set time range (optional)
- Select number of pages to scrape

**For User Posts:**
- Enter user's Douyin homepage URL
- Select page range

**For Link Conversion:**
- Paste the link you want to convert
- Select conversion type

#### 4. Start Collection

Click **"Start"** button and monitor progress in real-time.

**Features:**
- Real-time progress display
- Automatic data saving (every page)
- Detailed log file generation
- CSV output format

#### 5. Review Results

After completion, check the CSV files in the same folder:
- `comments_*.csv` - Collected comments
- `posts_*.csv` - Collected posts
- `logs/*.log` - Execution logs

**Note:** Data is saved after each page (not all at once) to prevent data loss from unexpected interruptions.

---

## 💰 Pricing

### Subscription Plans

| Plan | Duration | Price | Features |
|------|----------|-------|----------|
| **Daily Pass** | 1 day | ¥39 | Single use, suitable for trial |
| **Monthly Pass** | 1 month | ¥149 | Multiple uses, short-term projects |
| **Quarterly Pass** | 3 months | ¥399 | Multiple uses, medium-term projects |
| **Yearly Pass** | 1 year | ¥799 | Multiple uses, long-term projects |

### Purchase Methods

#### Method 1: Self-Service (Recommended)
- **Platform:** [https://mgnb.pro/product/douyin](https://mgnb.pro/product/douyin)
- **XET:** [https://kjyjf.xetlk.com/s/36ksUh](https://kjyjf.xetlk.com/s/36ksUh)

#### Method 2: Manual Payment
- Contact via WeChat: 493882434
- Send payment receipt
- Receive activation code

### License Mechanism

- **One-device activation:** Each license key is bound to one computer
- **No multi-login:** Cannot run on multiple computers simultaneously
- **Anti-resale:** Licenses are non-transferable

---

## 🛠️ Technical Details

### Architecture

**Core Technologies:**
- **GUI:** `tkinter` (Python built-in)
- **HTTP Requests:** `requests`
- **Data Parsing:** `json`
- **CSV Export:** `pandas`
- **Logging:** `logging`

**Data Collection Method:**
- Uses Douyin's official API protocol
- NOT browser automation (no RPA/Selenium)
- **Advantages:** Higher stability, faster speed, lower resource usage

### Code Structure

```python
# Request and parse data
r = requests.get(url, headers=headers, params=params)
json_data = r.json()

# Parse comment content
for comment in comment_list:
    text = comment['text']
    text_list.append(text)

# Save to CSV
df = pd.DataFrame({
    'Target URL': f'https://www.douyin.com/video/{video_id}',
    'Page': page,
    'Commenter': user_name_list,
    'Commenter ID': user_id_list,
    'Commenter UID': uid_list,
    'Comment Time': create_time_list,
    'Comment IP': ip_list,
    'Likes': like_count_list,
    'Level': cmt_level_list,
    'Content': text_list,
})
df.to_csv(self.result_file, mode='a+', index=False, encoding='utf_8_sig')
```

### Logging System

Logs are automatically generated in the `logs/` folder with the format:
```
[2026-03-10 08:00:00]-douyin_one_spider.py][collect_comments-156]--Starting comment collection...
[2026-03-10 08:00:05]-douyin_one_spider.py][collect_comments-158]--Page 1 completed: 45 comments saved
```

---

## 📚 Documentation & Support

### Video Tutorial

**[【Tool Demo】Douyin One Spider Collection Tool](https://mp.weixin.qq.com/s/fDb21Rj_kKb_1GNHAJWyIQ)**

### Official Channels

- **GitHub:** [https://github.com/mashukui/douyin_one_spider](https://github.com/mashukui/douyin_one_spider)
- **WeChat Official Account:** 老男孩的平凡之路
- **Search "爬抖音聚合软件"** to get the latest version

### FAQ

**Q: Is this software free?**  
A: No, this is commercial software. See pricing section above.

**Q: Does it work on both Windows and Mac?**  
A: Yes! Both Windows 10/11 and macOS 10.15+ are supported.

**Q: Do I need to know Python to use it?**  
A: No! The application is GUI-based and requires no programming knowledge.

**Q: Is data saved automatically?**  
A: Yes! Data is saved after each page to prevent loss from interruptions.

**Q: Can I use it on multiple computers?**  
A: No, each license is bound to one computer. See license mechanism above.

**Q: What format is the output?**  
A: CSV format, compatible with Excel, Google Sheets, and other data analysis tools.

---

## ⚠️ Important Notice

### Legal & Ethical Use

This tool is **for academic research and data analysis purposes ONLY**. Users must:

1. Comply with all relevant laws and regulations
2. Respect Douyin's Terms of Service
3. Use data responsibly and ethically
4. **NOT** use for commercial spam, harassment, or illegal activities

### Disclaimer

- **Author:** [@马哥python说](https://github.com/mashukui)
- **All rights reserved**
- Software is independently developed and maintained
- Regular updates and bug fixes provided

---

## 🙏 Acknowledgments

Special thanks to all users who have provided feedback and support!

---

## 📄 License

Copyright © 2026 [@马哥python说](https://github.com/mashukui). All rights reserved.

---

**Support:** If you encounter any issues, please contact via WeChat: 493882434  
**Version:** v1.0  
**Last Updated:** 2026-03-10
