import TeleMotion
import MotionJog
import time
import threading

if __name__ == '__main__':

    tele1 = TeleMotion.Tele('COM4', 'COM3')
    print(tele1.A.Slewing_Steps(level=1))
    time.sleep(2)
    print(tele1.A.Slewing_Steps_revers(level=1))
    time.sleep(1)
    MotionJog.show(Axis1=tele1.A,Axis2=tele1.E,Independ=False)
    while True:
        pass