from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from fake_useragent import UserAgent
import random
import deathbycaptcha
import base64
import io
import os

def fire_wd():
    options = webdriver.ChromeOptions()
    #chrome_options = Options()
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)
    #driver.get(url)
    driver.get("https://cl.delhivery.com/#/login")
    print(driver.current_url)
    return driver

def wait(n):
    return time.sleep(random.uniform(1,int(n)))

def login(wd):
    username = wd.find_element_by_id("mat-input-0")
    password = wd.find_element_by_id("mat-input-1")
    username.send_keys("SHOPHEAVENLYFRANCHISE")
    wait(7)
    password.send_keys("Chotu5151@")
    wait(4)
    #click login button
    wd.find_elements_by_class_name("dlv-btn-primary")[0].click()
    wait(5)
    
def get_data(wd):
    wd.find_elements_by_xpath('/html/body/app-root/app-home/div[2]/div[1]/div/div/div[1]/div/a')[0].click()
    wait(6)
    wd.find_elements_by_xpath('/html/body/app-root/tour-step-template/popper-content/div/div[1]/div[1]/button')[0].click()
    wait(5)
    wd.find_elements_by_xpath('//*[@id="sidebar-wrapper"]/sidebar/ul/li[7]/a/span')[0].click()
    wait(5)
    html_list = wd.find_element_by_class_name("remittance-body")
    items = html_list.find_elements_by_tag_name("li")
    main_list=[]
    temp=[]
    for item in items:
        text = item.text
        if text.startswith('₹') or text.startswith('P') or ('/' in text):
            if len(temp)!=3:
                temp.append(text)
            else:
                main_list.append(temp)
                temp=[]
                temp.append(text)
    main_list.append(temp)
    print(main_list)
    df = pd.DataFrame(main_list, columns = ['Date', 'Amount','State'])
    df.to_csv('users.csv',index=False)
    wait(3)
    wd.quit()
    
def get_captcha():
    img_base64 = wd.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, wd.find_element_by_xpath('//*[@id="cdk-step-content-0-0"]/div/form/div[1]/div[1]/img'))
    with open(r"image.jpg", 'wb') as f:
        f.write(base64.b64decode(img_base64))
    
    data= io.BytesIO(base64.b64decode(img_base64))
    wait(2)
    client = deathbycaptcha.SocketClient("devpatat", "Pass@0199")
    try:
        balance = client.get_balance()
        captcha = client.decode(data, 15)
        if captcha:
            print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
    except deathbycaptcha.AccessDeniedException:
        print("fail")
       
    cap = wd.find_element_by_id("mat-input-2")
    cap.send_keys(captcha["text"].upper())
    wait(1.5)
    #wd.find_elements_by_class_name("dlv-btn-primary")[0].click()
    print("Captcha Solved Successfully!")
    
# wd = fire_wd()
# wait(5)
# login(wd)
# wait(8)
# if 'login' in wd.current_url:
#     get_captcha()
#     wait(1)
# wait(3)
# get_data(wd)
fire_wd()