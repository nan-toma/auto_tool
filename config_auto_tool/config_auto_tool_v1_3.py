# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import time
import shutil
import os
import sys
import pyminizip
import zipfile
from tkinter import messagebox
#import tkinter.ttk as ttk
import config_auto_tool_func
import atexit

# D_number = "D597860025"
# OSS_number = "20200817014"
D_number,OSS_number = config_auto_tool_func.D_OSS_output()

#タイムアウトもしくは予期せぬエラー
ERROR_state = 1

with open("config_tool_pass.txt") as f:
    pass_file = f.readlines()
    #FMSのID
    ID = pass_file[0].lstrip("FMS_ID:").rstrip("\n") # ID = "toman01"

    #FMSのpassword
    password = pass_file[1].lstrip("FMS_PASSWORD:").rstrip("\n") # password = "C9a553b98f"

    #TRIOSのID
    T_ID = pass_file[2].lstrip("TRIOS_ID:").rstrip("\n")

    #TRIOSのpassword
    T_password = pass_file[3].lstrip("TRIOS_PASSWORD:").rstrip("\n") 

#証明書エラーを無視する
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptInsecureCerts'] = True

#ダウンロード先フォルダの作成
dl_folder_path = "C:\\Users\\{}\\Desktop\\config".format(ID)

for retry1 in range(100):
    try:
        os.mkdir(dl_folder_path)
        break

    except FileExistsError:
        shutil.rmtree(dl_folder_path)
        for retry2 in range(100):
            try:
                os.mkdir(dl_folder_path)
                break
            except PermissionError:
                print("mkdir failed, retrying") 
        break

    except PermissionError:
        print("mkdir failed, retrying") #たまにアクセス拒否されることがあるので、何回か繰り返す

#終了後に実行する関数
def final_func():
    global ERROR_state
    if ERROR_state == 1:
        messagebox.showinfo("エラー","タイムアウトもしくは予期せぬエラー")
    elif ERROR_state == 2:
        messagebox.showinfo("エラー","正常に終了しましたが、シリアルが登録されていません")
    elif ERROR_state == 0:
        messagebox.showinfo("メッセージ","正常に終了しました")

atexit.register(final_func)
    
##################################################################################
##################################################################################

##################################################################################
#FMSからファイルをダウンロード

#証明書エラーを無視する
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptInsecureCerts'] = True

#ダウンロード先フォルダの作成
dl_folder_path = "C:\\Users\\{}\\Desktop\\config".format(ID)

#ダウンロード先フォルダの指定
prefs = {
    "download.default_directory": dl_folder_path}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", prefs)
#chromeOptions.add_argument('--headless')

# ブラウザを開く。
driver = webdriver.Chrome(executable_path='chromedriver.exe', desired_capabilities=capabilities, chrome_options=chromeOptions)
driver.implicitly_wait(20)
#driver.minimize_window()

# FMSの検索TOP画面を開く。
driver.get("https://fmswebl2.bb.local/common/index.jsp")

#フレーム変更
driver.switch_to_frame(driver.find_element_by_name("head"))

# ログインIDを入力
driver.find_element_by_name("account").clear()
login_id = driver.find_element_by_name("account")
login_id.send_keys(ID)

#passwordを入力
driver.find_element_by_name("password").clear()
login_id = driver.find_element_by_name("password")
login_id.send_keys(password)

#ログインボタンをクリック
login_btn = driver.find_elements_by_name("login")
login_btn[2].click()

time.sleep(2)

#対象のシステムを選択
system_btns = driver.find_elements_by_tag_name("option")
for btn in system_btns:
    if btn.get_attribute("value") == "/BE/me2/||false||59":
        system_btn = btn


#対象のボタンをクリック
try:
    system_btn.click()
except NameError:
    ERROR_state = 3
    messagebox.showinfo("エラー","IDもしくはPASSWORDが間違っています。")

#ポップアップでOKを選択
Alert(driver).accept()

time.sleep(2)

#フレーム変更
driver.switch_to_frame(driver.find_element_by_name("header"))

#プルダウンでメニューを選択
menu_element = driver.find_element_by_name("menu")
menu_select_element = Select(menu_element)
if D_number[1] == "3": 
    menu_select_element.select_by_value("/BE/me2/index.jsp")
elif D_number[1] != "3":
    menu_select_element.select_by_value("/BE/svpn_me2/index.jsp")

#フレーム変更
driver.switch_to_frame(driver.find_element_by_name("search"))

# D番号を入力
D_num_select = driver.find_element_by_name("contractID")
D_num_select.clear()
D_num_select.send_keys(D_number)

#検索ボタンをクリック
search_btn = driver.find_element_by_name("basicSearch")
search_btn.click()

time.sleep(3)

#デフォルトに戻す
driver.switch_to.default_content()

#フレーム変更
driver.switch_to_frame(driver.find_element_by_name("result"))

time.sleep(3)

