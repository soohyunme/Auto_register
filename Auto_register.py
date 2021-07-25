import ctypes
import subprocess
import os, sys, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

console_hwnd = ctypes.windll.kernel32.GetConsoleWindow ()
ctypes.windll.user32.ShowWindow (console_hwnd, subprocess.SW_HIDE)

os_path = os.getcwd()
file_name = 'userDate'
user_id = ''
user_pw = ''
url = ''
today = '07.21'
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')
try :
    with open(file_name,'r',encoding='utf-8') as f:
        info = f.read()
        user_id = re.findall(r'{.*}', info)[0].replace('{','').replace('}','')
        user_pw = re.findall(r'{.*}', info)[1].replace('{','').replace('}','')
        class_ = re.findall(r'{.*}', info)[2].replace('{','').replace('}','')
        if class_.lower() == 'a':
            url = 'http://gbiga.onilifo.co.kr/'
        elif class_.lower() == 'b':
            url = 'http://gbigb.onilifo.co.kr/'
        else:
            pass
except:
    with open(file_name,'w',encoding='utf-8') as f:
        f.write('Id : {}\n')
        f.write('Password : {}\n')
        f.write('class(월화:a, 수목:b) : {}')
    ctypes.windll.user32.MessageBoxW(None, f'{os_path}\\{file_name} 생성\n\n로그인 정보를 갱신해주세요.',"로그인 정보 생성", 0)
    sys.exit()

if url == '' or user_id == '' or user_pw == '':
    ctypes.windll.user32.MessageBoxW(None, f'{os_path}\\{file_name}\n\n로그인 정보를 갱신해주세요.',"로그인 정보 오류", 0)
    sys.exit()

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized");
if getattr(sys, 'frozen',False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    browser = webdriver.Chrome(chromedriver_path, options=options)
else:
    browser = webdriver.Chrome(options=options)
browser.get(url)
browser.implicitly_wait(5)

browser.find_element_by_xpath('//*[@id="btn-login"]').click()
browser.implicitly_wait(5)
browser.find_element_by_xpath('//*[@id="username"]').send_keys(user_id)
browser.find_element_by_xpath('//*[@id="password"]').send_keys(user_pw)
browser.find_element_by_xpath('//*[@id="btn-login"]').click()
browser.implicitly_wait(5)

if browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[6]/ul/li/a').text == '로그인':
    ctypes.windll.user32.MessageBoxW(None, '아이디와 비밀번호를 확인해주세요.',"로그인 오류", 0)
    sys.exit()

def register_today_study():
    path = '//ul/li/div/div/div[2]'
    btn_path = path+'/button'
    contents =browser.find_elements_by_xpath(path)
    btns = browser.find_elements_by_xpath(btn_path)
    page_tag = browser.find_element_by_xpath('//div/div[4]/ul').text
    for i in contents:
        if today in i.text:
            btns[contents.index(i)].click()
            try: 
                WebDriverWait(browser, 5).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
                alert= browser.switch_to.alert
                alert.accept()
            except:
                pass
            break

        elif i == contents[-1]:
            if page_tag == '다음':
                browser.find_element_by_xpath('//*[@id="btn-next"]').click()
            else:
                ctypes.windll.user32.MessageBoxW(None, f'{month}월 {day}일에 해당하는 강의가 없습니다.',"강의 검색 오류", 0)
                sys.exit()
                return
            register_today_study()
            break
    return

browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[1]/a').click()
browser.implicitly_wait(5)
register_today_study()

browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[4]/a').click()
browser.implicitly_wait(5)
register_today_study()

