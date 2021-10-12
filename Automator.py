import re
from cv2 import TermCriteria_COUNT
import uiautomator2 as u2
import time
import cv2
import numpy as np
from ocr import ocr


class Automator:
    def __init__(self, auto_task=False, auto_policy=True,
                 auto_goods=False, speedup=True):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect()
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断jgm进程是否在前台, 最多等待20秒，否则唤醒到前台
            if self.d.app_wait("com.bilibili.priconne", front=True, timeout=1):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    time.sleep(1)
                self.appRunning = True
                break
            else:
                self.app = self.d.session("com.bilibili.priconne")
                self.appRunning = False
                continue

        while True:
            if self.get_screen_state('imgs/liwu.jpg'):
                time.sleep(2)
                if self.get_screen_state('imgs/liwu.jpg'):
                    break
            self.d.click(0.01*self.dWidth,  0.01*self.dHeight)
            time.sleep(1)

    def get_screen_state(self, template_path, threshold=0.84):
        screen_shot = self.d.screenshot(format="opencv")
        template = cv2.imdecode(np.fromfile(template_path, dtype=np.uint8), -1)
        h, w = template.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(screen_shot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > threshold:
            return True
        else:
            return False

    def go_jjc(self):
        while True:
            self.d.click(636, 680)
            time.sleep(3)
            if self.get_screen_state('imgs/jjc.jpg'):
                break
        while True:
            self.d.click(779, 549)
            time.sleep(3)
            if self.get_screen_state('imgs/gengxin.jpg'):
                break

    def go_pjjc(self):
        while True:
            self.d.click(636, 680)
            time.sleep(3)
            if self.get_screen_state('imgs/jjc.jpg'):
                break
        while True:
            self.d.click(1100, 549)
            time.sleep(3)
            if self.get_screen_state('imgs/gengxin.jpg'):
                break

    def go_dxc(self):
        while True:
            self.d.click(636, 680)
            time.sleep(3)
            if self.get_screen_state('imgs/jjc.jpg'):
                break
        while True:
            self.d.click(1170, 181)
            time.sleep(3)
            if self.get_screen_state('imgs/chetui.jpg'):
                break

    def battle_ready(self):
        count = 0
        min_rank = 999
        while True:
            screen_shot = self.d.screenshot(format="opencv")
            rank = screen_shot[158:186, 1015:1080]
            rank = ocr(rank)
            if rank < min_rank:
                min_rank = rank
            count += 1
            if count == 10:
                break
            self.d.click(1155, 125)
            time.sleep(3)
        count = 0
        while True:
            screen_shot = self.d.screenshot(format="opencv")
            rank = screen_shot[158:186, 1015:1080]
            rank = ocr(rank)
            if rank < min_rank + 5 or count == 10:
                while True:
                    self.d.click(900, 200)
                    time.sleep(3)
                    if self.get_screen_state('imgs/zhandoukaishi.jpg') or self.get_screen_state('imgs/duiwu2.jpg') or self.get_screen_state('imgs/duiwu3.jpg'):
                        break
                break
            count += 1
            self.d.click(1155, 125)
            time.sleep(3)

    def battle(self):
        while True:
            self.d.click(1119, 605)
            time.sleep(3)
            if self.get_screen_state('imgs/caidan.jpg'):
                break
        while True:
            if self.get_screen_state('imgs/xiayibu.jpg') or self.get_screen_state('imgs/xiayibu2.jpg'):
                while True:
                    self.d.click(1108, 653)
                    time.sleep(3)
                    if self.get_screen_state('imgs/gengxin.jpg'):
                        break
                break

    def dxc(self):
        while True:
            self.d.click(640, 360)
            time.sleep(2)
            if self.get_screen_state('imgs/tiaozhan.jpg'):
                self.d.click(1118, 607)
                break
        while True:
            self.d.click(1151, 120)
            time.sleep(2)
            self.d.click(1053, 233)
            time.sleep(2)
            self.d.click(1119, 605)
            time.sleep(20)
            if self.get_screen_state('imgs/xiayibu.jpg') or self.get_screen_state('imgs/xiayibu2.jpg'):
                while True:
                    self.d.click(1108, 653)
                    time.sleep(3)
                    if self.get_screen_state('imgs/chetui.jpg'):
                        break
                break
        while True:
            self.d.click(847, 387)
            time.sleep(2)
            if self.get_screen_state('imgs/tiaozhan.jpg'):
                self.d.click(1118, 607)
                break
        while True:
            self.d.click(1119, 605)
            time.sleep(20)
            if self.get_screen_state('imgs/xiayibu.jpg') or self.get_screen_state('imgs/xiayibu2.jpg'):
                while True:
                    self.d.click(1108, 653)
                    time.sleep(3)
                    if self.get_screen_state('imgs/chetui.jpg'):
                        break
                break
        while True:
            self.d.click(640, 360)
            time.sleep(2)
            if self.get_screen_state('imgs/tiaozhan.jpg'):
                self.d.click(1118, 607)
                break
        while True:
            self.d.click(1119, 605)
            time.sleep(20)
            if self.get_screen_state('imgs/xiayibu.jpg') or self.get_screen_state('imgs/xiayibu2.jpg'):
                while True:
                    self.d.click(1108, 653)
                    time.sleep(3)
                    if self.get_screen_state('imgs/chetui.jpg'):
                        break
                break
        while True:
            self.d.click(640, 360)
            time.sleep(2)
            if self.get_screen_state('imgs/tiaozhan.jpg'):
                self.d.click(1118, 607)
                break
        while True:
            self.d.click(1119, 605)
            time.sleep(20)
            if self.get_screen_state('imgs/xiayibu.jpg') or self.get_screen_state('imgs/xiayibu2.jpg'):
                while True:
                    self.d.click(1108, 653)
                    time.sleep(3)
                    if self.get_screen_state('imgs/chetui.jpg'):
                        break
                break
        flag = True
        while flag:
            while True:
                self.d.click(640, 360)
                time.sleep(2)
                if self.get_screen_state('imgs/tiaozhan.jpg'):
                    self.d.click(1118, 607)
                    break
            while True:
                self.d.click(1119, 605)
                time.sleep(60)
                if self.get_screen_state('imgs/dxc.jpg'):
                    while True:
                        self.d.click(1078, 658)
                        time.sleep(3)
                        if self.get_screen_state('imgs/chetui.jpg'):
                            break
                    break
                if self.get_screen_state('imgs/xiayibu.jpg'):
                    flag = False
                    while True:
                        self.d.click(1108, 653)
                        time.sleep(3)
                        if self.get_screen_state('imgs/EX2.jpg'):
                            break
                    break
        self.d.click(1108, 446)
        time.sleep(2)
        self.d.click(784, 495)
        time.sleep(5)
