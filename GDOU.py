#!/user/bin/env pyhton解释器路径
# -*-coding:utf-8-*- 脚本编码
import cryptocode
import msvcrt
import os
import requests
import time
import pywifi
from pywifi import const
from configparser import ConfigParser
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.live import Live
from rich.text import Text

file100 = 'config.ini'
version_info = '1.5'

# 范围时间
d_time = datetime.strptime(str(datetime.now().date())+'6:30', '%Y-%m-%d%H:%M')
d_time1 =  datetime.strptime(str(datetime.now().date())+'23:30', '%Y-%m-%d%H:%M')

def run(playwright: Playwright) -> None:
    try:
        global context
        browser = playwright.chromium.launch(headless=mode, channel=local)
        context = browser.new_context()
        page = context.new_page()
        printer('url: ' + testurl)
        page.goto(testurl)
        printer('account: ' + account)
        page.locator("[placeholder=\"请输入账号\"]").fill(account)  # .type(account)
        printer('password: ' + len(password) * '*')
        page.locator("[placeholder=\"请输入密码\"]").fill(password)
        page.locator("xpath=//*[@id='protocol']").click()
        printer('submit')
        page.locator("text=登录").click()
        browser.close()
        if network_check():
            printer('success')
        else:
            printer('fail')

    except:
        printer('fail')

    # 下线功能
    ''' printer('enter to log out')
        if len(input()) != 0:
            page.click('xpath=//*[@id="logout"]')
            page.click('text=确认')
            printer('exiting program...')
            time.sleep(5)
            #browser.close()
            #sys.exit()'''

def file1():  # 文件读写
    global account, password, testurl, mode, local, connect, check
    console = Console()
    if os.path.exists(file100):  # 文件存在检测
        # printer('file existed')
        cf = ConfigParser()
        cf.read(file100)
        version = cf.get('parm', 'ver')
        if version < version_info:
            os.remove(file100)
            with console.screen(style="bold white on red") as screen:
                text = Align.center("[blink]配置文件\n版本过低\n自动删除[/blink]", vertical="middle")
                screen.update(Panel(text))
                time.sleep(5)
            file1()
        # main
        account = cf.get('main', 'uid')
        password = cf.get('main', 'pwd')
        # parm
        local = cf.get('parm', 'local')
        mode = cf.get('parm', 'mode')
        check = cf.get('parm', 'check')
        connect = cf.get('parm', 'connect')
        testurl = cf.get('parm', 'url')

        # return account, password, testurl, mode, local, connect, check
    else:
        printer('config file not fund')
        os.system('mode con cols=48 lines=23')
        printer('密码会自动加密')
        printer('输入后请按回车')
        printer('input account')
        account = input()

        printer('input password')
        password = pwd_input()
        print(' ')

        printer('运行模式选择')
        printer('headless(1)|browser(2)')
        mode = input()

        printer('浏览器选择')
        printer('edge(1)|chrome(2)')
        local = input()

        printer('使用网线(0)|GDOU.NET(1)')
        connect = input()

        printer('网络检查间隔（秒）')
        check = int(input())

        testurl = 'http://1.1.1.1/'
        t0 = '\n'
        password = cryptocode.encrypt(password, 'louis16s')  # 加密

        with open(file100, "w") as file:
            file.write(
                '[main]' + t0 +
                'uid = ' + str(account) + t0 +
                'pwd = ' + str(password) + t0 +
                '[parm]' + t0 +
                'local = ' + str(local) + t0 +
                'mode = ' + str(mode) + t0 +
                'check = ' + str(check) + t0 +
                'connect = ' + str(connect) + t0 +
                'url = ' + str(testurl) + t0 +
                'ver = ' + version_info + t0)
            file.close()
        for step in track(range(100), description="Writing..."):
            time.sleep(0.01)
        printer('config is generated')

    password = cryptocode.decrypt(password, 'louis16s')  # 解密
    # 浏览器
    if local == '0':
        local = None  # Chromium
    if local == '1':
        local = 'msedge'
    if local == '2':
        local = 'chrome'

    if mode == '1':
        mode = True  # 无头模式
    else:
        mode = False

    return account, password, testurl, mode, local, connect, check

def connect_wifi(ssid):
    if ssid == '1':
        ssid0 = "GDOU.NET"
    if ssid == '2':
        ssid0 = "海大校园网"
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()
    time.sleep(3)
    profile = pywifi.Profile()  # 配置文件
    profile.ssid = ssid0  # wifi名称
    ifaces.remove_all_network_profiles()  # 删除其它配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)
    time.sleep(3)
    isok = True

    if ifaces.status() == const.IFACE_CONNECTED:
        print("connect successfully!")
    else:
        print("connect failed!")
        print('turn on ur wifi')
        time.sleep(5)
        connect_wifi(ssid)

    time.sleep(1)
    return isok

def network_check():
    try:
        session = requests.Session()
        html = session.get("https://www.baidu.com", timeout=2)
    except:
        return False
    return True

def os_checker():
    temp = file1()
    if temp[5] != "0":
        connect_wifi(temp[5])
    #os_version = platform.platform()
    if os.path.exists(file100):
        os.system('mode con cols=45 lines=8')
        printer('version ' + version_info)
        printer('script started')

def pwd_input():  # 密码
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n':  # 如果是换行，则输入结束
            break
        elif newChar == '\b':  # 如果是退格，则删除密码末尾一位并且删除一个星号
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格
                msvcrt.putch(' '.encode(encoding='utf-8'))  # 输出一个空格覆盖原来的星号
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8'))  # 显示为星号
    return (''.join(chars))

def printer(content):  # 彩色输出
    console = Console()
    time1 = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    console.print(time1, end='')
    console.print(content, style="yellow")

def info():
    try:
        url = ("http://10.129.1.1/cgi-bin/rad_user_info?"
               "callback=jQuery112406118340540763985_1556004912581&_=1556004912582")  # 指定网址
        response = requests.get(url=url)  # 发起请求#get会返回一个响应对象
        detail = response.text.split(',')

        ip = str(detail[12].split(':')[1]).replace('"', " ")
        printer("ip:" + ip)
        sum = str(int(int(detail[20].split(':')[1])*0.000000001))
        printer("已用流量："+sum+"GB")
        device = str(detail[11].split(':')[1]).replace('"'," ")
        printer("在线设备:" + device)
    except:
        printer("获取信息失败")

def time_update():
    time1 = str(datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]'))
    text = Text(time1+"脚本正常运行中(无提示)")  # create renderable text object
    live.update(text)  # update display with text object

if __name__ == '__main__':
    temp = file1()
    os_checker()
    i = 1
    n = 1
    with Live(refresh_per_second=1) as live:  # refresh once per second
        while True:
            # 当前时间
            n_time = datetime.now()
            if n_time > d_time and n_time < d_time1:
                if network_check():#网络正常
                    if i == 1:
                        printer('认证通过，网络正常')
                        info()
                        i = 0
                    #time_update()

                else:#网络异常或未连接
                    with sync_playwright() as playwright:
                        run(playwright)

                time.sleep(int(temp[6]))
                n = 1
            else:
                if n == 1:
                    printer('time2rest')
                    n = 0
                time.sleep(int(temp[6]))
                exit(0)