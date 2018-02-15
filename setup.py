#encoding=utf-8
from setuptools import setup,find_packages

setup(
    name='m3u8_downloader',
    version='1.0.3',
    author='Frank Yang',
    author_email='lxyangfan@gmail.com',
    license = 'MIT License',  
    url='http://www.fr4nk.cn',
    description=u'这是一个m3u8视频地址下载器。 This is a downloading tool for m3u8 urls.',
    packages = find_packages(),
    install_requires = [
        'beautifulsoup4==4.6.0',
        'requests==2.18.4',
        'lxml==4.1.0'
    ],
    dependency_links = [
        "https://www.ffmpeg.org/"
    ]
)