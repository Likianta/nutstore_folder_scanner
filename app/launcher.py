"""
nutstore_folder_scanner v1.2.2

工作流程:
    1. 输入你要遍历的主目录
    2. 输入你要标记的文件(夹)名(否则将标记全部开头为"."的名字)
    3. 输入你要标记的文件数阈值(比如输入500,则表示如果某个文件夹中有超过500个文件,则该文件夹所在的路径会被标记)

更新日志:
    1.0
        创建项目
        增加对".idea"文件夹的扫描
    1.1
        增加对文件数大于500的文件夹的过滤
    1.2
        将项目名称由"idea_folder_scanner"改为"nutstore_folder_scanner"
        增加对文件大小在500mb以上的文件的过滤
        将阈值改为自定义阈值
        对三类路径分开收集

"""
from common_utils import lk_logger, read_and_write_basic
import os

lk = lk_logger.main(__name__)
collector = {
    '.*'                 : [],
    'filesnum_overnumber': [],
    'filesize_overnumber': []
}


def main(dir_in, filter_name='.*', filesnum_threshold=500, filesize_threshold=500):
    """
    
    :param dir_in: str. 要扫描的主目录,使用绝对路径,建议用反斜杠,示例:'D:\likianta\lk_workspace\com_qwings_data'
    :param filter_name: str. 要过滤掉的文件夹名字,默认过滤掉所有以"."开头的文件夹路径
    :param filesnum_threshold: int. 如果某文件夹的所含文件数量大于这个值,就记录它的路径
    :param filesize_threshold: int. 如果某文件的大小超过这个值(单位是mb),就记录它的路径
    :return:
    """
    lk.record_launch_func()
    
    assert ':' in dir_in
    dir_in = dir_in.replace('/', '\\')
    assert os.path.exists(dir_in)
    
    digger(dir_in, filter_name, filesnum_threshold, filesize_threshold)
    
    writer = read_and_write_basic.FileSword('../temp/out.txt')
    
    writer.write('\n# filter name')
    writer.write(collector['.*'])
    writer.write('\n# filesnum_overnumber')
    writer.write(collector['filesnum_overnumber'])
    writer.write('\n# filesize_overnumber')
    writer.write(collector['filesize_overnumber'])
    
    lk.divider_line()
    if any(collector.values()):
        lk.prt(
            '[I] collector found.'
            '\tlen(collector[".*"]) = {}'
            '\tlen(collector["filesnum_overnumber"]) = {}'
            '\tlen(collector["filesize_overnumber"]) = {}'.format(
                len(collector[".*"]),
                len(collector["filesnum_overnumber"]),
                len(collector["filesize_overnumber"])
            )
        )
    else:
        lk.prt('[W] no collected path found')


def digger(dir_in, filter_name, filesnum_threshold, filesize_threshold):
    if dir_in[-1] != '\\':
        dir_in += '\\'
    
    for i in os.listdir(dir_in):
        curr_path = dir_in + i
        
        if os.path.isdir(curr_path):
            if is_name_matched(i, filter_name):
                lk.prt('[I2140] target name matched.\tpath name = {}'.format(curr_path))
                collector['.*'].append(curr_path)
            
            elif is_too_many_files_inside(curr_path, filesnum_threshold):
                lk.prt('[I2205] is_too_many_files_inside().\tpath name = {}'.format(curr_path))
                collector['filesnum_overnumber'].append(curr_path)
            
            else:
                lk.prt('digging deeper in "{}"'.format(curr_path), count_up=True)
                lk.total_count += 1
                digger(curr_path, filter_name, filesnum_threshold, filesize_threshold)
        
        elif is_too_big_this_file(curr_path, filesize_threshold):
            """
            注意:坚果云不能忽略文件,只能忽略文件夹.因此这里我们要
            """
            dirname = os.path.dirname(curr_path)
            dirname = dirname.replace('/', '\\')
            if dirname not in collector['filesize_overnumber']:
                lk.prt('[I3634] is_too_big_this_file().\tdirname = {}'.format(dirname))
                collector['filesize_overnumber'].append(dirname)


# ----------------------------------------------------------------

def is_name_matched(path, match_name):
    if match_name == '.*':
        return path[0] == match_name[0]
    else:
        return path == match_name


def is_too_many_files_inside(dir_in, threshold):
    return len(os.listdir(dir_in)) > threshold


# 以mb为文件体积单位
unit_mb = 1024 * 1024


def is_too_big_this_file(file, threshold):
    filesize = os.path.getsize(file)
    filesize = filesize / unit_mb
    return filesize > threshold


# ----------------------------------------------------------------

if __name__ == '__main__':
    main(r'E:\com_qwings_data', '.idea', 500, 200)  # home
    # main(r'D:\likianta\lk_workspace\com_qwings_data', '.idea', 500, 200)  # work
    
    lk.print_important_msg()
    lk.over()
    lk.dump_log()
