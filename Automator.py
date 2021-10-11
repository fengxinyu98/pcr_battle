from cv2 import TermCriteria_COUNT
import uiautomator2 as u2
import time
from cv import *
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
            screen_shot = self.d.screenshot(format="opencv")

            if self.get_screen_state(screen_shot) == 'liwu':
                time.sleep(2)
                screen_shot = self.d.screenshot(format="opencv")
                if self.get_screen_state(screen_shot) == 'liwu':
                    break
            self.d.click(0.01*self.dWidth,  0.01*self.dHeight)

            time.sleep(1)

    def get_butt_stat(self, screen_shot, template_paths, threshold=0.84):
        #此函数输入要判断的图片path,屏幕截图, 阈值,   返回大于阈值的path,坐标字典,
        self.dWidth, self.dHeight = self.d.window_size()
        return_dic = {}
        zhongxings, max_vals = UIMatcher.findpic(
            screen_shot, template_paths=template_paths)
        for i, name in enumerate(template_paths):
            print(name + '--' + str(round(max_vals[i], 3)), end=' ')
            if max_vals[i] > threshold:
                return_dic[name] = (
                    zhongxings[i][0] * self.dWidth, zhongxings[i][1] * self.dHeight)
        print('')

        return return_dic

    def get_screen_state(self, screen):
        active_path = self.get_butt_stat(screen, [
                                         'imgs/liwu.JPG', 'imgs/jjc.JPG', 'imgs/gengxin.JPG', 'imgs/zhandoukaishi.JPG', 'imgs/caidan.jpg', 'imgs/xiayibu.jpg', 'imgs/xiayibu2.jpg'])

        if 'imgs/liwu.JPG' in active_path:
            return 'liwu'

        if 'imgs/jjc.JPG' in active_path:
            return 'jjc'

        if 'imgs/gengxin.JPG' in active_path:
            return 'gengxin'

        if 'imgs/zhandoukaishi.JPG' in active_path:
            return 'zhandoukaishi'

        if 'imgs/caidan.jpg' in active_path:
            return 'caidan'

        if 'imgs/xiayibu.jpg' in active_path or 'imgs/xiayibu2.jpg' in active_path:
            return 'xiayibu'
        else:
            return 0

    def go_jjc(self):
        while True:
            self.d.click(636, 680)
            time.sleep(1)
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'jjc':
                break
        while True:
            self.d.click(779, 549)
            # self.d.click(1100,549)
            time.sleep(1)
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'gengxin':
                break

    def go_pjjc(self):
        while True:
            self.d.click(636, 680)
            time.sleep(1)
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'jjc':
                break
        while True:
            # self.d.click(779,549)
            self.d.click(1100, 549)
            time.sleep(1)
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'gengxin':
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
            time.sleep(2)
        count = 0
        while True:
            screen_shot = self.d.screenshot(format="opencv")
            rank = screen_shot[158:186, 1015:1080]
            rank = ocr(rank)
            if rank < min_rank + 5 or count == 10:
                while True:
                    self.d.click(900, 200)
                    time.sleep(2)
                    screen_shot = self.d.screenshot(format="opencv")
                    if self.get_screen_state(screen_shot) == 'zhandoukaishi':
                        break
                break
            count += 1
            self.d.click(1155, 125)
            time.sleep(2)

    def battle(self):
        while True:
            self.d.click(1119, 605)
            time.sleep(2)
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'caidan':
                break
        while True:
            screen_shot = self.d.screenshot(format="opencv")
            if self.get_screen_state(screen_shot) == 'xiayibu':
                while True:
                    self.d.click(1108, 653)
                    time.sleep(2)
                    screen_shot = self.d.screenshot(format="opencv")
                    if self.get_screen_state(screen_shot) == 'gengxin':
                        break
                break

    def test(self):
        screen_shot = cv_imread('imgs//Screenshot.jpg')
        template = cv_imread('imgs//xiayibu.jpg')
        zhongxings = []
        max_vals = []
        h, w = template.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(screen_shot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        x = (max_loc[0]+w//2)
        y = (max_loc[1] + h // 2)
        zhongxings.append([x, y])
        max_vals.append(max_val)
        print(zhongxings)
        print(max_vals)
