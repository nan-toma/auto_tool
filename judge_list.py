#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from ont_change_auto import ont_change_auto as oca
import sys
import time
import ont_change_cmd as occ

class judge_def:

    #継続するかを決める変数
    continue_or = 0

    #version情報
    version_state = "NG"

    #総合判定
    result = "NG"

    #ログ結果
    result_log = ""

    def __init__(self,ip, sn, sl, pr, lp, os):
        self.sn = sn
        self.sl = sl
        self.pr = pr
        self.lp = lp
        self.os = os

    #sは出力結果が格納されたファイル
    #scroll
    def j_scr(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()
        return output_list[0]

    #undo terminal monitor
    def j_utm(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()
        return output_list[0]
    
    #display ont info summary 0/1/<Port> | include Distance|Last|DownTime|0   o|(dBm)|1-<Port>-<LogicalPort>
    def j_doi(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()

        #onlineの確認
        if "offline" in output_list[6]:
            return output_list[0] + " is OK"
        elif "online" in output_list[6]:
            self.__class__.continue_or = 1
            return "NotOK, online"
        else:
            return "事前ONT状態異常"
            

    #display ont autofind all
    def j_doa(self,s):
        output_list = s.splitlines()
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        if ("0/{}/{}".format(self.sl,self.pr) in s) and (self.os in s):
            return output_list[0] + " is OK"
        elif "Failure: The automatically found ONTs do not exist" in s:
            self.__class__.continue_or = 1
            print(output_list[0])
            return "新規ONT登録なし"
        else:
            self.__class__.continue_or = 1
            print(output_list[0])
            return "ERROR\n" + s

    #config
    def j_con(self,s):
        output_list = s.splitlines()
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        return output_list[0]

    #interface gpon 0/1
    def j_ig(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()
        return output_list[0]
    
    #modify
    def j_om(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()
        return output_list[0]
    
    #return
    def j_re(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        time.sleep(3)
        output_list = s.splitlines()
        return output_list[0]

    #display ont info summary 0/1/<Port> | include Distance|Last|DownTime|0   o|(dBm)|1-<Port>-<LogicalPort>
    def j_doi2(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()

        #onlineの確認
        if "online" in output_list[6]:
            pass
        elif "offline" in output_list[6]:
            self.__class__.continue_or = 1
            return "NotOK, offline"
        else:
            self.__class__.continue_or = 1
            print("STATE ERROR")
            return s

        #シリアルの確認
        if self.os in output_list[9]:
            pass
        else:
            self.__class__.continue_or = 1
            return "SIRIAL ERROR"
        
        #受光レベル確認
        new_out = [e for e in output_list[9].split(" ") if e not in " "]
        RXpower = float(new_out[4].split("/")[0])
        if -28 <= RXpower <= -8:
            return output_list[0] + " is OK"
        elif -28 > RXpower and RXpower > -8:
            self.__class__.continue_or = 1
            print(output_list[0]) + "is ERROR"
            return "RXpower unusual"
        else:
            self.__class__.continue_or = 1
            print(output_list[0]) + " is ERROR"
            return "RXpower ERROR"

        #return output_list[9]

    #display ont version 0 1 <Port> <LogicalPort> | include Main Software Version
    def j_dov(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        if "V8R019C10S102" in s:
            self.__class__.version_state = "version,OK"
            output_list = s.splitlines()
            return output_list[0] + "is OK"
        else:
            print(output_list[0]) + " is ERROR"
            return "version is different"
    
    # display file MxUV800R019C10SPC102_common_all.bin
    def j_df(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        if "not exist" in s:
            print(output_list[0]) + " is no file"
            return "file is not exist"
        else:
            self.__class__.version_state == "file,OK"
            output_list = s.splitlines()
            return output_list[0] + " is OK"

    #load file ftp 219.188.193.38 msan/firmware/MxUV800R019C10SPC102_common_all.bin
    def j_lff(self,s):
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        output_list = s.splitlines()
        return output_list[0]

    #Whether to start loading? (y/n)[n]:y
    def j_Wts(self,s):
        output_list = s.splitlines()
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        if "Failure" in s:
            print(output_list[0] + " is ERROR")
            self.__class__.continue_or = 1
            return "Firmwareダウンロード失敗"
        else:
            print("成功")
            time.sleep(90)
            return output_list[0] + " is OK"


    #display file MxUV800R019C10SPC102_common_all.bin
    def j_df2(self,s):
        output_list = s.splitlines()
        self.__class__.result_log += s + "\n" # 最後に出力するログを格納する
        if "not exist" in s:
            self.__class__.continue_or = 1
            print(output_list[0] + " is nofile")
            return "file is not exist"
        else:
            output_list = s.splitlines()
            return output_list[0] + "is OK"

    #config
    def j_con2(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #ont load 0/1/<Port> <LogicalPort> mxuv800r019c10spc102_common_all.bin activemode next-startup
    def j_ol(self,s):
        output_list = s.splitlines()
        return output_list[0]


    #display ont load state all | include 0/0/0.+*0
    def j_dol(self,s):
        if "Fail" in s:
            self.__class__.continue_or = 1
            return "Firmwareダウンロード失敗"
        else:
            output_list = s.splitlines()
            return output_list[0]

    #interface gpon 0/1
    def j_ig2(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #ont reset graceful <Port> <LogicalPort>
    def j_org(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #Are you sure to reset the ONT(s)? (y/n)[n]:y
    def j_Ays(self,s):
        time.sleep(90)
        output_list = s.splitlines()
        return "RESET"


    #return
    def j_re2(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #display ont info summary 0/1/<Port> | include Distance|Last|DownTime|0   o|(dBm)|1-<Port>-<LogicalPort>
    def j_doi3(self,s):
        return self.j_doi2(s)

    #display ont version 0 1 <Port> <LogicalPort> | include Main Software Version
    def j_dov2(self,s):
        return self.j_dov(s)

    #save
    def j_s(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #backup configuration tftp 221.111.4.119 /var/tftpboot/LATEST/AR/<ManagementIP>.txt
    def j_bct(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #y
    def j_y2(self,s):
        return "backup"

    # # config
    # def j_con3(self,s):
    #     pass


    # # diagnose
    # def j_dia(self,s):
    #     pass

    # # ont-load info program msan/firmware/ONTToolsV100R002C00SPC180_common_all_packet.bin ftp 219.188.193.38 gepon ge_ponpon
    # def j_oli(self,s):
    #     pass

    # # display ont-load info
    # def j_dol2(self,s):
    #     pass
    # # ont-load select <Flame>/<Slot> <Interface> <ONT-ID>
    # def j_olse(self,s):
    #     pass
    # # ont-load start activemode next-startup
    # def j_olsa(self,s):
    #     pass
    # # display ont-load select
    # def j_dol3(self,s):
    #     pass

    # # ont-load stop
    # def j_olst(self,s):
    #     pass

    # # telnet ont <Flame>/<Slot>/<Interface> <ONT-ID>
    # def j_to(self,s):
    #     pass
    # # quit
    # def j_quit(self,s):
    #     pass

    #display alarm history alarmtime start 2020-07-12 00:00:00 end 2020-07-13 23:59:59 list | include ( )
    def j_dah(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #display event history eventtime start 2020-07-12 00:00:00 end 2020-07-13 23:59:59 list | include ( ) | exclude Telnet
    def j_deh(self,s):
        output_list = s.splitlines()
        return output_list[0]

    #display logfile all starttime 2020-07-12T00:00:00 endtime 2020-07-13T23:59:59 | include cmd | exclude (cmd: log off|cmd: log on|cmd: scroll|cmd: terminal monitor|cmd: undo smart)
    def j_dla(self,s):
        self.__class__.result = "OK"
        output_list = s.splitlines()
        return output_list[0]


    