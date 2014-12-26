#!/usr/bin/python
#encoding=utf-8

'''
Creator:	murphy.wang <wyz_sun@126.com>
Date	:	2014-12-22
Description:getting the infomation about CPU/MEMORY/DISK/NETWORK/PROCESS and others from Servers;

Note:


'''

import psutil as ps
import time

class Myserver():
    def __init__(self):
        self.nic='eth0'
        self.disk_part='/'
        self.pid='0'
        self.cpulcnt=ps.cpu_count(logical=True)
        self.cpupcnt=ps.cpu_count(logical=False)
        self.cpupercent=ps.cpu_times_percent(percpu=False)
        self.memtotal=ps.virtual_memory()
        self.diskconf=ps.disk_partitions()
        self.diskio=ps.disk_io_counters(perdisk=False)
        self.diskio2=ps.disk_io_counters(perdisk=True)
        self.swap=ps.swap_memory()
        self.netio_part=ps.net_io_counters(pernic=True)
        
    def get_server_info(self):
        self.res={}
        self.CPUnum="Pysical CPUs:"+self.cpupcnt+"\tLogical CPUs:"+self.cpulcnt
        self.MEMtotal='%.2f'%(list(self.memtotal)[0]/1024/1024/1024)+'G'
        self.SWAPtotal='%.2f'%(list(self.swap)[0]/1024/1024/1024)+'G'
        self.NIClist="Net_Interface:"+str((self.netio_part).keys())
        self.res['CPUs']=self.CPUnum
        self.res['Memory']=self.MEMtotal
        self.res['Swaps']=self.SWAPtotal
        self.res['Interfaces']=self.NIClist
        return self.res
    
    def get_cpu_state(self):
        self.CPUs={}
        cpu_tup=tuple(self.cpupercent)
        for i in range(0,len(cpu_tup)):
            self.CPUs['User']=str(cpu_tup[i])+'%'
        
        return self.CPUs
    def get_mem_state(self):
        self.res={}
        self.mem=list(self.memtotal)
        self.res['Total']=str(self.mem[0]/1024/1024)+'M'
        self.res['Used']=str(self.mem[3]/1024/1024)+'M'
        self.res['Free']=str(self.mem[4]/1024/1024)+'M'
        self.res['Buffer']=str(self.mem[7]/1024/1024)+'M'
        self.res['Cache']=str(self.mem[8]/1024/1024)+'M'
        
        return self.res
    def get_disk_state(self):
        self.res={}
        self.disklist2=tuple(self.diskio2.keys())
        self.Devicelist=[]
        for i in range(0,len(self.disklist2)):
            self.Devicelist.append(str('/dev/'+self.diskio2[i]))
            
        self.disklist=tuple(self.diskio)
        self.Read_per_IO=str('%.2f'%(self.disklist[2]/self.disklist[0]/1024))
        self.Write_per_IO=str('%.2f'%(self.disklist[3]/self.disklist[1]/1024))
        self.Read_per_Sec=str('%.2f'%(self.disklist[2]/self.disklist[4]/1024)+'K')
        self.Write_per_Sec=str('%.2f'%(self.disklist[3]/self.disklist[5]/1024)+'K')
        self.res['Read/IO']=self.Read_per_IO
        self.res['Write/IO']=self.Write_per_IO
        self.res['Read/S']=self.Read_per_Sec
        self.res['Write/S']=self.Write_per_Sec
        
        self.res['Devices']=self.Devicelist
        return self.res
    def get_disk_partition_usage(self,mountpoint):
        self.partlist=tuple(self.diskconf)
        self.diskusage={}
        self.res={}

        for i in range(0,len(self.partlist)):
            self.part_list=list(self.partlist[i])
            if self.part_list[1]==mountpoint:
                self.ldisk=ps.disk_usage(self.part_list[1]) 
                self.ldisks=list(self.ldisk)
                self.diskusage['Total']=str('%.2f'%(self.ldisks[0]/1024/1024)+'M')
                self.diskusage['Used']=str('%.2f'%(self.ldisks[1]/1024/1024)+'M')
                self.diskusage['Percent']=str('%.2f'%(self.ldisks[3])+'%')
                
                self.res['Disk Part Space']=self.diskusage
                
                self.logic_name=(self.part_list[0])[5:]
                self.partio=tuple((self.netio_part).get(self.logic_name))
                
                self.Read_per_IO=str('%.2f'%(self.disklist[2]/self.disklist[0]/1024))
                self.Write_per_IO=str('%.2f'%(self.disklist[3]/self.disklist[1]/1024))
                self.Read_per_Sec=str('%.2f'%(self.disklist[2]/self.disklist[4]/1024)+'K')
                self.Write_per_Sec=str('%.2f'%(self.disklist[3]/self.disklist[5]/1024)+'K')
                self.res['Read/IO']=self.Read_per_IO
                self.res['Write/IO']=self.Write_per_IO
                self.res['Read/S']=self.Read_per_Sec
                self.res['Write/S']=self.Write_per_Sec
    
            else:
                continue
        if len(self.res)==0:
            print "The mountpoint is not Exist or Correctly,Check it again!"
            
        return self.res
            
    def get_net_pernic_state(self,nicname):
        self.res={}
        self.nics=tuple(self.netio_part)
        for i in range(0,len(self.nics)):
            if self.nics[i]==nicname:
                self.nicstate=tuple((self.netio_part).get(nicname))
                self.res['Kbytes/Sent']='%.2f'%(self.nicstate[0]/1024/1024)
                self.res['Kbytes/Recv']='%.2f'%(self.nicstate[1]/1024/1024)
                self.res['Err_in_out']=int(self.nicstate[4]+self.nicstate[5])
                self.res['Drop_in_out']=int(self.nicstate[6]+self.nicstate[7])
            else:
                continue
        if len(self.res)==0:
            print "The Interface name is not Exist or Correctly,Check it again!"
            
    def get_proc_state(self,pid):
        self.res={}
        self.mem={}
        self.pio={}
        self.conn={}
        self.result={}
        
        if ps.pid_exists(pid):
            self.pp=ps.Process()
            self.res['Status']=self.pp.status()
            self.res['Username']=self.pp.username()
            self.res['Createtime']=str(time.strftime('%Y%m%d %H:%M:%S',self.pp.create_time()))
            self.res['CPU percent']=str(self.pp.cpu_percent())+'%'
            self.res['MEM percent']=str('%.3f'%(self.pp.memory_percent()))+'%'
            
            self.cc=tuple(self.pp.memory_info_ex())
            self.mem['RSS']=str(self.cc[0])+'K'
            self.mem['Shared']=str(self.cc[2])+'K'
            self.mem['Lib']=str(self.cc[4])+'K'
            self.mem['Data']=str(self.cc[5])+'K'
            
            self.dd=tuple(self.pp.io_counters())
            self.pio['Read_cnt']=self.dd[0]
            self.pio['Write_cnt']=self.dd[1]
            self.pio['Read_byte']=self.dd[2]
            self.pio['Read_byte']=self.dd[3]
            
            self.result['Pid Info']=self.res
            self.result['Pid Mem']=self.mem
            self.result['pid IO']=self.pio
        else:
            print "The pid is not exist or Correctly."
        
        if len(self.result)==0:
            print "The pid is not exist or Correctly."
        
        return self.result
        