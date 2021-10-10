import os
import time
import cv2
from Automator import *

if __name__ == '__main__':
    os.system('adb connect 127.0.0.1:5554')
    a = Automator()
    a.start()
    a.go_jjc()
    a.battle()
