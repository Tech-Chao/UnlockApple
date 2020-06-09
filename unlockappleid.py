from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import base64
import time
import  json




def unlockAccount(email,pwd,brithday,questionAnswer):
    questionAnswer = json.loads(questionAnswer)
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    #chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 不显示Chrome

    # url地址
    forgetUrl = "https://iforgot.apple.com/"
    driver.get(forgetUrl)
    # 找到账号输入框
    print('输入邮箱'+email)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
        email)
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[3]/idms-toolbar/div/div/div/button').click()

    driver.implicitly_wait(5)
    # 通过判断是否存在答题解锁判断账号是否被锁
    try:
        optionquestions = driver.find_element_by_xpath('/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/authentication-method/div[2]/div[2]/div[1]/input')
        optionquestions.click()
    except Exception  as  e:
        driver.close()
        print('账号' + email + '未锁住')

    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/iforgot-nav/div/div/div[1]/div/div/button[2]').click()
    # page 3 day
    print("正在验证生日信息……")
    # driver.implicitly_wait(30)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/birthday/div[2]/div/masked-date/idms-error-wrapper/div/div/input').send_keys(
        brithday)
    time.sleep(1)

    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/iforgot-nav/div/div/div[1]/div/div/button[2]').click()
    # page 4 questiones
    print("正在验证信息2……")
    driver.implicitly_wait(3)
    # 三个验证问题会随机出现2个，需自行浏览器F12查看每个问题输入框的id，每个问题的id都是固定的
    try:
        q1 = driver.find_element_by_xpath(
            '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/verify-security-questions/div[2]/div[1]/label').text
        driver.find_element_by_xpath('/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/verify-security-questions/div[2]/div[1]/idms-textbox/idms-error-wrapper/div/div/input').send_keys(questionAnswer[q1])
    except Exception as e:
        pass
    try:
        q2 = driver.find_element_by_xpath('/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/verify-security-questions/div[2]/div[2]/label').text
        driver.find_element_by_xpath('/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/verify-security-questions/div[2]/div[2]/idms-textbox/idms-error-wrapper/div/div/input').send_keys(questionAnswer[q2])
    except:
        pass
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/iforgot-nav/div/div/div[1]/div/div/button[2]').click()

    # page 5 unlock
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/web-reset-options/div[2]/div[2]/div/button').click()
    # page 6 password
    print("正在输入密码……")
    driver.implicitly_wait(30)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/web-current-password/div[2]/div[1]/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
        pwd)
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/iforgot-nav/div/div/div[1]/div/div/button[2]').click()
    # page 7 success
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_xpath(
            '/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/sa/idms-flow/div/section/div/unlock-success/div[2]/div/button')
        print(email + "已成功解锁！")
    except:
        print("密码错误！")
    driver.quit()