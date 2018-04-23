#!/usr/bin/python
#coding=utf-8


import paramiko

def sshclient_execmd(hostname, port, username, pk, execmd):
  paramiko.util.log_to_file("paramiko.log")

  s = paramiko.SSHClient()
  s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  s.connect(hostname=hostname,port=port,username=username,key_filename=pk)
  # s.connect(hostname=hostname, port=port, username=username, password=password)
  stdin, stdout, stderr = s.exec_command (execmd)
  stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

  print stdout.read()

  # s.close()



def main():

  hostname = '54.222.212.135'
  port = 22
  username = 'ec2-user'
  pk="./xinzhili-prod.pem"
  execmd = "free"

  sshclient_execmd(hostname, port, username,pk , execmd)


if __name__ == "__main__":
  main()
