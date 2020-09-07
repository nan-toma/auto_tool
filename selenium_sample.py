# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

#証明書エラーを無視する
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptInsecureCerts'] = True


# ブラウザを開く。
driver = webdriver.Chrome(executable_path='W:\chromedriver.exe',desired_capabilities=capabilities)

# Googleの検索TOP画面を開く。
driver.get("https://fmswebl2.bb.local/common/index.jsp")
#driver.get("https://www.yahoo.co.jp/")
#driver.get("https://sites.google.com/a/g.softbank.co.jp/ma_portal/home")

# # ログインIDを入力
#login_class = driver.find_element_by_name("account")
name = "account"
element = WebDriverWait(driver, 30).until(
	EC.visibility_of_element_located((By.name, name))
)
# login_btn.click()
# print(driver.find_elements_by_class_name())
#print(driver.title)

# ブラウザを終了する。
driver.close()


#<input type="password" size="24" name="password" value="" class="BOX" tabindex="2">

#<input type="text" id="jot-ui-searchInput" name="q" sizイトを検索">
# //*[@id="ContentWrapper"]/header/section[1]/div/form/fieldset/span/input
# /html/body/form/table/tbody/tr/td[3]/table/tbody/tr[2]/td[2]/input