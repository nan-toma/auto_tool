#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telnetlib import Telnet
from datetime import date,datetime
import sys
import ont_change_cmd as occ
import ont_change_judge as ocj
from judge_list import judge_def as jd
import os

import json
import pprint


args = sys.argv

class ont_change_auto:

    __ManagementIP = "10.1.5.15"
    __SysName = 0
    __Slot = 1
    __Port = 2
    __LogicalPort = 15
    __OnuSerial = "48575443022F749B"

    User = "odoroki2"             
    Password = "Momonoki2"


    def __init__(self,IP=__ManagementIP, SN=__SysName, Sl=__Slot, Pr=__Port, LP=__LogicalPort, OS=__OnuSerial):
        self.ip = IP
        self.sn = SN
        self.sl = Sl
        self.pr = Pr
        self.lp = LP
        self.os = OS


    #メイン関数
    def main(self):
        #telnet実行
        TN = self.telnet()

        #login,enable実行
        self.login(TN)
        self.enable(TN)

        #ディレクトリ作成
        new_dir_path = "logs/" + str(date.today())
        new_dir_path_json = "json/" + str(date.today())
        try:
            os.mkdir(new_dir_path)
        except FileExistsError:
            pass

        try:
            os.mkdir(new_dir_path_json)
        except FileExistsError:
            pass
        
        #コマンド実行
        per_list = [self.ip, self.sn, self.sl, self.pr, self.lp, self.os]
        cmd_list = occ.create_list(*per_list)

        start_num = 0 
        end_num = None
        for num,cmd in enumerate(cmd_list[start_num:end_num]):
            if cmd == "save":
                jd.version_state = None
            
            elif cmd == "config" and jd.version_state == "file,OK":
                jd.version_state = None

            if jd.continue_or == 1:     #変数が1の場合は、終了
                break

            elif jd.version_state == "version,OK" or jd.version_state == "file,OK": #versionが合っている場合は、saveまでpass。fileがある場合は、configまでpass
                continue

            # elif "modify" in cmd:      #modifyコマンドをパス
            #     print("pass modify")

            # elif "save" in cmd:      #saveコマンドをパス
            #     print("pass save")

            else:
                # if "reset" in cmd:    #resetコマンドをパス
                #     print("pass reset")
                #     cmd = "return"
                output = occ.cmd_action(TN,cmd)

                #出力結果をファイルに書き込み、保存
                d_now = datetime.now()
                file_path = new_dir_path + "/" + cmd.replace(" ", "").replace("/", "-")+ str(d_now.hour) + ":" + str(d_now.minute) + ":" + str(d_now.second) + ".txt"

                with open(file_path, mode='w') as f:
                    f.write(output)

                #判定
                result = ocj.judge(file_path, num+start_num, *per_list)
                print(result)

        #ログアウト
        self.logout(TN)


        #結果
        Result_all = jd.result #総合判定結果
        message = result #エラー理由
        logs = jd.result_log #ログ

        json_result = {"ResultMessage":Result_all, "NoticeMessage":result, "logs":jd.result_log}
        #print(json_result)
        if Result_all == "OK":
            print("ALL OK")
        else:
            print(Result_all,message)

        #出力結果をファイルに書き込み、保存
        file_path_json = new_dir_path_json + "/" + str(datetime.now()) + ".json"

        with open(file_path_json, mode='w') as f:
            json.dump(json_result, f, indent=4)
        


    # MSAN2にログイン
    def telnet(self):
        try:
            tn = Telnet(self.ip,23,3)
        except:
            print("telnet不可")
            sys.exit()
        
        return tn


    #access
    def login(self,tn,user=User,password=Password):
        tn.read_until(b"User name: ",5)
        tn.write(user.encode('euc-jp') + b"\n")

        tn.read_until(b"password: ",5)
        tn.write(password.encode('euc-jp') + b"\n")


    #enable
    def enable(self,tn):
        tn.write(b"enable\n")

    # tn.read_util("Password")
    # tn.write(password + "\n")

    #logout
    def logout(self,tn):
        tn.write(b"quit\n")
        tn.write(b"y\n")

        tn.close()



if __name__ == '__main__':
    ont = ont_change_auto()
    ont.main()