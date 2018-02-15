#encoding=utf-8
import requests
from m3u8_downloader import download_m3u8_url

m3u8_url = 'http://v3.julyedu.com/video/73/667/2a70b0e95b.m3u8'
with requests.Session() as sess:
    download_m3u8_url(m3u8_url, sess, title=u'测试视频', out_path='.')