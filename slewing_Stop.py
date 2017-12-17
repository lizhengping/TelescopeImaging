from telescope import *


# import time

class camera:
    def __init__(self, com='COM2'):
        self.tele1 = Tele(com)
        self.state_deg = self.tele1.get_Direction_Precise()
        self.state_urad = self.tele1.get_Direction_Precise_uRad()

    def scan_Line(self, direction, step_urad, num, photoTime):
        state = self.tele1.get_Direction_Precise_uRad()
        if direction == 1:
            for i in range(num):
                print(self.tele1.A_move_urad(state[0] + step_urad * (i)))
                self.tele1.slewing_Stop()
                print(i, ' done')
                time.sleep(photoTime)

        if direction == -1:
            for i in range(num):
                print(self.tele1.A_move_urad(state[0] - step_urad * (i)))
                self.tele1.slewing_Stop()
                print(i, ' done')
                time.sleep(photoTime)
        if (direction != 1) & (direction != -1):
            print('Error in direction')

    def scan_Row(self, direction, step_urad, num, photoTime):
        state = self.tele1.get_Direction_Precise_uRad()
        if direction == 1:
            for i in range(num):
                print(self.tele1.E_move_urad(state[1] + step_urad * (i)))
                self.tele1.slewing_Stop()
                print(i, ' done')
                time.sleep(photoTime)

        if direction == -1:
            for i in range(num):
                print(self.tele1.E_move_urad(state[1] - step_urad * (i)))
                self.tele1.slewing_Stop()
                print(i, ' done')
                time.sleep(photoTime)
        if (direction != 1) & (direction != -1):
            print('Error in direction')

    def takePhoto(self, xNum, yNum, step, phototime):
        if yNum > 0:
            for i in range(yNum):
                if (i % 2) == 0:
                    cam1.scan_Line(1, step, xNum, phototime)
                    if i != yNum:
                        cam1.scan_Row(1, step, yNum, phototime)
                if (i % 2) == 1:
                    cam1.scan_Line(-1, step, xNum, phototime)
                    if i != yNum:
                        cam1.scan_Row(1, step, yNum, phototime)


if __name__ == '__main__':
    cam1 = camera('COM7')
    cam1.tele1.slewing_Stop()
