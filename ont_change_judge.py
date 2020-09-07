#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telnetlib
from judge_list import judge_def
from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)

today_d = datetime.strftime(today, '%Y-%m-%d') #今日の日付
yesterday_d = datetime.strftime(yesterday, '%Y-%m-%d') #昨日の日付

def func_act(func, arg):
    return func(arg)

#判定
def judge(file_path, judge_num, ip, sn, sl, pr, lp, os):
    jl = judge_def(ip,sn,sl,pr,lp,os)

    Judge_l = [jl.j_scr, jl.j_utm,jl.j_doi, jl.j_doa, jl.j_con, jl.j_ig, jl.j_om, jl.j_re, jl.j_doi2,\
        jl.j_dov,  jl.j_df, jl.j_lff, jl.j_Wts, jl.j_df2, jl.j_con2, jl.j_ol, jl.j_dol, jl.j_ig2, \
            jl.j_org, jl.j_Ays, jl.j_re2,jl.j_doi3, jl.j_dov2, jl.j_s, \
            # jl.j_bct, jl.j_y2,\
                # jl.j_con3, jl.j_dia, jl.j_oli, jl.j_dol2, jl.j_olse, jl.j_olsa, jl.j_dol3,jl.j_olst, jl.j_to, jl.j_quit, \
                 jl.j_dah, jl.j_deh,jl.j_dla]

    with open(file_path) as f:
        s = f.read() #出力結果が格納されたファイルを読み込む
        result = func_act(Judge_l[judge_num], s) #それに対し、判定を行い、判定結果を返す
    return result