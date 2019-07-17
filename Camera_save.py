import time
#import Camera_image_save
import subprocess
import shlex

if __name__ == '__main__':
    while True:
        shell_cmd = "python D:\\lidar\\program\\Telescope\\Camera_image_save.py"
        #cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(shell_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:

            line = p.stdout.readline()[:-1]
            line = str(line, 'utf8')
            if line != '\n':
                print(line)
        p.kill()
        time.sleep(5*60)
