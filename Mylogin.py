#!/usr/bin/python
#enconding=utf-8


'''
Creator:murphy.wang <wyz_sun@126.com>
Date:2014-12-27
Description:the class is for logining linux server

Note:
In case of normal,there are multithread in python function will happend "NoneType" Error.
so,it is googd idea define the class or function with python threading<thread module>
'''

import time,socket,struct
import paramiko as pk
import threading

class Mylogin():
    def __init__(self,host,port,username,passwd,cmd,outfile):
        self.host=host
        self.port=port
        self.username=username
        self.passwd=passwd
        self.cmd=cmd
        self.outfile=outfile
        self.dt=time.strftime('%Y%m%d%H%M%S')
        self.logfile='/tmp/mylogin-%s.log'%(self.dt)
        self.outfile=open(outfile,'a')
        pk.util.log_to_file(self.logfile)
        self.ssh=pk.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
        self.result="All logs:%s\nAll results:%s"%(self.logfile,self.outfile)
    def valid_ipv4(self):
        try:
            socket.inet_aton(self.host)
            return True
        except:
            print "The format of hostip is not correctly"
            return False

    def login_single(self):
        self.bb=self.valid_ipv4()
        if self.bb==True:
            try:
                self.ssh.connect(self.host,port=self.port,username=self.username,password=self.passwd)
                self.stdin,self.stdout,self.stderr=self.ssh.exec_command(self.cmd)
                self.outfile.write('*'*60+'Host:'+self.host+'\n')
                for self.line in self.stdout.readlines():
                    self.outfile.write(self.line)
            except Exception,e:
                print "Connect or Command failed!"+str(e)
                self.close()
        else:
            print 'The format of ip ranging is not correctly.Check it again!'
            self.ssh.close()

        return self.result
    def login_netrange(self):
        if self.host.find(':')!=-1:
            self.hostrange=self.host.split(':')
        elif self.host.find('-')!=-1:
            self.hostrange=self.host.split('-')
        else:
            print 'The format of ip ranging is not correctly.Check it again!'
            exit()

        self.start=socket.ntohl(struct.unpack("i",socket.inet_aton(str(self.hostrange[0])))[0])
        self.end=socket.ntohl(struct.unpack("i",socket.inet_aton(str(self.hostrange[1])))[0])

        for i in range(0,int(self.end-self.start)+1):
            try:
                self.host=socket.inet_ntoa(struct.pack('I',socket.htonl(self.start+long(i))))
                self.login_single()
            except:
                continue

    def login_netlist(self):
        self.hostlist=[]
        if isinstance(self.host,list) or isinstance(self.host,tuple):
            for j in range(0,len(self.host)):
                self.hostlist.append(self.host[j])
            self.host=''
        for i in range(0,len(self.hostlist)):
            self.host=self.hostlist[i]
            self.login_single()
        
    def close(self):
        self.outfile.close()
        self.ssh.close()

'''
hostlist='127.0.0.1-127.0.0.7'
my=Mylogin(hostlist,5888,'root','123456789','uname -r','/tmp/res1213.txt')
my.login_netrange()
my.close()
'''
