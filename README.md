# NetEase Cloud Music Song Keyword Analysis System

This is a system for analyzing Chinese song keywords from NetEase Cloud Music, which can generate keyword frequency rankings by year.

Ada

## Features

- 🔍 Search and extract song information directly from NetEase Cloud Music website
- 📝 Extract song lyrics from web pages
- 🗣️ Use jieba for Chinese word segmentation
- 📊 Count keyword frequencies by year
- 🏆 Generate yearly keyword rankings
- 💾 Save analysis results to JSON files

## Installation

```powershell
pip install -r requirements.txt
```

## Usage

### Run Main Program

```powershell
python youqian.py
```

### Run Tests

```powershell
python test_analyzer.py
```

## 系统架构

### 主要组件

1. **NetEaseMusicAnalyzer**: 主分析器类
   - `search_songs()`: 搜索歌曲
   - `get_song_details()`: 获取歌曲详情
   - `get_lyrics()`: 获取歌词
   - `extract_keywords()`: 提取关键词
   - `analyze_songs()`: 分析歌曲
   - `generate_rankings()`: 生成排行榜

2. **关键词提取**
   - 使用jieba进行中文分词
   - 过滤长度小于2的词
   - 只保留字母字符

3. **年度分析**
   - 按歌曲发布年份分组
   - 统计每个关键词的出现频率
   - 生成年度排行榜

## 输出格式

### 控制台输出
```
年度关键词排行榜
============================================================

2020年:
----------------------------------------
 1. 爱情        (出现 15 次)
 2. 家          (出现 12 次)
 3. 钱          (出现 10 次)
...
```

### JSON输出文件
```json
{
  "songs_data": [...],
  "keywords_by_year": {...},
  "rankings": {...},
  "analysis_time": "2024-01-01T12:00:00"
}
```

## 配置选项

在`main()`函数中可以修改：

- `search_keywords`: 搜索关键词列表
- `songs_per_keyword`: 每个关键词搜索的歌曲数量
- `top_n`: 显示的关键词数量

## 注意事项

⚠️ **重要提醒**:
- 本系统仅用于学习和研究目的
- 请遵守网易云音乐的使用条款
- 建议添加适当的请求延迟避免被封
- 实际使用时可能需要处理更复杂的加密算法

## 技术栈

- Python 3.7+
- requests: HTTP请求
- jieba: 中文分词
- json: 数据存储
- collections: 数据统计

## 扩展功能

可以考虑添加的功能：
- 情感分析
- 词云生成
- 可视化图表
- 数据库存储
- 多线程处理
