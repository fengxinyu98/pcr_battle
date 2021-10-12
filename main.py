import os
import time
import cv2
from Automator import *

if __name__ == '__main__':
    os.system('start C:\leidian\LDPlayer4\dnplayer.exe')
    time.sleep(30)
    os.system('adb connect 127.0.0.1:5554')
    a = Automator()
    a.start()
    jjc_times, pjjc_times = 0, 5
    a.go_jjc()
    for i in range(jjc_times):
        a.battle_ready()
        a.battle()
        if i == jjc_times - 1:
            time.sleep(5)
        else:
            time.sleep(270)
    a.go_pjjc()
    for i in range(pjjc_times):
        a.battle_ready()
        a.battle()
        if i == pjjc_times - 1:
            time.sleep(5)
        else:
            time.sleep(270)
    a.go_dxc()
    a.dxc()
