import Tool
import newport
import time

class NewportPic():

    def __init__(self):

        idProduct = '0x4000'
        idVendor = '0x104d'
        self.idProduct = int(idProduct, 16)
        self.idVendor = int(idVendor, 16)


        self.controller = newport.Controller(idProduct=self.idProduct, idVendor=self.idVendor)

    def go_to_Target(self,channal,Targer):

        symbol=''
        # if Targer>0:
        #     symbol='+'


        command='{}PA{}{}'.format(channal,symbol,Targer)
        print(command)
        rep = self.controller.command(command)


    def get_Position(self,channal):
        command='{}TP?'.format(channal)
        rep = self.controller.command(command)
        if rep:
         return rep

    def move_steps(self,channal,steps):

        symbol = ''
        # if Targer > 0:
        #     symbol = '+'

        command='{}PR{}{}'.format(channal,symbol,steps)
        rep = self.controller.command(command)

    def isFree(self,channal):
        command = '{}SD?'.format(channal)
        rep= self.controller.command(command)
        return bool(rep[2])

class scaner(NewportPic):
    # NewportPic


    def scan(self,steps,N,M,interval_ms=2000):
        xTarget, yTarget = Tool.relatedDirection(N, M, steps)
        print(xTarget, yTarget)
        self.time_start=time.time()
        print(self.time_start)
        self.time_point=[self.time_start+x*interval_ms/1000 for x in range(N*M)]
        print(len(self.time_point))
        print(self.time_point)
        time_index=0
        for pixel_index in range(N*M):
           self.wait_for_next(pixel_index,precision_ms=interval_ms/20) #5%
           print(pixel_index)
           if xTarget[pixel_index]!=xTarget[pixel_index-1] or pixel_index ==0:
                self.wait_for_free(1)
                self.go_to_Target(1, xTarget[pixel_index])
           if yTarget[pixel_index] != yTarget[pixel_index - 1]or pixel_index==0:
                time.sleep(0.05)
                self.wait_for_free(2)
                self.go_to_Target(2, yTarget[pixel_index])
           time.sleep(0.05)
           self.wait_for_free(1)
           print(self.get_Position(1))
           self.wait_for_free(2)
           print(self.get_Position(2))


           print(time.time()-self.time_start)

        self.go_to_Target(1,0)
        self.wait_for_free(1)
        time.sleep(1)
        self.go_to_Target(2,0)
        time.sleep(1)
        self.wait_for_free(2)

        print(self.get_Position(1))
        print(self.get_Position(2))



    def wait_for_next(self,index,precision_ms):
        time_Now=time.time()
        while time_Now < self.time_point[index]:
            time.sleep(precision_ms/1000)
            time_Now=time.time()

    def wait_for_free(self,channal,precision_ms=1000):
        while self.isFree(channal) != True:
            time.sleep(precision_ms/1000)





if __name__ == '__main__':
    # s=scaner()
    # s.scan(100,3,3)
    b=scaner()
    # rep = a.controller.command('1PR-10')
    # time.sleep(1)
    # rep = a.controller.command('1PR10')
    # if rep:
    #     print("Output: {}".format(rep))
    #
    # time.sleep(1)
    # print(a.get_Position(1))
    # time.sleep(1)
    # a.go_to_Target(1,-100)
    # time.sleep(1)
    # print(a.get_Position(1))
    # time.sleep(1)
    # a.move_steps(1,-90)
    # time.sleep(1)
    # print(a.get_Position(1))
    # time.sleep(1)
    # a.go_to_Target(1,0)
    # time.sleep(1)
    # print(a.get_Position(1))

    b.scan(20,5,5)