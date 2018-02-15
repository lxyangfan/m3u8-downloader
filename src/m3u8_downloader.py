#! -*- encoding:utf-8 -*-
import requests
import os
import re
import logging
import errno
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from ffmpeg_util import dir_ts_to_mp4, get_undownload_files

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger()


default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def get_file_ts_name(ts_url):
    framents = ts_url.split('/')
    return framents[len(framents) - 1]


def download_ts(ts_url, sess,  save_path='./', headers=default_headers):
    ts_name = get_file_ts_name(ts_url)
    dirname = save_path
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # Reraise if failed for reasons other than existing already
    log.debug(u'下载到目录： %s' % dirname)
    xxx = None
    try:
        xxx = sess.get(ts_url, headers=headers, timeout=(3.05, 10))
    except Exception as e:
        log.warn(u'下载超时: %s' % ts_url)
        raise

    chunk_size = 1000
    with open(dirname + '/' + ts_name, 'wb') as fd:
        for chunk in xxx.iter_content(chunk_size):
            fd.write(chunk)
    log.debug(u'文件-{0}-下载完成'.format(save_path + '/' + ts_name))

def get_domain(url):
    ptn_str = r'(?<=//).+?(?=/)'
    ptn = re.compile(ptn_str)
    domain = ptn.search(url).group(0)
    di = url.index(domain)
    return url[0:di], domain, url[0:di+len(domain)]


def download_m3u8_url(m3u8, sess,title=None, out_path='.'):
    '''
        通过m3u8点播地址下载
    '''
    log.debug(m3u8)
    log.debug(u'开始解析m3u8地址内容...')
    base_url = re.search('.+(?=/\w+\.m3u8)', m3u8).group(0) # 下载ts文件的基地址
    name = re.search('(?<=/)\w+\.m3u8', m3u8).group(0)
    title = name if title is None else title
    base_file_path = os.path.abspath(os.path.dirname(out_path))
    out_path = os.path.join(base_file_path, 'outputs', title)
    file_path = os.path.join(base_file_path, 'downloads', name)

    m3u8_rsp = sess.get(m3u8)
    with open(os.path.join(base_file_path, 'm3u8', name), 'w') as fd:
        fd.write(m3u8_rsp.text)
    ts_urls = re.findall(r'(?<=,\n)(.*)(?=\n)', m3u8_rsp.text)

    log.debug(u'origin size: %d' % len(ts_urls) )
    # 筛选出没有下载的文件再下载
    get_undownload_files(ts_urls, dirname=file_path)
    log.debug(u'after size: %d' % len(ts_urls) )
    ts_urls = map(lambda x: '%s/%s' % (base_url, x), ts_urls) # 从m3u8文件中读取所有 ts的列表
    log.debug(u'>>> 所有下载任务正在开启......')
    pool = ThreadPool(50) 
    pool.map(lambda x: download_ts(x, sess, file_path), ts_urls)
    pool.close() 
    pool.join() 
    log.debug(u'>>> 所有下载任务已经完成')
    dir_ts_to_mp4(file_path, out_path)
