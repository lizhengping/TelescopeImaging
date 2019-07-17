#! /usr/bin/env python
#coding=GB18030

'''
FuncName: johnny-pywinauto.py
Desc: study pywinauto
Date: 2016-10-10 14:30
Author: johnny
Home:http://blog.csdn.net/z_johnny
'''
import pywinauto
from pywinauto import application
#import PyUserInput
from pykeyboard import *
import time

class Pywin(object):
    """
    pywin framwork main class
    tool_name : 程序名称，支持带路径
    windows_name : 窗口名字
    """
    SLEEP_TIME = 1

    def __init__(self):
        """
        初始化方法，初始化一个app
        """
        self.app = application.Application()
        self.k= PyKeyboard()
        dlg_spec = self.app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
        dlg_spec = self.app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi']
        print(dlg_spec.app.print_control_identifiers())

    def run(self, tool_name):
        """
        启动应用程序
        """
        self.app.start(tool_name)
        #time.sleep(1)

    def connect(self, window_name):
        """
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        """
        self.app.connect(title = window_name)
        #time.sleep(1)

    def close(self, window_name):
        """
        关闭应用程序
        """
        self.app[window_name].close()
        #time.sleep(1)

    def max_window(self, window_name):
        """
        最大化窗口
        """
        self.app[window_name].maximize()
        #time.sleep(1)
    def min_window(self,window_name):
        self.app[window_name].minimize()

    def fine_window(self, window_name):
        self.app[window_name].find

    def menu_click(self, window_name, menulist):
        """
        菜单点击
        """
        self.app[window_name].menu_select(menulist)
        #time.sleep(1)

    def input(self, window_name, controller, content):
        """
        输入内容
        """
        self.app[window_name][controller].type_keys(content)
        #time.sleep(1)

    def click(self, window_name, controller):
        """
        鼠标左键点击
        example:
        下面两个功能相同,下面支持正则表达式
        app[u'关于“记事本”'][u'确定'].Click()
        app.window_(title_re = u'关于“记事本”').window_(title_re = u'确定').Click()
        """
        self.app[window_name][controller].click()
        #time.sleep(1)

    def double_click(self, window_name, controller, x = 0,y = 0):
        """
        鼠标左键点击(双击)
        """
        self.app[window_name][controller].DoubleClick(button = "left", pressed = "",  coords = (x, y))
        #time.sleep(1)

    def right_click(self, window_name, controller, order):
        """
        鼠标右键点击，下移进行菜单选择
        window_name : 窗口名
        controller：区域名
        order ： 数字，第几个命令
        """
        self.app[window_name][controller].right_click()
        for down in range(order):
                k.tap_key(k.down_key)
                #time.sleep(0.5)
        k.tap_key(k.enter_key)
        #time.sleep(1)

   # def press_save_image(self):
        #self.
