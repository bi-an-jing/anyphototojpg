'''
    作者: BAJ

    新手练手项目 之 一个任何格式的图片转jpg格式的小脚本

    依赖 opencv-python
    如果没有安装的话需要手动安装
        windows: pip install opencv-python
        Linux:   pip3 install opencv-python
'''


import os
import sys
import cv2
import time


def my_mkdir(dir_name: str):
    '''
        这是一个带有异常处理的创建文件夹函数
        函数名:  my_mkdir
        参数:    dir_name: str    指的是要创建的文件夹名称
        返回值:  bool             成功创建文件夹返回 True
                                 文件夹已存在返回 False
    '''
    print('正在创建 文件夹' + dir_name)
    try:
        os.mkdir(dir_name)
        print('文件夹', dir_name, '创建成功')
    except FileExistsError:
        print('该目录下已经存在该文件夹 不需要重复创建', dir_name)
        return False
    return True

def my_chdir(path: str):
    '''
        这是一个带有异常处理的切换工作目录函数
        函数名:  my_chdir
        参数:    path: str       指的是即将要切换的目标工作目录
        返回值:  当成功切换至指定工作目录时 返回True
                 否则直接退出程序 避免后续的操作影响其他工作目录下的文件
    '''
    print('正在尝试进入 文件夹b')
    try:
        os.chdir(path)
        return True
    except FileNotFoundError:
        print('该路径:', path, '不存在\n为了避免误操作')
        input('程序正在退出\n按回车以继续。。。。。。')
        sys.exit(0)

def my_rename(file_name: str, new_first_name: str):
    '''
        这是一个不修改文件拓展名的情况下只修改文件名的函数
        函数名: my_rename
        参数:
            file_name str  原文件名(需要完整文件名, 包含拓展名)
            new_first_name 新的文件名(不包含拓展名)
        返回值:
            将修改后新的文件名返回(包含拓展名)

        (未完成该函数的编写)未来需要加入异常逻辑
            1、文件不存在引发异常 (异常处理)
            2、原文件名没有拓展名 ('.' in obj 解决)
    '''
    # 将文件名反转
    i_ = file_name[::-1]
    # 获取文件扩展名 (万一没有文件拓展名呢)
    last_name = i_[:i_.find('.')][::-1]
    # 新的文件名
    new_name = new_first_name + '.' + last_name
    # 调用os的方法实现文件名的修改
    os.rename(file_name, new_name)
    # 将新的文件名返回出去
    return new_name

def my_copy(file_name, old_path, new_path):
    '''
        后期待优化, 应该有更加直接的复制而不是读取文件
        考虑考虑, 毕竟文件复制的本质其实就是读和写
        但是open函数有文件大小 4G 的限制
    '''
    path = os.path.abspath('.')
    my_chdir(old_path)
    f = open(file_name, 'rb')
    data = f.read()
    f.close()
    my_chdir(new_path)
    f = open(file_name, 'wb')
    f.write(data)
    f.close()
    my_chdir(path)




if __name__ == '__main__':
    # 获取进入主程序时的时间戳
    sys_time = time.time()

    # 进入对应目录进行操作
    my_chdir('b')
    my_mkdir('ok')
    my_mkdir('no')

    # 获取目录下所有的图片文件
    all_file = list(os.walk('.'))[0][2]

    # 这个变量为了给图片文件按顺序命名
    photo_file_name = 0

    # 这个只是简单的打印而已, 非必要代码
    print('获取到的图片列表为：')
    print(all_file)

    # 循环迭代每一个图片文件
    for i in all_file:
        i = my_rename(i, str(photo_file_name))
        img = cv2.imread(i)
        if img is None:
            print('图片', i, '打开失败')
            print('标记点:', i)
            my_copy(i, '.', 'no')
        else:
            my_chdir('ok')
            cv2.imwrite(str(photo_file_name)+'.jpg', img)
            photo_file_name += 1
            my_chdir('..')

    # 显示转换结果
    print('成功:', photo_file_name, '张图片')
    print('失败:', len(all_file)-photo_file_name, '张图片')

    # 做时间展示 (这个时间操作也是非必要的)
    sys_time = time.time() - sys_time
    if sys_time <= 60:
        print('历时:', sys_time, '秒')
    elif sys_time <= 3600:
        sys_time = int(sys_time)
        print('历时:', sys_time // 60, '分钟', sys_time % 60, '秒')
    else:
        sys_time = int(sys_time)
        hour = sys_time // 3600
        min = (sys_time % 3600) // 60
        s = (sys_time % 3600) % 60
        print('历时:', hour, '小时', min, '分钟', s, '秒')