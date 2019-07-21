import serial, time
from serial import *
class Servotronix(object):

    def __init__(self, port):
       if 'COM' in port:
           self.port = Serial(port=port, baudrate=115200, timeout=0.01)

    def send(self, cmd):
        self.port.write(bytes(cmd+'\r', encoding = "utf8"))
        # time.sleep(0.01)
        # self.port.write('\r')

   # def recv(self, n):
   #     try:
   #         return self.port.recv(1024)
   #     except:
   #         return ''

    def cmd_return(self, cmd, ret=0):
        self.send(cmd)
        buff = ''
        while "-->" not in buff:
            buff += str(self.port.read(),encoding = "utf-8")
            # if cmd in buff and buff[-2:] == '->':
            #     drivelog('%s %d success: %s' % (cmd, self.addr, buff.replace('\r\n', '#')))
            #     return buff.split('\r')[1].strip()
        return buff.split('\r')[1].strip()
        # .split(' ')[0]

    def enable(self):
        if len(self.cmd_return('en')):
            return True
        else:
            return False

    def disable(self):
        if len(self.cmd_return('k')):
            return True
        else:
            return False

    def stop(self):
        if len(self.cmd_return('stop')):
            return True
        else:
            return False

if __name__ == '__main__':
    a=Servotronix('COM3')
    b=Servotronix('COM4')
    print(a.cmd_return('PFB'))
    print(a.cmd_return('HOMETYPE'))
    print(a.cmd_return('STOPPED'))
    a.enable()
    a.send('MOVEABS 0 0.5')
    print(a.cmd_return('STOPPED'))
    time.sleep(1)
    a.disable()

    print(b.cmd_return('PFB'))
    print(b.cmd_return('HOMETYPE'))
    print(b.cmd_return('STOPPED'))
    b.enable()
    b.send('MOVEABS 0 0.5')
    time.sleep(1)
    b.disable()