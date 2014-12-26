#!/usr/bin/python

#encoding=utf-8


'''
'''
import MySQLdb as db
import os,time
import psutil as ps

class Performance_sql:
	def __init__(self,host,user,pwd,port,socket,sql):
		self.host=host
		self.user=user
		self.pwd=pwd
		self.port=port
		self.socket=socket
		self.sql=sql
		self.conn=db.connect(host=self.host,user=self.user,passwd=self.pwd,port=self.port,unix_socket=self.socket,timeout=30)
		self.cur=self.conn.cursor()

	def get_help():

	def get_explain(self.sql):
		self.sqlp="explain "+self.sql
		self.cur.execute(self.sqlp)
		self.requests=['| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |']
		for row in self.cur.fetchall():
			self.requests.append(rows)

		return self.requests

	def get_db_request():
		self.sql1="SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME='INNODB_BUFFER_POOL_READ_REQUESTS';"
		self.cur.execute(self.sql1)
		self.rows=cur.fetchone()
		self.requests=self.rows[0]

		return self.requests
	def get_timelong():		
		self.st=time.time()
		self.cur.execute(self.sql)
		self.ed=time.time()
		self.timelong=int(self.ed-self.st)
		
		return self.timelong
	def get_session():

	def close():
		self.cur.close()
		self.conn.close()

	def main():


	if '__name__'=='main':
		main()

