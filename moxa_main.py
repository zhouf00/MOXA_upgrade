import os
import subprocess
import time
from selenium import webdriver

def moxa_info(ip):
    """
    初始化浏览器，并进行登陆操作
    :param ip:
    :return:
    """
    # 获取谷歌插件的位置
    chr_path = os.path.join(os.getcwd(),"chromedriver")
    # executable_path用来指定插件的位置
    driver = webdriver.Chrome(executable_path=chr_path)
    driver.get(ip)

    driver.find_element_by_id("Username").clear()
    driver.find_element_by_id("Username").send_keys("admin")
    driver.find_element_by_id("Password").clear()
    driver.find_element_by_id("Password").send_keys("moxa")
    driver.find_element_by_name("Submit").click()
    return driver

def moxa_up(web, file_path):
    """
    进行文件上传和升级的操作
    :param web:
    :param file_path:
    :return:
    """
    try:
        # 展开左侧网页
        web.switch_to.frame(1)
        web.find_element_by_id("folder59").click()
        web.find_element_by_id("item62").click()

        # 进入右侧网页并上传文件
        web.switch_to.parent_frame()
        web.switch_to.frame(2)
        web.find_element_by_name("filename").send_keys(file_path)
        web.find_element_by_name("Submit").click()
    except Exception as e:
        return "刷机失败，检查文件是否正确\n"
    else:
        web.quit()

def moxa_check(web):
    """
    进行升级后参数的检查工作
    :param web:
    :return: 参数存在时返回参数的值，否则报错提示
    """
    try:
        web.switch_to.parent_frame()
        web.switch_to.frame(1)
        web.find_element_by_id("folder7").click()
        web.find_element_by_xpath("//*[@id='folder10']/tbody/tr/td[1]/a[1]/img").click()
        web.find_element_by_id("item13").click()

        web.switch_to.parent_frame()
        web.switch_to.frame(2)
        web.find_element_by_xpath("//*[@id='turboRoaming_enable']").click()
        table = web.find_element_by_xpath("//*[@id='iw_turboRoaming_channels']")
        t_rows = table.find_elements_by_tag_name("tr")
    except Exception as e:
        return "指定位置无参数\n"
    else:
        web.quit()
        return len(t_rows)

def check_ip_ping(ip):
    """
    进行ping交换机IP的操作，并对网络是否畅通返回值
    :param ip:
    :return: 0：网络不通  1：网络畅通
    """
    cmd = "ping -n 1 " + ip
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines = response.stdout.readlines()
    res = lines[2].decode("gbk")
    if res.strip() == "请求超时。":
        return 0
    else:
        res = res.split(":")[1].strip()
        if res == "无法访问目标主机。":
            return 0
        else:
            return 1

def time_now():
    """
    :return:返回固定时间格式 如：<20:35:29>
    """
    return time.strftime('<%H:%M:%S>', time.localtime())


if __name__ == '__main__':
    file = "D:\临时\moxa升级\附件三AWK1137C_1.2.4_Build_18053019.rom"
"""
    web = moxa_info()
    moxa_up(web, file)
    t = check_ip_ping()
    if t:
        web = moxa_info()
        moxa_check(web)
    else:
        print("超时未启动")
        exit()
"""
