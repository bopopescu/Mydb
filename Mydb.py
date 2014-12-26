#!/usr/bin/python
#encoding=utf-8

'''
Creator:wyz_sun@126.com
Date:2014-12-18
Description: Mydb class for connectting db and getting static or dymatic variables 
'''

import MySQLdb as mysqldb

class Mydb():
	host=''
	user=''
	passwd=''
	db=''
	unix_socket=''
	connect_timeout=60
	charset='utf8'

	def __init__(self,host,user,passwd,db,unix_socket,connect_timeout,charset):
		self.host=host
		self.user=user
		self.passwd=passwd
		self.db=db
		self.charset=charset
		self.unix_socket=unix_socket
		self.connect_timeout=connect_timeout
		self.charset=charset
		try:
			self.conn=mysqldb.connect(user=self.user,host=self.host,passwd=self.passwd,db=self.db,charset=self.charset,unix_socket=self.unix_socket,connect_timeout=self.connect_timeout)
			self.cur=self.conn.cursor()
			sqlpre="set session sql_mode='ERROR_FOR_DIVISION_BY_ZERO'"
			self.cur.execute(sqlpre)

		except MySQLdb.Error as e:
			print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

	def get_innodb_config(self):
		res={}
		sql="select variable_name,variable_value from information_schema.global_variables where variable_name in ('INNODB_DATA_HOME_DIR','INNODB_ADDITIONAL_MEM_POOL_SIZE','INNODB_BUFFER_POOL_SIZE','INNODB_SORT_BUFFER_SIZE','INNODB_LOG_GROUP_HOME_DIR','INNODB_LOG_GROUP_HOME_DIR','INNODB_LOG_BUFFER_SIZE','INNODB_LOG_FILE_SIZE','INNODB_FLUSH_LOG_AT_TRX_COMMIT','INNODB_LOG_FILES_IN_GROUP') order by variable_name;"
		self.cur.execute(sql)
		for row in self.cur.fetchall():
			res[row[0]]=row[1]
		return res

	def get_myisam_config(self):
		res={}
		sql="select variable_name,variable_value from information_schema.global_variables where variable_name in ('BASEDIR','DATADIR','KEY_BUFFER_SIZE','KEY_BUFFER_BLOCK_SIZE','KEY_CACHE_DIVISION_LIMIT','KEY_CACHE_AGE_THRESHOLD');"
		self.cur.execute(self.sql)
		for row in self.cur.fetchall():
			res[row[0]]=row[1]
		return res
	def get_innodb_status(self):
		res=[]
		statu={}
		ratios={}
		sql1="show engine innodb status;"
		sql2-"SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ('INNODB_BUFFER_POOL_READS','INNODB_BUFFER_POOL_READ_REQUESTS','QCACHE_HITS','QCACHE_INSERTS');"

		self.cur.execute(sql1)
		row=self.cur.fetchone()
		res.append(row)

		self.cur.execute(sql2)
		for x in self.cur.fetchall():
			statu[x[0]]=x[1]

		ratios['INNODB_BUFFER_READ_HITS']='%.2f'%((1-int(statu['INNODB_BUFFER_POOL_READS'])/int(statu['INNODB_BUFFER_POOL_READ_REQUESTS']))*100)
		ratios['QUERY_CACHE_HITS']='%.2f'%(int(statu['QCACHE_HITS'])/(int(statu['QCACHE_HITS'])+int(statu['QCACHE_INSERTS']))*100)
		res.append(ratios)
		return res
	def get_myisam_status(self):
		res=[]
		frag={}
		statu={}
		sql1="SELECT CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) TABLE_NAME,DATA_FREE/DATA_LENGTH AS FRAGMENT_RATIO FROM INFORMATION_SCHEMA.TABLES WHERE ENGINE='MYISAM' AND DATA_FREE/DATA_LENGTH>'0.15';"
		sql2="SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ('KEY_BLOCKS_UNUSED','KEY_BLOCKS_USED','KEY_READS','KEY_READ_REQUESTS','KEY_WRITES','KEY_WRITE_REQUESTS');"
		self.cur.execute(sql1)
		for row in self.cur.fetchall():
			frag[row[0]]=row[1]
		
		self.cur.execute(sql2)
		for row in self.cur.fetchall():
			statu[row[0]]=row[1]

		statu['KEY_BUFFER_READ_HITS']='%.2f'%((1-int(res['KEY_READS'])/int(res['KEY_READ_REQUESTS']))*100)
		statu['KEY_BUFFER_WRITE_HITS']='%.2f'%((1-int(res['KEY_WRITES'])/int(res['KEY_WRITE_REQUESTS']))*100)
		statu['INNODB_BUFFER_READ_HITS']='%.2f'%((1-int(res['INNODB_BUFFER_POOL_READS'])/int(res['INNODB_BUFFER_POOL_READ_REQUESTS']))*100)
		statu['KEY_BUFFER_USAGERATION']='%.2f'%(int(res['KEY_BLOCKS_USED'])/(int(res['KEY_BLOCKS_USED'])+int(res['KEY_BLOCKS_UNUSED']))*100)
		res.append(frag)
		res.append(statu)
		return res
	def get_mydb_info(self):
		dbinfo=()
		SIZEM={"DBTOTAL_SIZE(M)":0}
		ENGINE=[]
		DBNUM={"DBNUM":1}
		sql1='select "DBSIZE_TOTAL",truncate(sum(data_length)/1024/1024,2) "SIZE(M)" from information_schema.tables;'
		sql2='select "DBNUM",count(distinct table_schema) "DBNUM" from information_schema.tables;'
		sql3='select upper(engine),support,comment from information_schema.engines;'
		self.cur.execute(sql1)
		sizem=self.cur.fetchone()
		SIZEM['DBTOTAL_SIZE(M)']='%.2f'%(sizem[1])

		self.cur.execute(sql2)
		dbnum=self.cur.fetchone()
		DBNUM['DBNUM']=int(dbnum[1])

		self.cur.execute(sql3)
		for row in self.cur.fetchall():
			ENGINE.append(row)
		dbinfo=(SIZEM,DBNUM,ENGINE)
		return dbinfo

	def get_mydb_status(self):
		res={}
		ratios={}
		sql="select variable_name,variable_value from information_schema.global_status where variable_name in ('KEY_BLOCKS_UNUSED','KEY_BLOCKS_USED','CREATED_TMP_DISK_TABLES','CREATED_TMP_TABLES','THREADS_CACHED','CONNECTIONS','QUESTIONS','UPTIME','COM_COMMIT','COM_ROLLBACK','KEY_READS','KEY_READ_REQUESTS','KEY_WRITES','KEY_WRITE_REQUESTS','INNODB_BUFFER_POOL_READS','INNODB_BUFFER_POOL_READ_REQUESTS','QCACHE_HITS','QCACHE_INSERTS');"
		self.cur.execute(sql)
		for row in self.cur.fetchall():
			res[row[0]]=row[1]

		ratios['QPS']='%.2f'%(int(res['QUESTIONS'])/int(res['UPTIME']))
		ratios['TPS']='%.2f'%((int(res['COM_COMMIT'])+int(res['COM_ROLLBACK']))/int(res['UPTIME']))
		ratios['THREAD_CACHE_HITS']='%.2f'%((1-int(res['THREADS_CACHED'])/int(res['CONNECTIONS']))*100)
		ratios['KEY_BUFFER_READ_HITS']='%.2f'%((1-int(res['KEY_READS'])/int(res['KEY_READ_REQUESTS']))*100)
		ratios['KEY_BUFFER_WRITE_HITS']='%.2f'%((1-int(res['KEY_WRITES'])/int(res['KEY_WRITE_REQUESTS']))*100)
		ratios['INNODB_BUFFER_READ_HITS']='%.2f'%((1-int(res['INNODB_BUFFER_POOL_READS'])/int(res['INNODB_BUFFER_POOL_READ_REQUESTS']))*100)
		ratios['QUERY_CACHE_HITS']='%.2f'%(int(res['QCACHE_HITS'])/(int(res['QCACHE_HITS'])+int(res['QCACHE_INSERTS']))*100)
		ratios['KEY_BUFFER_USAGERATION']='%.2f'%(int(res['KEY_BLOCKS_USED'])/(int(res['KEY_BLOCKS_USED'])+int(res['KEY_BLOCKS_UNUSED']))*100)
		ratios['TMP_TABLE_RATIOS']='%.2f'%(int(res['CREATED_TMP_DISK_TABLES'])/int(res['CREATED_TMP_TABLES']))

		return ratios
	def get_deadlock(self):
		pass
	def get_event_wait(self):
		pass
	def conn_close(self):
		self.cur.close()
		self.conn.close()

'''
mydb=Mydb('127.0.0.1','root','root','mysql','/tmp/mysql-3306.sock',60,'utf8')
#res=mydb.get_innodb_config()
#inno=mydb.get_innodb_status()
#stat=mydb.get_mydb_status()
dbinfo=mydb.get_mydb_info()
print dbinfo
#mydb.conn_close()
'''

