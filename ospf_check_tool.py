#! -*- coding:utf-8 -*-
import csv
import codecs
import sys

args = sys.argv

#csvファイルをオープン
f_t = open("/home/nan.toma/msan_ospf_check/today_msan_ospf_csv/{}/output.csv".format(args[1]), "r", errors = "ignore") #今日のデータ

f_y = open("/home/nan.toma/msan_ospf_check/yesterday_msan_ospf_csv/{}/output.csv".format(args[2]), "r", errors = "ignore") #昨日のデータ
#fin  = codecs.open('/home/nan.toma/output.csv', 'r', 'euc_jp')
#fout = codecs.open('/home/nan.toma/output.csv', 'w', 'utf-8')


#csvデータを読み込む
reader_t = csv.reader(f_t)
reader_y = csv.reader(f_y)

#csvデータを2次元リストに変換
output_list_t = [row for row in reader_t]
output_list_y = [row for row in reader_y]
output_list =  output_list_y + output_list_t[1:] #昨日のデータと今日のデータを連結

#MSAN,logical_port,ZRのユニークリスト
MSAN_logical_ZR_list = []

for row in output_list[1:]:
    MSAN_logical_ZR_list.append((row[4],row[7],row[9]))

MSAN_logical_ZR_unique_list = list(sorted(set(MSAN_logical_ZR_list), key=MSAN_logical_ZR_list.index))    


OK_list = [] #ospfが最終的にupになっているmsanのリスト
NG_list = [] #ospfが最終的にdownになっているmsanのリスト

#csvデータからMSAN,論理ポート,ZRごとの最終ステータスを取得
for unique_list in MSAN_logical_ZR_unique_list:
    for row in output_list:
        if (unique_list[0] in row[4]) and (unique_list[1] in row[7]) and (unique_list[2] in row[9]):
            last_state = row #最後のステータスを取得       
    #最終ステータスがupならOK_listにappend
    if last_state[1] == "up":
        OK_list.append(last_state[4] + " " + last_state[7] + " " + last_state[9] + " is" + " OK" + " " + last_state[0] + "\n")
        pass
    #最終ステータスがup以外(down)ならNG_listにappend
    else:
        NG_list.append(last_state[4] + " " + last_state[7] + " " + last_state[9] + " is" + " NG" + " " + last_state[0] + "\n")
    
# check_output = "-----------OK_list-----------\n"
# for OK in OK_list:
#        check_output += OK

check_output = "\n\n"
check_output += "-----------NG_list-----------\n"

for NG in NG_list:
        check_output += NG

print(check_output)

#判定結果をファイルに入力
with open("/home/nan.toma/msan_ospf_check/check_output/check_output.txt", mode="w") as f:
        f.write(check_output)



f_t.close()
f_y.close()