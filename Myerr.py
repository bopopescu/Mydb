#!/usr/bin/python
#encoding=utf-8

'''
Creator:murphy.wang <wyz_sun@126.com>
Datetime:2014-12-02
Description: the script for getting mysqld error with interval;
Note: 
1.Unit
the unit for interval is second

2.format
Date formating support:
20140812 11:49:38 '%Y%m%d %H:%M:%S' len()=17
2014-08-12 11:49:38 '%Y-%m-%d %H:%M:%S' len()=19
140812 11:49:38  '%y%m%d %H:%M:%S' len()=15
'''

import time

class Myerr():
        def __init__(self,errfile,level,interval):
                self.errfile=str(errfile)
                self.interval=interval
                self.infos=[]
                self.local=int(time.time())

                try:
                        if int(level)==1:
                                self.level=['[ERROR]']
                        elif int(level)==2:
                                self.level=['[ERROR]','[Warning]']
                        elif int(level)==3:
                                self.level=['[ERROR]','[Warning]','[Note]']
                except Exception,e:
                        print "The type of level must be int."

        def get_err(self):
                file = open(self.errfile,'r')
                readsize=1000
                position=0
                lines=file.readlines(readsize)
                while file.tell() - position > 0:
                        position=file.tell()
                        for line in lines:
                                for i in range(0,len(self.level)):
                                        if line.find(self.level[i])!=-1:
                                                num=line.find(':')
                                                if num==9:
                                                        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(line[0:15],'%y%m%d %H:%M:%S'))
                                                elif num==13:
                                                        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(line[0:19],'%Y-%m-%d %H:%M:%S'))
                                                elif num==11:
                                                        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(line[0:17],'%Y%m%d %H:%M:%S'))
                                                else:
                                                        if len(self.infos)>0:
                                                                tim=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                                                        else:
                                                                tim=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime('1999-01-01 00:00:00','%Y-%m-%d %H:%M:%S'))
                                                
                                                dest=int(time.mktime(time.strptime(tim,"%Y-%m-%d %H:%M:%S")))                     
                                                if self.local-dest<=self.interval:
                                                        self.infos.append(line)

                        lines = file.readlines(readsize)
                return self.infos

'''
wyzerr=Myerr('/var/log/wyz/err.log',3,40000)
cc=wyzerr.get_err()
for i in range(0,len(cc)):
        print cc[i]
'''
