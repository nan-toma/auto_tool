#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telnetlib
from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)

today_d = datetime.strftime(today, '%Y-%m-%d') #今日の日付
yesterday_d = datetime.strftime(yesterday, '%Y-%m-%d') #昨日の日付

def create_list(ip, sn, sl, pr, lp, os):

    #コマンドリスト
    command_list = [
        "scroll",
        "undo terminal monitor",
        "display ont info summary 0/{Slot}/{Port} | \
            include Distance|Last|DownTime|{LogicalPort}   o|(dBm)|1-{Port}-{LogicalPort}"\
                .format(Slot = sl, Port = pr, LogicalPort = lp),
        'display ont autofind all',
        "config",
        "interface gpon 0/{Slot}".format(Slot=sl),
        "ont modify {Port} {LogicalPort} sn {OnuSerial}".format(Port = pr, LogicalPort = lp, OnuSerial = os),
        "return",
        "display ont info summary 0/{Slot}/{Port} | \
            include Distance|Last|DownTime|{LogicalPort}   o|(dBm)|1-{Port}-{LogicalPort}"\
                .format(Slot = sl, Port = pr, LogicalPort = lp),
        "display ont version 0 {Slot} {Port} {LogicalPort} | include Main Software Version"\
            .format(Slot = sl, Port = pr, LogicalPort = lp),
        "display file MxUV800R019C10SPC102_common_all.bin",
        "load file ftp 219.188.193.38 msan/firmware/MxUV800R019C10SPC102_common_all.bin",
        "y",
        "display file MxUV800R019C10SPC102_common_all.bin",
        "config",
        "ont load 0/{Slot}/{Port} {LogicalPort} mxuv800r019c10spc102_common_all.bin \
            activemode next-startup".format(Slot = sl, Port = pr, LogicalPort = lp),
        "display ont load state all | include 0/{Slot}/{Port}.+*{LogicalPort}"\
            .format(Slot = sl, Port = pr, LogicalPort = lp),
        "interface gpon 0/{Slot}".format(Slot=sl),
        "ont reset graceful {Port} {LogicalPort}".format(Port=pr, LogicalPort = lp),
        "y",
        "return",
        "display ont info summary 0/{Slot}/{Port} | \
            include Distance|Last|DownTime|{LogicalPort}   o|(dBm)|{Slot}-{Port}-{LogicalPort}"\
                .format(Slot = sl, Port = pr, LogicalPort = lp),
        "display ont version 0 {Slot} {Port} {LogicalPort} | include Main Software Version"\
            .format(Slot = sl, Port = pr, LogicalPort = lp),
        "save",
        # "backup configuration tftp 221.111.4.119 /var/tftpboot/LATEST/AR/{ManagementIP}.txt"\
        #     .format(ManagementIP = ip),
        # "y",

        # "config",
        # "diagnose",
        # "ont-load info program msan/firmware/\
        #     ONTToolsV100R002C00SPC180_common_all_packet.bin ftp 219.188.193.38 gepon ge_ponpon",
        # "display ont-load info",
        # "ont-load select 0/{Slot} {Port} {LogicalPort}".format(Slot = sl, Port = pr, LogicalPort = lp),
        # "ont-load start activemode next-startup",
        # "display ont-load select",
        # "ont-load stop",
        # "telnet ont 0/{Slot} {Port} {LogicalPort}".format(Slot = sl, Port = pr, LogicalPort = lp),
        # "telnet ont 0/{Slot} {Port} {LogicalPort}".format(Slot = sl, Port = pr, LogicalPort = lp),
        # "quit",
        
        "display alarm history alarmtime \
            start {Yesterday} 00:00:00 end {Today} 23:59:59 list | include ( )"\
                .format(Yesterday = yesterday_d, Today = today_d),
        "display event history eventtime \
            start {Yesterday} 00:00:00 end {Today} 23:59:59 list | include ( ) | exclude Telnet"\
                .format(Yesterday = yesterday_d, Today = today_d),
        "display logfile all starttime {Yesterday}T00:00:00 endtime {Today}T23:59:59 | \
            include cmd | exclude (cmd: log off|cmd: log on|cmd: scroll|cmd: terminal monitor|cmd: undo smart)"\
                .format(Yesterday = yesterday_d, Today = today_d)

    ]

    return command_list

#コマンドを実行
def cmd_action(tn,cmd):
    tn.read_until(cmd.encode(),3 )
    tn.write(cmd.encode() + b"\n") #コマンドを入力

    result = tn.read_until(b"#",3).decode("ascii") #実行結果を挿入

    return result
            
