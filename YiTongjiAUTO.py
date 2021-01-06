from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver
import time
import os
import os.path
import json
import shutil

def Console():
   print("SYSETM: Running With Console ...\n")
   global driver
   chrome_options = Options()
   chrome_options.add_argument('--headless')
   chrome_options.add_argument('--disable-gpu')
   chrome_options.add_argument('--ignore-certificate-errors') 
   chrome_options.add_argument('--ignore-ssl-errors') 
   chrome_options.add_argument('log-level=3')
   chrome_options.add_argument('blink-settings=imagesEnabled=false')                                                     
   chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
   username = os.environ[ 'USERNAME' ]
   userpath = 'C:\\Users\\' + username + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
   chrome_options.add_argument('--user-data-dir=' + userpath) 
   chrome_options.binary_location = r"C:\Users\SchoolWebLogin\ChromeCore\App\Chrome-bin\chrome.exe"                                             
   driver = webdriver.Chrome(executable_path=r".\ChromeCore\Driver\win32\chromedriver.exe",chrome_options=chrome_options) 
 
def GUI():
    print("SYSETM: Running With GUI ...\n")
    global driver
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors') 
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('log-level=3')
    #chrome_options.add_argument('blink-settings=imagesEnabled=false')                                                         
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    username = os.environ[ 'USERNAME' ]
    userpath = 'C:\\Users\\' + username + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    chrome_options.add_argument('--user-data-dir=' + userpath) 
    chrome_options.binary_location = r".\ChromeCore\App\Chrome-bin\chrome.exe"                                          
    driver = webdriver.Chrome(executable_path=r"C:\Users\SchoolWebLogin\ChromeCore\Driver\win32\chromedriver.exe",chrome_options=chrome_options)


def login_history():
    global driver
    print ("\n尝试用记录过的历史身份登录...")
    driver.get("https://www.ioteams.com/ncov/ccbuptxs#/report")                                 
    driver.implicitly_wait(3)                                                           
    try:
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div/button[1]').click()
        driver.implicitly_wait(3)                                                           
        print ("\n上报成功！:-)\n")
        driver.quit()
    except:
        print ("\n登录失败，可能是之前的身份记录已经失效或发生信息更新等其他错误！")
        print ("\n历史身份记录已被重置,请重新验证。")
        login_first()

def login_first():
    global driver
    #driver.get('chrome://settings/clearBrowserData')
    #driver.implicitly_wait(3)                                                      
    #driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    driver.implicitly_wait(3)                                                     
    driver.get("https://www.ioteams.com/ncov/ccbuptxs#/login")                 
    driver.implicitly_wait(3)                                                        
    print('\n第一次启用需要验证你的身份。')
    try:
        PhoneNumber = input('\n请输入手机号码：')
        driver.implicitly_wait(3)                                                           
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div/input').send_keys(PhoneNumber)
        driver.implicitly_wait(3)                                                           
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/button').click()
        driver.implicitly_wait(3)                                                           
        VerifyCode = input('\n请输入手机获取到的验证码：')
        driver.implicitly_wait(3)                                                           
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/input').send_keys(VerifyCode)
        driver.implicitly_wait(3)                                                           
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div/div[2]/button').click()
        driver.implicitly_wait(3)                                                           
        print ("\n登录成功，记录已保存。")
        login_history()
        driver.quit()
    except:
        print ("\n发生错误，请关闭重试。\n")
        driver.quit()    

def autorun():
    username = os.environ[ 'USERNAME' ]
    source_path = os.getcwd() + '\ChromeCore'
    target_path = 'C:\\Users\\' + username + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\ChromeCore'
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)
    CurrentPath = os.getcwd() + '\YiTongjiAUTO.exe'
    path = 'C:\\Users\\' + username + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\YiTongjiAUTOrun.vbs'
    vbs = '''set ws=WScript.CreateObject("WScript.Shell") 
ws.Run "''' + CurrentPath + ''' /start",1,True '''
    with open(path, 'w') as f:
        f.write(vbs)
    

if __name__ == '__main__':
    Console()
    #GUI()
    try:
        #autorun()
        #print("\n已经为你设置成开机自动启动并上报信息。")
        print("\n检查网络状态...")
        driver.get("https://www.ioteams.com/ncov/ccbuptxs#/report")  
        driver.maximize_window()
        driver.implicitly_wait(3) 
    except:
        print("\n设置开机自启动失败，请关闭程序并右键以管理员模式运行再试。")
        print("\n检查网络状态...")
                                                  
    try:
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div/button[1]')
        driver.implicitly_wait(3)                                                           
        login_history()
    except:
        login_first()