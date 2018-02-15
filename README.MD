# M3U8 downloader m3u8下载器

本工具可以下载m3u8地址格式的视频。

This project provides a tool for downloading m3u8 movies.

## 安装

```
pip install m3u8_downloader
```

## 使用

```python
#encoding=utf-8
import requests
from m3u8_downloader import download_m3u8_url

m3u8_url = 'http://v3.julyedu.com/video/73/667/2a70b0e95b.m3u8'
with requests.Session() as sess:
    download_m3u8_url(m3u8_url, sess, title=u'测试视频', out_path='.')

```

## 生成包

```bash
python setup.py bdist_wheel --universal
```