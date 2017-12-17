#encoding=utf-8
__author__ = 'benli'

from tkinter import *
from serial import *
import ttk
import time
import threading
import re
from  telescope import *

class GUI(Frame):

    #message=''

    def __init__(self,master):
        frame = Frame(master)
        frame.pack()


        #串口号提示
        self.lab1 = Label(frame,text = 'Serial Number')
        self.lab1.grid(row = 0,column = 0,sticky = W)
        #串口号选择下拉菜单
        self.boxValue = StringVar()
        self.boxChoice = ttk.Combobox(frame,textvariable = self.boxValue,state = 'readonly')
        self.boxChoice['value'] = ('COM1','COM2','COM3','COM4')
        self.boxChoice.current(0)
        self.boxChoice.bind('<<ComboboxSelected>>',self.Choice)
        self.boxChoice.grid(row = 1,column = 0,sticky = W)
        #波特率选择提示
        self.lab2 = Label(frame,text = 'Baudrate Set')
        self.lab2.grid(row = 2,column = 0,sticky = W)
        #波特率选择下拉菜单
        self.boxValueBaudrate = IntVar()
        self.BaudrateChoice = ttk.Combobox(frame,textvariable = self.boxValueBaudrate,state = 'readonly')
        self.BaudrateChoice['value'] = (9600,115200)
        self.BaudrateChoice.current(0)
        self.BaudrateChoice.bind('<<ComboboxSelected>>',self.ChoiceBaudrate)
        self.BaudrateChoice.grid(row = 3,column = 0,sticky = W)
        #输出框提示
        self.lab3 = Label(frame,text = 'Message Show')
        self.lab3.grid(row = 0,column = 1,sticky = W)
        #输出框
        self.show = Text(frame,width = 40,height = 5,wrap = WORD)
        self.show.grid(row = 1,column = 1,rowspan = 4,sticky = W)
        #输入框提示
        self.lab4 = Label(frame,text = 'Input here,please!')
        self.lab4.grid(row = 5,column = 1,sticky = W)
        #输入框
        self.input = Entry(frame,width = 40)
        self.input.grid(row = 6,column = 1,rowspan = 4,sticky = W)
        #输入按钮
        self.button1 = Button(frame,text = "Input",command = self.Submit)
        self.button1.grid(row = 11,column = 1,sticky = E)
        #串口开启按钮
        self.button2 = Button(frame,text = 'Open Serial',command = self.open)
        self.button2.grid(row = 7,column = 0,sticky = W)
        #串口关闭按钮
        self.button3 = Button(frame,text = 'Close Serial',command = self.close)
        self.button3.grid(row = 10,column = 0,sticky = W)
        #串口信息提示框
        self.showSerial = Text(frame,width = 20,height = 2,wrap = WORD)
        self.showSerial.grid(row = 12,column = 0,sticky = W)
        #状态提示框
        self.lab5 = Label(frame,text = 'Current State')
        self.lab5.grid(row = 13,column = 0,sticky = W)
        #E角
        self.lab6 = Label(frame,text = 'E=111')
        self.lab6.grid(row = 14,column = 0,sticky = W)
        #e角
        self.lab7 = Label(frame,text = 'e=111')
        self.lab7.grid(row = 14,column = 1,sticky = W)
        #序号
        self.lab8 = Label(frame,text = 'No.=')
        self.lab8.grid(row = 15,column = 0,sticky = W)

        '''
        #串口初始化配置
        #串口设置相关变量
        self.port = 'COM2'
        self.baudrate = 9600
        self.ser = Serial()
        self.ser.setPort(self.port)

       ####OPEN###
        self.ser.open()
        print (self.ser.isOpen())
        print (self.ser)
        threading._start_new_thread(self.read_data,())
        '''

    def Choice(self,event):
        context = self.boxValue.get()
        list = ["COM1",'COM2','COM3','COM4']
        if context in list:
            self.port = context
                #str(list.index(context))
            print(self.port)
            self.ser.setPort(self.port)
        print(self.port)
    def ChoiceBaudrate(self,event):
        self.baudrate = self.boxValueBaudrate.get()
        self.ser.setBaudrate(self.baudrate)
        print(self.baudrate)
    def Submit(self):
        context1 = self.input.get()
        context1=tele1.seri.Send(( bytes(context1, encoding = "utf8")))
        #context1 = self.input.get()
        #print(str.encode(context1))
        n = self.ser.write( bytes(context1, encoding = "utf8"))

        #output = self.ser.read(n)
        #print(output)
        #self.show.delete(0.0,END)


    def read_data(self):
        message=''
        char=''
        response=[]
        while True:
            char+=str(self.ser.read_all(),encoding = "utf-8")
            if char != '':
                message+=char
                #print(message)
                if char=='#':
                    self.show.insert(INSERT,message)
                    self.show.insert(INSERT,'\n')
                    self.show.see(END)
                    message=message[:-1]
                    response=re.split(',',message)
                    response=list(map(lambda x: int(x, 16), response))
                    if len(message)==9:
                        E=response[0]*(1/65536*360)
                        A=response[1]*(1/65536*360)
                    if len(message)==17:
                        E=response[0]*(1/16777216*360)
                        A=response[1]*(1/16777216*360)
                    response=[E,A]
                    print(response)
                    message=''
                char=''



    def open(self):
        self.ser.open()
        if self.ser.isOpen() == True:
            self.showSerial.delete(0.0,END)
            self.showSerial.insert(0.0,"Serial has been opend!")
    def close(self):
        self.ser.close()
        if self.ser.isOpen() == False:
            self.showSerial.delete(0.0,END)
            self.showSerial.insert(0.0,"Serial has been closed!")
if __name__=='__main__':
    tele1=Tele('com2')
    root = Tk()
    root.title("Serial GUI")
    root.geometry("500x400")
    app = GUI(root)
    root.mainloop()
    print('The window is closed')