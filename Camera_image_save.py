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
    tool_name : �������ƣ�֧�ִ�·��
    windows_name : ��������
    """
    SLEEP_TIME = 1

    def __init__(self):
        """
        ��ʼ����������ʼ��һ��app
        """
        self.app = application.Application()
        self.k= PyKeyboard()
        dlg_spec = self.app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
        dlg_spec = self.app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi']
        print(dlg_spec.app.print_control_identifiers())

    def run(self, tool_name):
        """
        ����Ӧ�ó���
        """
        self.app.start(tool_name)
        #time.sleep(1)

    def connect(self, window_name):
        """
        ����Ӧ�ó���
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        """
        self.app.connect(title = window_name)
        #time.sleep(1)

    def close(self, window_name):
        """
        �ر�Ӧ�ó���
        """
        self.app[window_name].close()
        #time.sleep(1)

    def max_window(self, window_name):
        """
        ��󻯴���
        """
        self.app[window_name].maximize()
        #time.sleep(1)
    def min_window(self,window_name):
        self.app[window_name].minimize()

    def fine_window(self, window_name):
        self.app[window_name].find

    def menu_click(self, window_name, menulist):
        """
        �˵����
        """
        self.app[window_name].menu_select(menulist)
        #time.sleep(1)

    def input(self, window_name, controller, content):
        """
        ��������
        """
        self.app[window_name][controller].type_keys(content)
        #time.sleep(1)

    def click(self, window_name, controller):
        """
        ���������
        example:
        ��������������ͬ,����֧��������ʽ
        app[u'���ڡ����±���'][u'ȷ��'].Click()
        app.window_(title_re = u'���ڡ����±���').window_(title_re = u'ȷ��').Click()
        """
        self.app[window_name][controller].click()
        #time.sleep(1)

    def double_click(self, window_name, controller, x = 0,y = 0):
        """
        ���������(˫��)
        """
        self.app[window_name][controller].DoubleClick(button = "left", pressed = "",  coords = (x, y))
        #time.sleep(1)

    def right_click(self, window_name, controller, order):
        """
        ����Ҽ���������ƽ��в˵�ѡ��
        window_name : ������
        controller��������
        order �� ���֣��ڼ�������
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
    print(application.findwindows.find_elements(title_re=u'ȷ��'))
    #app.run(window_name)
    app.connect(window_name)
    # print(app)
    print(app.max_window(window_name))
    # time.sleep(1)
    app.input(window_name,controller,"^l")
    # print(application.findwindows.find_elements(title=u'����ļ���'))
    if application.findwindows.find_elements(title=u'����ļ���') != []:
        dlg_spec = app.connect(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
        dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").click()
        dlg_spec.window(title_re=u"����ļ���").edit.set_text('daidj')
    #     app.lick(u'����ļ���','ȷ��')
    #     #app.input(u'����ļ���', 'Button',"enter")
    # menulist= u"��׽->����->�ļ���"
    # app.menu_click(window_name, menulist)
    # app.input(u'����ļ���','Edit',path)
    # time.sleep(2.5)
    # app.click(u'����ļ���','Button')
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
    # if app.window(title=r'����ļ���', class_name='#32770').exists():
    #     dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").click()
#    print())
    #print(application.findwindows.find_element(title=u'����ļ���'))
    #change_path('aaa')
    # app = application.Application()
    # dlg_spec = app.connect(title ='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')
    # dlg_spec.print_control_identifiers()
 #  while True:
    #try:
            app = application.Application()
            dlg_spec = app.connect(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi')  # 1
            #dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").click()
            app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi').print_control_identifiers()
            app.window(title='AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi').maximize()

            if app.window(title=r'����ļ���',class_name='#32770').exists():
                app.window(title=u"����ļ���").print_control_identifiers()
                print('you')
                if dlg_spec.window(title_re=u"����ļ���").exists():
                    print('you')
                    if dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").exists():
                        print('you')
                        dlg_spec.window(title_re=u"����ļ���").close()
                #dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").click()
            app['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'].menu_select(u"��׽->����->�ļ���")
            #dlg_spec.menu_select(u"��׽->����->�ļ���")
            #dlg_spec['AMCap - C:\\Users\\Administrator\\Documents\\ZWO\\1.avi'][u"��׽"][u"����"][u"�ļ�"].cleck()
            dlg_spec.window(title_re=u"����ļ���").edit.set_text('D:\\lidar\\program\\Plot\\photos\\'+'Stable_test4')
            dlg_spec.window(title_re=u"����ļ���").window(title=u"ȷ��").click()
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

    # # ���±�����
    # tool_name = "notepad.exe"
    # # ͨ��Spy++ ��ȡwindow_name���������ı�
    # window_name = u"�ޱ��� - ���±�"
    # menulist = u"����->���ڼ��±�"
    # # ͨ��Spy++ ��ȡcontroller������������
    # controller = "Edit"
    # content = u"johnny"
    # window_name_new = content + ".txt"
    # # �������򣬼��±�ֻ�ܿ�һ��
    # app.run(tool_name)
    #app.connect(window_name)
    # app.max_window(window_name)
    # app.menu_click(window_name,menulist)
    # app.click(u'���ڼ��±�', u'ȷ��')
    # app.input(window_name,controller,content)
    # # Ctrl + a ȫѡ
    # app.input(window_name,controller,"^a")
    # # ѡ����
    # app.right_click(window_name,controller,3)
    # #ѡ��ճ��
    # app.right_click(window_name,controller,4)
    # k.tap_key(k.enter_key)
    # # Ctrl + v ճ��
    # app.input(window_name,controller,"^v")
    # # Ctrl + s ����
    # app.input(window_name,controller,"^s")
    # # �����ļ���
    # app.input(u"���Ϊ",controller,content)
    # # ����
    # app.click(u"���Ϊ","Button")
    # try:
    #     app.click(u"ȷ�����Ϊ","Button")
    # except:
    #     pass
    # finally:
    #     app.close(window_name_new)
