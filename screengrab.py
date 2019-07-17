from PIL import ImageGrab
import time

count = 0
while True:
    count += 1
    pic = ImageGrab.grab()
    name = time.strftime("%Y-%m-%d---%H:%M:%S", time.localtime()).replace(':', '-')
    pic.save(r'D:\\lidar\\beam_test\\%s.jpg' % name)
    print(count)
    time.sleep(2*60)