# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
import tkinter as tk
import tkinter.ttk as ttk

#テキストボックス作成
root = tk.Tk()
root.geometry("400x200")
root.title('D番号とOSS番号を入力')

# ラベル
lbl_d = tk.Label(text='D番号：')
lbl_d.place(x=50,y=0)
lbl_d = tk.Label(text='OSS番号：')
lbl_d.place(x=37,y=20)

txtBox_d = tk.Entry()
txtBox_d.configure(state='normal', width=30)
txtBox_d.pack(anchor='center',expand=0)

txtBox_o = tk.Entry()
txtBox_o.configure(state='normal', width=30)
txtBox_o.pack(anchor='center',expand=0)

D_number = 0
OSS_number = 0


def config_download():
    #D番号
    # D_number = "D597860025"
    # OSS_number = "20200817014"
    self.D_number = txtBox_d.get()
    self.OSS_number = txtBox_o.get()

    root.destroy()

    with open("config_tool_pass.txt") as f:
        pass_file = f.readlines()
        #FMSのID
        ID = pass_file[0].rstrip("\n") # ID = "toman01"

        #FMSのpassword
        password = pass_file[1].rstrip("\n") # password = "C9a553b98f"

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


    #ダウンロード先フォルダの指定
    prefs = {
        "download.default_directory": dl_folder_path}
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    #chromeOptions.add_argument('--headless')

    # ブラウザを開く。
    driver = webdriver.Chrome(executable_path='chromedriver.exe', desired_capabilities=capabilities, chrome_options=chromeOptions)
    driver.implicitly_wait(20)

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
    system_btn.click()
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
    while "result_btn" not in locals():
        result_btns = driver.find_elements_by_tag_name("img")
        for btn in result_btns:
            if btn.get_attribute("title") == "更新可能":
                result_btn = btn
    else:
        pass

    #対象のボタンをクリック
    result_btn.click()

    #windowの切り替え
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[1])

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
    else:
        pass

    #ダウンロード画面クローズ
    driver.close()

    #windowの切り替え
    driver.switch_to.window(handle_array[0])

    #FMSのクローズ
    driver.close()

    #ダウンロードしたファイルのパスワード付き圧縮を行う
    download_file = os.listdir(dl_folder_path)[0]  #ダウンロードしたファイル名を取得
    up_folder_path = "C:\\Users\\{}\\Desktop\\upload_config".format(ID) #アップロード用のconfigファイルを置くフォルダを作成

    try:
        os.mkdir(up_folder_path)

    except FileExistsError:
        shutil.rmtree(up_folder_path)
        os.mkdir(up_folder_path)

    with zipfile.ZipFile(dl_folder_path + "\\" + download_file) as existing_zip:
        existing_zip.extractall(up_folder_path)

    upload_file = os.listdir(up_folder_path)[0]

    pyminizip.compress(
        up_folder_path + "\\" + upload_file,
        "\\",
        up_folder_path + "\\" + "{}_fullconfig.zip".format(D_number),
        'sbgnesic20',
        int(4)               #圧縮率：0～9 (0は無圧縮)
    )


    # ブラウザを開く。
    driver = webdriver.Chrome(executable_path='W:\chromedriver.exe', \
        desired_capabilities=capabilities)



btnRead=tk.Button(root, height=1, width=10, text="実行", command=config_download)
btnRead.pack()
root.mainloop()


def config_upload():
    with open("config_tool_pass.txt") as f:
        pass_file = f.readlines()

        #TRIOSのID
        T_ID = pass_file[2].rstrip("\n")

        #FMSのpassword
        T_password = pass_file[3].rstrip("\n") 

    # ブラウザを開く。
    driver = webdriver.Chrome(executable_path='W:\chromedriver.exe')


    # TRIOSを開く
    driver.get("http://{}:{}@tog-linux:8800/cgi-bin/trios/main_noc.cgi".format(T_ID,T_password))

    # D番号を入力
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


    # #ファイル選択ボタンをクリック
    # system_btns = driver.find_elements_by_tag_name("input")
    # for btn in system_btns:
    #     if btn.get_attribute("value") == "添付ファイル操作画面へ":
    #         file_operate_btn = btn

    # file_operate_btn.click()




    # #TRIOSの画面を閉じる
    # driver.close()

config_upload()