def save_camera_image(path):
    #change_path(path)
    app = Pywin()
    k=PyKeyboard()
    window_name = 'AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'
    controller='ActiveMovie WindowVideoRenderer'
    print(application.findwindows.find_elements(title_re=u'确定'))
    #app.run(window_name)
    app.connect(window_name)
    # print(app)
    print(app.max_window(window_name))
    # time.sleep(1)
    app.input(window_name,controller,"^l")
    # print(application.findwindows.find_elements(title=u'浏览文件夹'))
    if application.findwindows.find_elements(title=u'浏览文件夹') != []:
        dlg_spec = app.connect(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
        dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").click()
        dlg_spec.window(title_re=u"浏览文件夹").edit.set_text('daidj')
    #     app.lick(u'浏览文件夹','确定')
    #     #app.input(u'浏览文件夹', 'Button',"enter")
    # menulist= u"捕捉->拍照->文件夹"
    # app.menu_click(window_name, menulist)
    # app.input(u'浏览文件夹','Edit',path)
    # time.sleep(2.5)
    # app.click(u'浏览文件夹','Button')
    # time.sleep(1)
    # app.input(window_name, controller, "^l")
    # time.sleep(1)
    app.min_window(window_name)

def try_to_save_image(FoldName):
    try:
        save_camera_image('D:\\lidar\\program\\Plot\\photos\\'+FoldName)
    except:

        # times_try=1
        # while times_try < 5:
        print('fail to save image')
        #     print('Try the {} time'.format(times_try))
        #     #print(application.findwindows.find_elements())
        #     try:
        #         save_camera_image('D:\\lidar\\program\\Plot\\photos\\'+FoldName)
        #         # k.tap_key(k.enter_key)
        #
        #     except:
        #         time.sleep(1)
        #         times_try=times_try+1

def change_path(FoldName):
    #filename='C:\\Program Files (x86)\\ZWO Design\\ZWO_USB_Cameras_DS\\USB CAMERA.ini'
    filename = 'C:\\Program Files (x86)\\ZWO Design\\ZWO_USB_Cameras_DS\\USB CAMERA.ini'
    f= open(filename, 'r')
    print('here')
    lines=f.readlines()
    for l in range(len(lines)):
        if 'StillPath'in lines[l]:
            print(lines[l])
            lines[l]= 'StillPath = D:\\lidar\\program\\Plot\\photos\\'+FoldName+'\n'
    f.close()
    ff = open(filename, 'w')
    ff.writelines(lines)
    ff.close()



if __name__ ==  "__main__":
    # app = application.Application()
    # dlg_spec = app.connect(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
    # if app.window(title=r'浏览文件夹', class_name='#32770').exists():
    #     dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").click()
#    print())
    #print(application.findwindows.find_element(title=u'浏览文件夹'))
    #change_path('aaa')
    # app = application.Application()
    # dlg_spec = app.connect(title ='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')
    # dlg_spec.print_control_identifiers()
 #  while True:
    #try:
            app = application.Application()
            dlg_spec = app.connect(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
            #dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").click()
            app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi').print_control_identifiers()
            app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi').maximize()

            if app.window(title=r'浏览文件夹',class_name='#32770').exists():
                app.window(title=u"浏览文件夹").print_control_identifiers()
                print('you')
                if dlg_spec.window(title_re=u"浏览文件夹").exists():
                    print('you')
                    if dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").exists():
                        print('you')
                        dlg_spec.window(title_re=u"浏览文件夹").close()
                #dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").click()
            app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'].menu_select(u"捕捉->拍照->文件夹")
            #dlg_spec.menu_select(u"捕捉->拍照->文件夹")
            #dlg_spec['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'][u"捕捉"][u"拍照"][u"文件"].cleck()
            dlg_spec.window(title_re=u"浏览文件夹").edit.set_text('D:\\lidar\\program\\Plot\\photos\\'+'Stable_test4')
            dlg_spec.window(title_re=u"浏览文件夹").window(title=u"确定").click()
            app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi']['ActiveMovie WindowVideoRenderer'].type_keys('^l')
            dlg_spec.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi').minimize()
            #time.sleep(10*60)
   # except:
            #print('fail')
            #time.sleep(10*60)
            #pass
#
# dlg_spec = app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi']
#     dlg_spec.print_control_identifiers()
#     print(app.Properties.child_window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'))
#     print(app.Properties.print_control_identifiers())
#
#     print(pywinauto.findwindows.find_windows())
#     while True:
#     #
#         try_to_save_image('Stable_test2')
    #save_camera_image('D:\\lidar\\program\\Plot\\photos\\Stable_test')
        # time.sleep(60)

# finally:

    # # 记事本例子
    # tool_name = "notepad.exe"
    # # 通过Spy++ 获取window_name，即标题文本
    # window_name = u"无标题 - 记事本"
    # menulist = u"帮助->关于记事本"
    # # 通过Spy++ 获取controller，即窗口类名
    # controller = "Edit"
    # content = u"johnny"
    # window_name_new = content + ".txt"
    # # 启动程序，记事本只能开一个
    # app.run(tool_name)
    #app.connect(window_name)
    # app.max_window(window_name)
    # app.menu_click(window_name,menulist)
    # app.click(u'关于记事本', u'确定')
    # app.input(window_name,controller,content)
    # # Ctrl + a 全选
    # app.input(window_name,controller,"^a")
    # # 选择复制
    # app.right_click(window_name,controller,3)
    # #选择粘贴
    # app.right_click(window_name,controller,4)
    # k.tap_key(k.enter_key)
    # # Ctrl + v 粘贴
    # app.input(window_name,controller,"^v")
    # # Ctrl + s 保存
    # app.input(window_name,controller,"^s")
    # # 输入文件名
    # app.input(u"另存为",controller,content)
    # # 保存
    # app.click(u"另存为","Button")
    # try:
    #     app.click(u"确认另存为","Button")
    # except:
    #     pass
    # finally:
    #     app.close(window_name_new)
