# -*- coding: utf-8 -*-
# !/usr/bin/python
import paramiko
import threading
import time


def ssh2(ip, username, passwd, cmd):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username, passwd, timeout=5)
    for m in cmd:
      stdin, stdout, stderr = ssh.exec_command(m,get_pty=True)
      if('sudo' in str(m)):
        stdin.write('dev'+'\n')
      stdin.write('repo'+'\n') #执行输入命令，输入sudo命令的密码，会自动执行
      stdin.write('reporepo'+'\n') #执行输入命令，输入sudo命令的密码，会自动执行
      time.sleep(1)
      # stdin.write("Y")   #简单交互，输入 ‘Y’
      out = stdout.readlines()
      # 屏幕输出
      for o in out:
        print (o),
    print ('%s\tOK\n' % (ip))
    ssh.close()
  except:
    print ('%s\tError\n' % (ip))


if __name__ == '__main__':
  # cmd = [ 'sudo groupadd docker','sudo gpasswd -a ${USER} docker','sudo service docker restart','newgrp - docker','sudo reboot']
  cmd = ['docker login registry.xzlcorp.com']#你要执行的命令列表
  username = "dev"  # 用户名
  passwd = "dev"  # 密码
  threads = []  # 多线程
  print ("Begin......")
  # ips = ['52', '118', '162']
  ips=['175']
  for i in ips:
    ip = '172.16.10.' + i
    a = threading.Thread(target=ssh2, args=(ip, username, passwd, cmd))
    a.start()