#更新ボタンをクリック
line_count = 0
while "result_btn" not in locals():
    #表示件数が0件の場合はberak
    if driver.find_element_by_class_name("RESULT_FOOTER_ME") == "表示件数 - 0件":
        break

    result_btns = driver.find_elements_by_tag_name("img")
    for btn in result_btns:
        if btn.get_attribute("title") == "更新可能":
            line_count += 1
            result_btn = btn

#冗長回線がある場合は、手動対応で行うため、処理終了
if line_count >= 2:
    ERROR_state = 3
    messagebox.showinfo("エラー","冗長回線があるため、手動での手配をお願いします。")
    sys.exit()
else:
    pass

#対象のボタンをコントロールクリックし、新規タブで開く

#検索結果がない場合はエラー
try:
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL)
    actions.click(result_btn)
    actions.perform()
except NameError:
    ERROR_state = 3
    messagebox.showinfo("エラー","対象のD番号はFMSに登録されていません")

#windowの切り替え
handle_array = driver.window_handles

#一部無駄なタブが出るので、close
driver.switch_to.window(handle_array[1]) 
driver.close()

#ダウンロードタブに移行
driver.switch_to.window(handle_array[-1])

#シリアルの有無を確認
detail_elements = driver.find_elements_by_class_name("DETAIL_LINE")
node_count = 0
for i in range(len(detail_elements)):
    if detail_elements[i].text == "WA2021" or detail_elements[i].text == "C881":
        node_count += 1
    else:
        pass


#configダウンロードボタンをクリック
config_btns = driver.find_elements_by_class_name("BTN_ACT")
for btn in config_btns:
    if btn.get_attribute("onclick") == "execConfigDownload(0);":
        config_btn = btn

#configダウンロードボタンをクリック
config_btn.click()

time.sleep(1)
#ポップアップでOKを選択
Alert(driver).accept()

time_count = 0
while len(os.listdir(dl_folder_path)) == 0 and time_count <= 30:
    time.sleep(3)
    time_count += 3

#ダウンロード画面クローズ
#driver.close()

#windowの切り替え
#driver.switch_to.window(handle_array[0])

#FMSのクローズ
#driver.close()

##################################################################################
#ダウンロードしたファイルの名称を変更
download_file = dl_folder_path + "\\" + os.listdir(dl_folder_path)[0] #ダウンロードしたファイルパスを取得
upload_file = dl_folder_path + "\\" + "{}_fullconfig.zip".format(D_number)

os.rename(download_file, upload_file)

##################################################################################
#TRIOS

# ブラウザを開く。
#driver = webdriver.Chrome(executable_path='chromedriver.exe')

#新規タブを開き、そこに移動
driver.execute_script("window.open()")
new_window = driver.window_handles[-1]
driver.switch_to.window(new_window)

# TRIOSを開く
driver.get("http://{}:{}@tog-linux:8800/cgi-bin/trios/main_noc.cgi".format(T_ID,T_password))
# driver.implicitly_wait(20)

# D番号を入力(原因不明だが、一回だけ実行するとエラーになるので2回実行)
for i in range(2):
    D_num_select = driver.find_element_by_name("circuit_num")
    D_num_select.clear()
    D_num_select.send_keys(D_number)


#検索ボタンをクリック
system_btns = driver.find_elements_by_tag_name("input")
for btn in system_btns:
    if btn.get_attribute("value") == "SEARCH":
        search_btn = btn

search_btn.click()

#オンサイトボタンをクリック
onsite_btn = driver.find_elements_by_name("onsite")
onsite_btn[1].click()

#ENTERボタンをクリック
system_btns = driver.find_elements_by_tag_name("input")
for btn in system_btns:
    if btn.get_attribute("value") == "ENTER":
        enter_btn = btn

enter_btn.click()

#OSS番号を入力
OSS_num_select = driver.find_element_by_name("ossttnumber")
OSS_num_select.clear()
OSS_num_select.send_keys(OSS_number)

#ENTERボタンをクリック
system_btns = driver.find_elements_by_tag_name("input")
for btn in system_btns:
    if btn.get_attribute("value") == "ENTER":
        enter_btn = btn

enter_btn.click()


#添付ファイル操作画面に移行するボタンをクリック
system_btns = driver.find_elements_by_tag_name("input")
for btn in system_btns:
    if btn.get_attribute("value") == "添付ファイル操作画面へ":
        file_operate_btn = btn

file_operate_btn.click()

#タブ移行
handle_array = driver.window_handles
driver.switch_to.window(handle_array[-1])


#ファイルを選択
driver.find_element_by_name("upfile").send_keys(upload_file)

#TRIOSサーバーに保存
system_btns = driver.find_elements_by_tag_name("input")
for btn in system_btns:
    if btn.get_attribute("value") == "TRIOSサーバ（onsite/da）に保存":
        file_save_btn = btn

file_save_btn.click()

#添付ファイル操作画面を閉じる
driver.close()


# #TRIOSの画面を閉じる
# driver.close()

#シリアルない場合はERROR_stateは2のまま、ある場合はERROR_stateを0に変更
if node_count == 1:
    ERROR_state = 2
else:
    ERROR_state = 0