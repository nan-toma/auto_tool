#!/home/ryo.ajima03/usr/bin/python3.6
#coding: euc-jp
"""
Create By Ryo Ajima
Last updated 2018/06/18

MSAN?Etelnet?・?A5?i-3I??Τ??a?Υ3\?o\?oA?yt?o?C
\??o\3\?o\E??´??Υ?!\?\e??n?-?Ф1
"""
__author__ = "Ryo Ajima <ryo.ajima03@g.softbank.co.jp>"
__version__ = "1.0"
__date__    = "2017/10"

import re
import time
import random
import subprocess
import telnetlib
import sys
sys.path.append('/home/ryo.ajima03/src/MSAN_TOOL/logs')
import datetime
import codecs
import os

class GetAllLog :
  __id = "odoroki"
  __pass = "momonoki"
  __hostorip = ""
  __telnet = "empty"
  __rand_num = ""
  __dir_name_full = ""

  def __init__(self, hostorip):
    """
    \3\o\1\??\?
    @param hostorip MSAN?Υ?1\E?orIP\￠\??
    """
    self.__hostorip = hostorip
  # end def

  def makeRandDir(self):
    """
    \?3E?I?IId?o??Υ?￡\?\?e?o8.?1?e
    8.，a??￣\?E?o??E?
    """
    flag = 1
    # \?￡\?\?e?I?p?￢\Хa?￡\o\°?・????≪\e§\a￣
    while(flag):
      unique_num = random.randint(0,999999)

      if(os.path.exists("/home/ryo.ajima03/src/MSAN_TOOL/logs/Randlogs/%d"%(unique_num))):
        flag = 1
      else:
        flag = 0

    subprocess.check_output(['install', '-d', '-m', '777',"/home/ryo.ajima03/src/MSAN_TOOL/logs/RandLogs/%d"%(unique_num)])
    self.__rand_num = unique_num
  # end def

  def makeCommandsList(self, name, commands):
    """
    ?・????1?3\?o\??\?ooi.?1??
    \?!\?\e??IDynamicCommands.txt
    """
    path_list = "/home/ryo.ajima03/src/MSAN_TOOL/commands/%s.txt"%(name)
    if(os.path.isfile(path_list)):
      pass # do nothing
    else: # command list exists.
      subprocess.run(['rm', "%s"%(path_list)])

    with open("%s"%(path_list), "w") as f_commands:
      for command in commands:
        f_commands.write("%s\n"%(command))
    # end with
  # end def

  def getLog(self, command_list):
    """
    ??¨?e??Eo°?I5?i-3I?I?Υ??oId?o\?￡\?\?eC???E8.?1?e
    @param \3\?o\??\E:MSAN?OA?yt??\?o\??\E(2t1?eA?e)
    """
    # \3\?o\??\?oA??t?a
    f_cmd = open("%s"%(command_list), "r")
    temp = []
    temp = command_list.split("/")
    file_name = temp[-1].split(".")[0]
    cmd = f_cmd.readline()
    # \3\?o\??\?Υ?!\?\e??Υ?￡\?\?e?oId?o\?￡\?\?eC????i.
    self.__dir_name_full = "/home/ryo.ajima03/src/MSAN_TOOL/logs/RandLogs/%s/%s"%(self.__rand_num, file_name)
    subprocess.check_output(['install', '-d', '-m', '777', self.__dir_name_full])
    # °??\3\?o\?1OEe???-\1\??!\?\e??DII
    while(cmd):
      repeat_count = 0
      redo = 1
      no_space_cmd = cmd.replace(" ", "")
      no_space_cmd = no_space_cmd.replace("\n", "")
      no_space_cmd = no_space_cmd.replace("/", "")
      no_space_cmd = no_space_cmd.replace("|", "")
      while(redo == 1):
        repeat_count += 1
        f_res = open("%s/%s.txt"%(self.__dir_name_full, no_space_cmd), "w")
        self.__telnet.write(cmd.encode('euc-jp')) # \3\?o\EA?yt?s

        if("show syslog" in cmd):
          time.sleep(1)
        # end if

        chars = self.__telnet.read_until(b"# ", 5).decode('ascii') # \3\?o\?ηe2IA??t?s

        # 52o・≪?eE?・??-?do??3\?o\?￢At?e????i1c??￠?-?e?a?e
        if(repeat_count > 5):
          f_res.write("Inputed Command didn't log output correctly...\n")
          break
        # end if

        # °????On°??n?-?Ф1 ??????n?-1t????
        # ?n?-1t??i????e?Τ￢byte\??\???ΤC1?≫u1?≫u?n?-1t?a
        # ，Τ?t1?3!?\?o??±?μ?≫?e(\n\r)
        first_line = 0
        line = ""
        count = 0
        line_count = 1
        for char in chars:
          if(count < 2):
            line = line + char
            if(char == "\n" or char == "\r"):
              count += 1
          else: # ?3???e2t1?1??°?????νeIy
            if(line_count == 1 and cmd.strip() == line.strip()):
              redo = 0
            # end if
            f_res.write(line)
            line = "" + char
            line_count += 1
            count = 0
          # end if
        # end for
        os.chmod("%s/%s.txt"%(self.__dir_name_full, no_space_cmd), 0o777)
        f_res.close()
      #end while(redo)
      cmd = f_cmd.readline()
    # end while
    f_cmd.close()
    f_res.close()
  # end def

  def login(self):
    """
    MSAN???\?\o?1????-????i1c?I1?oE?1
    @return \3!?\?§1->\Ρ?\?￢，≪??≪?e??? -1->TelnetE?A
    """
    try:
      f_nodelist = codecs.open("/var/www/html/core-pj/msanlist.txt" , encoding="euc-jp")
      f_nodelist_line = f_nodelist.readline()
      ip_pattern = r",%s," %(self.__hostorip)
      host_pattern = r"^%s," %(self.__hostorip)
      Exist = 0 # ，!o÷2AEY?AeIN

      # \Ρ?\?oo?1!￡，≪??≪?e??±?i?D1?oE?・??aλ
      while(f_nodelist_line):
        if(re.search(ip_pattern, f_nodelist_line) or re.search(host_pattern, f_nodelist_line)):
          hit_line = f_nodelist_line
          Exist = 1
          break
        # end if
        f_nodelist_line = f_nodelist.readline()
      # end while

      if(Exist): # \Ρ?\?￢，≪??≪?a??Τ?eIy?o3?±?e
        line_partition = hit_line.split(",")
        msan_ip = self.__hostorip = line_partition[3]
      else:
        #print("NOT EXIST SUCH HOST!")
        return 2

      # Ae´u?eA%??￢?￠??3I??1?e
      today = datetime.datetime.today().strftime("%Y%m%d") # o￡Au?IAuEO e.g. 20171108
      if(datetime.datetime.today().hour > 16): # 13≫t°???1?μ???eooAu?IAuEO
        oldday = datetime.datetime.today() + datetime.timedelta(-1)
      else: # Ae´u?eA%??￢?eA$μ?i?ep??e2Aup?Υ??o≫?|
        oldday = datetime.datetime.today() + datetime.timedelta(-2)
      oldday = oldday.strftime("%Y%m%d")

      if(os.path.exists("/home/ryo.ajima03/src/MSAN_TOOL/logs/DailyLogs/%s/%s"%(oldday, msan_ip))):
        pass
      else:
        return 4

      # 3oAo?IMSAN?￢，≪??≪?a??Τ?￠?eIy?o3?±??1!￡
      self.__telnet = telnetlib.Telnet(msan_ip, 23, 5)
      res = self.__telnet.read_until(b"login:", 5)
      if(res == b' '):
        return 1

      self.__telnet.write(self.__id.encode('euc-jp') + b"\n")
      self.__telnet.read_until(b"Password:")
      self.__telnet.write(self.__pass.encode('euc-jp') + b"\n")
      self.__telnet.read_until(b"GMT+9")
      self.__telnet.write(b"terminal length 0\n")
      self.__telnet.write(b"enable\n")
      self.__telnet.read_until(b"Password:",5)
      self.__telnet.write(self.__pass.encode('euc-jp') + b"\n")
      self.__telnet.read_until(b"#",5)
      return 0
    except IOError:
      return 1

  # end def

  def loginGPON(self, slot):
    """
    GPON CARD???\?\o?1???3?θa?EgetLog("Slot1GPON.txt")??≪，?O
    @param slot GPON CARD(1 or 2)
    @return \¨\?≫t -1 5?i 0
    """
    try:
      self.__telnet.write(b"telnet 169.254.255.10%d"%(slot) + b"\n")
      self.__telnet.read_until(b"login:", 5)
      self.__telnet.write(b"admin" + b"\n")
      self.__telnet.read_until(b"Password:", 5)
      self.__telnet.write(b"admin" + b"\n")
      self.__telnet.read_until(b">", 5)
      self.__telnet.write(b"enable" + b"\n")
      self.__telnet.read_until(b"#", 5)
    except IOError:
      return -1
  # end def

  def loginStandbySFU(self, pre_act):
    """
    Standby|?ISFU???\?\o?1?????θa??￠logoutSlot，??DACT?EIa?i?e
    SFU?ISwitchOverI??i.
    """
    if(pre_act == 5):
      slot = 1
    elif(pre_act == 6):
      slot = 2
    else:
      return -1

    try:
      command = "telnet 169.254.255.%s"%(slot)
      self.__telnet.write(command.encode("utf-8") + b"\n")
      self.__telnet.read_until(b"login:", 5)
      self.__telnet.write(b"odoroki" + b"\n")
      self.__telnet.read_until(b"Password:", 5)
      self.__telnet.write(b"momonoki" + b"\n")
      self.__telnet.read_until(b">", 5)
      self.__telnet.write(b"enable" + b"\n")
      self.__telnet.read_until(b"Password:", 5)
      self.__telnet.write(b"momonoki" + b"\n")
      self.__telnet.read_until(b"#", 5)
    except IOError:
      return -1
  # end def


  def logoutMSAN(self):
    """
    telnet?o\￣\?\o°iE??a???O
    @param telnet login()??Ф?-???a?A
    @return nothing
    """
    self.__telnet.close()
  # end def

  def logoutSLOT(self):
    """
    Act SFU?≪?eGPON??≪\μ\OSFU??Itelnet?oA?e
    """
    self.__telnet.write(b"exit" + b"\n")
    self.__telnet.read_until(b"#", 5)
  # end def

  def getRandNum(self):
    return self.__rand_num
  # end def

  def getRandDir(self):
    return self.__dir_name_full
  # end def

  def getIP(self):
    return self.__hostorip
  # end def

  def getTelnetSession(self):
    return self.__telnet
  # end def
# end class