#! -*- encoding:utf-8 -*-
import sys
import subprocess
import argparse
import os
import re
import errno
import logging

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__file__)

'''
    将列表中所有的ts文件合并并转换为mp4
    files: 所有文件的列表
    output: 输出文件的详细地址
'''
def join_ts_to_mp4_with_small_number(files, output='output'):
    params = ['ffmpeg', '-y', '-i']
    params.append('concat:')
    for file in files:
        if os.path.isfile(file):
            params[-1] += file + '|'
    params += ['-c', 'copy']
    params.append(output+'.mp4')
    if subprocess.call(params, stdin=None) == 0:
        log.info(u'合并成功！')
        return True
    else:
        raise Exception(u'执行合并文件失败！')

def join_ts_to_mp4_with_large_number(files_list, output='output'):
    '''
        使用 ffmpeg将文件列表的ts文件合并转换为 MP4
    '''
    params = ['ffmpeg','-safe', '0', '-f', 'concat', '-i']
    params.append(files_list)
    params += [ '-bsf', 'aac_adtstoasc']
    params += ['-c', 'copy']
    params.append(output+'.mp4')
    if subprocess.call(params, stdin=None) == 0:
        log.info(u'合并成功！')
        return True
    else:
        raise Exception(u'执行合并文件失败！')


def get_concat_file_list(dirname='.', file_ext=".ts"):
    '''
        从文件夹中获取所有对应后缀名文件列表，并按照序号排序
    '''
    file_list = [x for x in os.listdir(dirname) if x.endswith(file_ext) ]
    ordered_files = sorted(file_list, key=lambda x: (int(re.findall('([0-9]+)(?=\.ts)',x)[0]),x))
    ordered_files = [dirname+'/'+x for x in ordered_files ]
    return ordered_files

def get_undownload_files(ori_list, dirname='.', file_ext=".ts"):
    '''
        给出一个原始列表ori_list，根据目录dirname的文件列表筛选出还没下载的文件
    '''
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # Reraise if failed for reasons other than existing already
    file_list = [x for x in os.listdir(dirname) if x.endswith(file_ext) ]
    map(lambda x: ori_list.remove(x), file_list)
    return ori_list

def dir_ts_to_mp4(dirname, output='out'):
    '''
        将目录中的所有ts文件转换为mp4文件
    '''
    files  = generate_concat_list(dirname, output)
    return join_ts_to_mp4_with_large_number(files,output)

# Given a list of segments and the output path, generates the concat
# list and returns the path to the concat list.
def generate_concat_list(dirname, output):
    files = get_concat_file_list(dirname)
    concat_list_path = output + '.txt'
    concat_list_dir = os.path.dirname(concat_list_path)
    try:
        os.makedirs(concat_list_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # Reraise if failed for reasons other than existing already
    
    with open(concat_list_path, 'w') as concat_list:
        for file in files:
            if os.path.isfile(file):
                concat_list.write('file {0}\n'.format(file))
    return concat_list_path

if __name__ == "__main__":
    reload(sys)                         # 2
    sys.setdefaultencoding('utf-8')     # 3
    parser = argparse.ArgumentParser(description=u'下载视频，请输入query和存储路径')
    parser.add_argument('in_dir')
    parser.add_argument('out_file_path')
    args = parser.parse_args()
    print args
    dir_ts_to_mp4(args.in_dir, args.out_file_path)