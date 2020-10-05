import tkinter as tk
import sys
import csv
from tkinter import messagebox

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

# #me2のホワイトリストを読み込む
# with open('me2_not_backup_list.csv') as f:
#     reader = csv.reader(f)
#     me2_backup_list = [row[1] for row in reader]

# #svpnのホワイトリストを読み込む
# with open('svpn_not_backup_list.csv') as f:
#     reader = csv.reader(f)
#     svpn_backup_list = [row[1] for row in reader]


#D番号とOSSを入力
def D_OSS_input():
    #D番号
    global D_number
    global OSS_number
    D_number = txtBox_d.get() 
    OSS_number = txtBox_o.get()

    root.destroy()


def D_OSS_output():
    btnRead=tk.Button(root, height=1, width=10, text="実行", command=D_OSS_input)
    btnRead.pack()
    root.mainloop()

    #何も入力しない場合、もしくは片方しか入力されない場合は終了
    if (D_number == 0) or (OSS_number == 0):
        sys.exit()

    elif (D_number == "") or (OSS_number == ""):
        sys.exit()

    # elif (D_number not in me2_backup_list) and (D_number not in svpn_backup_list):
    #     messagebox.showinfo("エラー","冗長回線が含まれている、もしくは対象外の回線であるため手動で手配をお願いします。")
    #     sys.exit()

    return D_number,OSS_number