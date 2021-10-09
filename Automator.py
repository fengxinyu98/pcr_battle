import uiautomator2 as u2
import time
from cv import *


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
                    print("find!")
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
        self.dWidth, self.dHeight = self.d.window_size()
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        num_of_white = len(np.argwhere(binary == 255))
        active_path = self.get_butt_stat(screen, [
                                         'pcr_battle/liwu.jpg'])

        if 'pcr_battle/liwu.jpg' in active_path:
            return 'liwu'
        '''
        if 'imgs/jjc.png' in active_path:
            return 'jjc'

        if 'imgs/gengxin.png' in active_path:
            return 'gengxin'

        if 'imgs/zhandoukaishi.jpg' in active_path:
            return 'zhandoukaishi'

        if num_of_white < 50000:
            return 'dark'
        else:
            '''
        return 0