#!/bin/python
#encoding=utf-8

'''
Creator:murphy.wang <wyz_sun@126.com>
Datetime:2014-12-02
Description: we can find/update/delete mysqld paramiters which is in config file.
Note: we can process string formatting(like "key=value",Not support updating for "key") with this script
'''

import os,ConfigParser as p

class Myconfig():
	def __init__(self,confile):
		self.confile=confile

	def update(self,section,k,v):
		cc=p.ConfigParser()
		try:
			cc.read(self.confile)
		except Exception,e:
			f=0

		secs=cc.sections()
		for i in range(0,len(secs)):
			if secs[i]==section:
				cc.set(section,k,v)
		cc.write(open(self.confile,'w'))

	def find(self,var):
		cc=p.ConfigParser()
		try:
			cc.read(self.confile)
		except Exception,e:
			f=0
		
		secs=cc.sections()
		for i in range(0,len(secs)):
			try:
				vars=secs[i]+'.'+var+'='+cc.get(secs[i],var)
			except Exception,e:
				l=0
		return vars

	def delete(self,section,k):
		cc=p.ConfigParser()
		try:
			cc.read(self.confile)
		except Exception,e:
			f=0

		secs=cc.sections()
		for i in range(0,len(secs)):
			if secs[i]==section:
				cc.remove_option(secs[i],k)
		cc.write(open(self.confile,'w'))

'''
## the flowing code is for testing;
wyz3306=Myconfig('/mysql/etc/mysql-3306.cnf')
basedir=wyz3306.find('basedir')
print 'the basedir: %s'%(basedir)
wyz3306.update('mysqld','hostname','')
localhost=wyz3306.find('hostname')
print "hostname is %s"%(localhost)

wyz3306.delete('mysqld','hostname')
'''