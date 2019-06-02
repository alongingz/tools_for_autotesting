"""自动化测试常用方法"""

"""移动端APP前置代码，格式固定，可修改platformName，platformVersion，deviceName，appPackage，appActivity"""

# 导模块
from appium import webdriver

# 创建⼀个字典，包装相应的启动参数
desired_caps = dict()
# 需要连接的⼿机的平台(不限制⼤⼩写)
desired_caps['platformName'] = 'Android'
# 需要连接的⼿机的版本号(⽐如 5.2.1 的版本可以填写 5.2.1 或 5.2 或 5 ，以此类推)
desired_caps['platformVersion'] = '5.1'
# 需要连接的⼿机的设备号(andoird平台下，可以随便写，但是不能不写；ios下必须写例如：iPhone 8)
desired_caps['deviceName'] = '192.168.56.101:5555'
# 需要启动的程序的包名
desired_caps['appPackage'] = 'com.android.settings'
# 需要启动的程序的界⾯名
desired_caps['appActivity'] = '.Settings'
# 解决中文问题
desired_caps['unicodeKeyboard'] = True
desired_caps["resetKeyboard"] = True
# 连接appium服务器
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 执行操作。。。。。。
# 关闭
driver.quit()

"""pytest运行配置代码"""
# 配置代码，.ini文件
[pytest]
addopts = -s - -html = report / report.html
testpaths =./ scripts
python_files = test_ *.py
python_classes = Test *
python_functions = test_ *

"""找到元素并点击"""


# 找到元素（element）并点击
def find_element_and_clike(option):
    while True:
        try:
            driver.find_element_by_xpath("//*[@text='{}']".format(option)).click()
            driver.quit()
            break
        except Exception as e:
            page = driver.page_source
            swipe_screen()
            # 到底了，未找到，关闭
            if driver.page_source == page:
                print("Couldent find \"{}\" on the whole page, please check if the option you passed in exists.".format(
                    option))
                break

"""APP yaml格式数据文件"""

# "test_case_function_name":
#   "test_case_01":
#     "username": "张三"
#     "pwd": 123
#   "test_case_02":
#     "username": "lisi"
#     "pwd": 123456



"""移动端APP yaml格式数据读取"""
import yaml


def read_data(case_name):
    with open("../data/data.yaml", "r", encoding="utf-8") as f:
        data_dict = yaml.load(f)[case_name]
        data_list = list()
        data_list.extend(data_dict.values())
        print(data_list)



"""allure报告中截图方法"""
import allure


def get_allure_screenshot():
    allure.attach("截图", self.driver.get_screenshot_as_png(), allure.attach_type.PNG)



"""移动端APP函数，依赖于driver"""


# 屏幕滑动
def swipe_screen(direction="up"):
    """
    获取屏幕分辨率，并滑动
    :param direction:
        "up":向上滑动
        "down":向下滑动
        "left":向左滑动
        "right":向右滑动
    :return:
    """
    screen_width = driver.get_window_size()["width"]
    screen_height = driver.get_window_size()["height"]
    width_center = screen_width * 0.5
    height_center = screen_height * 0.5
    top_y = screen_height * 0.25
    end_y = screen_height * 0.75
    left_x = screen_width * 0.25
    right_x = screen_width * 0.75
    if direction == "up":
        driver.swipe(width_center, end_y, width_center, top_y)
    elif direction == "down":
        driver.swipe(width_center, top_y, width_center, end_y)
    elif direction == "left":
        driver.swipe(right_x, height_center, left_x, height_center)
    elif direction == "right":
        driver.swipe(left_x, height_center, right_x, height_center)
    else:
        raise Exception("The direction argument you send must be in the range of up/down/left/right.")


"""web 封装driver"""
# 封装浏览器对象，单例
from selenium import webdriver
# page是页面对象模块，__init__方法内含有需要定位的元素、URL
import page


class GetDriver:
    driver = None

    @classmethod
    def get_driver(cls):
        if not cls.driver:
            cls.driver = webdriver.Firefox()
            cls.driver.maximize_window()
            cls.driver.get(page.url)
        return cls.driver

    @classmethod
    def quit_driver(cls):
        if cls.driver:
            cls.driver.quit()
            cls.driver = None


"""web 生成日志方法"""
# 生动态成日志，单例
import logging.handlers

import time


class GetLog:
    logger = None

    @classmethod
    def creat_log(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger()
            cls.logger.setLevel(logging.INFO)

            fm = "%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s"
            fmt = logging.Formatter(fm)

            cl = logging.handlers.TimedRotatingFileHandler("../log/{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S")),
                                                           when="MIDNIGHT",
                                                           interval=1,
                                                           backupCount=31,
                                                           encoding="utf8")
            cl.setLevel(logging.INFO)
            cl.setFormatter(fmt)

            cls.logger.addHandler(cl)
        return cls.logger


"""生成报告"""
# 动态生成HTML测试报告，单例
import unittest

import time

from tools.HTMLTestRunner import HTMLTestRunner


class GetReport:
    report = None

    @classmethod
    def creat_report(cls):
        if cls.report is None:
            suite = unittest.defaultTestLoader.discover("../scripts/")
            filepath = "../report/{}.html".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
            with open(filepath, "wb") as f:
                cls.report = HTMLTestRunner(stream=f, title="tpshop登录界面测试报告")
                cls.report.run(suite)


"""json数据读取"""
import json


def read_json(filename):
    filepath = "../datas/{}".format(filename)
    with open(filepath, "r", encoding="utf-8") as f:
        arr = list()
        for data in json.load(f).values():
            arr.append([data.get("name"),
                        data.get("pwd"),
                        data.get("code"),
                        data.get("except")])
        return arr


"""text数据读取"""


def read_text():
    filepath = "../datas/{}".format("login.text")
    with open(filepath, "r", encoding="utf-8") as f:
        arr = list()
        for data in f.readlines():
            arr.append(data.strip().split(","))
        return arr[1:]
