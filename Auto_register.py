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
file_name = 'userData'
user_id = ''
user_pw = ''
url = ''
register_flag = False
class_counter = 0
today = datetime.now().strftime('%m.%d')
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')

def login(id,pw):
    click_xpath('//*[@id="btn-login"]')
    browser.find_element_by_xpath('//*[@id="username"]').send_keys(id)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(pw)
    click_xpath('//*[@id="btn-login"]')
    
    if browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[6]/ul/li/a').text == '로그인':
        ctypes.windll.user32.MessageBoxW(None, '아이디와 비밀번호를 확인해주세요.',"로그인 오류", 0)
        sys.exit()
    
def register_today_study():
    global register_flag, class_counter
    path = '//ul/li/div/div/div[2]'
    contents = browser.find_elements_by_xpath(path)
    btns = browser.find_elements_by_xpath(path+'/button')
    page_tag = browser.find_element_by_css_selector('div > div.buttonMultiContainer').text
    for i in contents:
        if today in i.text:
            btns[contents.index(i)].click()
            class_counter +=1
            register_flag = True
            try: 
                WebDriverWait(browser, 5).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
                alert= browser.switch_to.alert
                alert.accept()
            except:
                pass
        if i == contents[-1]:
            if '다음' in page_tag:
                click_xpath('//*[@id="btn-next"]')
                register_today_study()
            elif(register_flag==False):
                ctypes.windll.user32.MessageBoxW(None, f'{month}월 {day}일에 해당하는 강의가 없습니다.',"강의 검색 오류", 0)
                sys.exit()
                return
            break
    return

def enter_class():
    path = '//ul/li/div/div/div[2]'
    contents =browser.find_elements_by_xpath(path)
    btns = browser.find_elements_by_xpath(path+'/button')
    page_tag = browser.find_element_by_css_selector('div > div.buttonMultiContainer').text
    for i in contents:
        if today in i.text:
            browser.execute_script("arguments[0].style.backgroundColor = 'yellow'; return arguments[0];", i)
            webdriver.ActionChains(browser).drag_and_drop_by_offset(i,0,0).perform()
            if class_counter == 1:
                btns[contents.index(i)].click()
                return
            elif (enter_disable == False) and (class_counter>=2):
                mbox_flag = ctypes.windll.user32.MessageBoxW(None, '해당 강의가 맞나요?',"강의 입장 확인", 4) # 6 = True, 7 = False
                if mbox_flag == 6:
                    btns[contents.index(i)].click()
                    return
            else:
                return
        if i == contents[-1]:
            if '다음' in page_tag:
                click_xpath('//*[@id="btn-next"]')
                enter_class()
            else:
                ctypes.windll.user32.MessageBoxW(None, '마지막 강의 입니다.',"안내", 0)
                sys.exit()
                return
    return

def click_xpath(path):
    browser.find_element_by_xpath(path).click()
    browser.implicitly_wait(5)
    return 

try :
    with open(file_name,'r+',encoding='utf-8') as f:
        info = f.read()
        user_id = re.findall(r'{.*}', info)[0].replace('{','').replace('}','')
        user_pw = re.findall(r'{.*}', info)[1].replace('{','').replace('}','')
        class_ = re.findall(r'{.*}', info)[2].replace('{','').replace('}','')
        tmp_flag = 'F'
        try:
            tmp_flag = re.findall(r'{.*}', info)[3].replace('{','').replace('}','')
        except:
            f.write('\n강의 입장 확인 비활성화(T or F (Default) ) : {}')
        if tmp_flag == 'T':
            enter_disable = True
        else:
            enter_disable = False
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
        f.write('class(월화:a, 수목:b) : {}\n')
        f.write('강의 입장 확인 비활성화(T or F (Default) ) : {}')
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


login(user_id,user_pw)
    
click_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[1]/a')
register_today_study()

click_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[4]/a')
enter_class()

