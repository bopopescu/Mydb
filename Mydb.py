#!/usr/bin/python
#encoding=utf-8

'''
Creator:wyz_sun@126.com
Date:2014-12-18
Description: Mydb class for connectting db and getting static or dymatic variables 
'''

import MySQLdb as mysqldb

class Mydb():
	def __init__(self,host,user,passwd,db,unix_socket):
		self.host=host
		self.user=user
		self.passwd=passwd
		self.db=db
		self.charset=charset
		self.unix_socket=unix_socket
		self.connect_timeout=60
		self.charset='utf8'
		try:
			self.conn=mysqldb.connect(user=self.user,host=self.host,passwd=self.passwd,db=self.db,charset=self.charset,unix_socket=self.unix_socket,connect_timeout=self.connect_timeout)
			self.cur=self.conn.cursor(cursorclass = mysqldb.cursors.DictCursor)
			sqlpre="set session sql_mode='ERROR_FOR_DIVISION_BY_ZERO'"
			self.cur.execute(sqlpre)

		except MySQLdb.Error as e:
			print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

	def get_innodb_config(self):
		res={}
		sql="SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME IN ('INNODB_DATA_HOME_DIR','INNODB_ADDITIONAL_MEM_POOL_SIZE','INNODB_BUFFER_POOL_SIZE','INNODB_SORT_BUFFER_SIZE','INNODB_LOG_GROUP_HOME_DIR','INNODB_LOG_GROUP_HOME_DIR','INNODB_LOG_BUFFER_SIZE','INNODB_LOG_FILE_SIZE','INNODB_FLUSH_LOG_AT_TRX_COMMIT','INNODB_LOG_FILES_IN_GROUP') ORDER BY VARIABLE_NAME;"
		self.cur.execute(sql)
		result=self.cur.fetchall()
		for i in range(0,len(result)):
			res[result[i].get('VARIABLE_NAME')]=result[i].get('VARIABLE_VALUE')

		return res

	def get_myisam_config(self):
		res={}
		sql="SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME IN ('BASEDIR','DATADIR','KEY_BUFFER_SIZE','KEY_BUFFER_BLOCK_SIZE','KEY_CACHE_DIVISION_LIMIT','KEY_CACHE_AGE_THRESHOLD');"
		self.cur.execute(self.sql)
		result=self.cur.fetchall()
		for i in range(0,len(result)):
			res[result[i].get('VARIABLE_NAME')]=result[i].get('VARIABLE_VALUE')

		return res
	def get_innodb_status(self):
		res=[]
		statu={}
		ratios={}
		sql1="show engine innodb status;"
		sql2-"SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ('INNODB_BUFFER_POOL_READS','INNODB_BUFFER_POOL_READ_REQUESTS','QCACHE_HITS','QCACHE_INSERTS');"

		self.cur.execute(sql1)
		row=self.cur.fetchone()['Status']
		res.append(row)

		self.cur.execute(sql2)
		status=self.cur.fetchall()
		for i in range(0,len(status)):
			statu[status[i].get('VARIABLE_NAME')]=status[i].get('VARIABLE_VALUE')

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
		frags=self.cur.fetchall()
		for i in range(0,len(frags)):
			frag[frags[i].get('VARIABLE_NAME')]=frags[i].get('VARIABLE_VALUE')
		
		self.cur.execute(sql2)
		status=self.cur.fetchall()
		for i in range(0,len(status)):
			statu[status[i].get('VARIABLE_NAME')]=status[i].get('VARIABLE_VALUE')

		statu['KEY_BUFFER_READ_HITS']='%.2f'%((1-int(res['KEY_READS'])/int(res['KEY_READ_REQUESTS']))*100)
		statu['KEY_BUFFER_WRITE_HITS']='%.2f'%((1-int(res['KEY_WRITES'])/int(res['KEY_WRITE_REQUESTS']))*100)
		statu['INNODB_BUFFER_READ_HITS']='%.2f'%((1-int(res['INNODB_BUFFER_POOL_READS'])/int(res['INNODB_BUFFER_POOL_READ_REQUESTS']))*100)
		statu['KEY_BUFFER_USAGERATION']='%.2f'%(int(res['KEY_BLOCKS_USED'])/(int(res['KEY_BLOCKS_USED'])+int(res['KEY_BLOCKS_UNUSED']))*100)
		res.append(frag)
		res.append(statu)

		return res
	def get_mydb_info(self):
		res={}

		sql1='SELECT TRUNCATE(SUM(DATA_LENGTH)/1024/1024,2) "SIZE(M)" FROM INFORMATION_SCHEMA.TABLES;'
		sql2='SELECT COUNT(DISTINCT TABLE_SCHEMA) "DBNUM" FROM INFORMATION_SCHEMA.TABLES;'
		sql3="SELECT * FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME='DEFAULT_STORAGE_ENGINE';"
		sql4="SELECT * FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME='CHARACTER_SET_SERVER';"
		self.cur.execute(sql1)
		sizem=self.cur.fetchone()
		res['DBTOTAL_SIZE(M)']='%.2f'%(sizem.get('SIZE(M)')

		self.cur.execute(sql2)
		dbnum=self.cur.fetchone()
		res['DBNUM']=int(dbnum.get('DBNUM'))

		self.cur.execute(sql3)
		engine=self.cur.fetchone()
		res[engine.get('VARIABLE_NAME')]=int(engine.get('VARIABLE_VALUE'))

		self.cur.execute(sql4)
		char=self.cur.fetchone()
		res[char.get('VARIABLE_NAME')]=int(char.get('VARIABLE_VALUE'))

		return res
	def get_engine_info(self):
		res={}
		sql="SELECT ENGINE,SUPPORT,COMMENT FROM INFORMATION_SCHEMA.ENGINES;"
		self.cur.execute(sql)
		res=self.cur.fetchall()
		
		return res
	def get_mydb_status(self):
		res={}
		ratios={}
		sql="SELECT VARIABLE_NAME,VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME IN ('KEY_BLOCKS_UNUSED','KEY_BLOCKS_USED','CREATED_TMP_DISK_TABLES','CREATED_TMP_TABLES','THREADS_CACHED','CONNECTIONS','QUESTIONS','UPTIME','COM_COMMIT','COM_ROLLBACK','KEY_READS','KEY_READ_REQUESTS','KEY_WRITES','KEY_WRITE_REQUESTS','INNODB_BUFFER_POOL_READS','INNODB_BUFFER_POOL_READ_REQUESTS','QCACHE_HITS','QCACHE_INSERTS');"
		self.cur.execute(sql)
		result=self.cur.fetchall()
		for i in range(0,len(result)):
			res[result[i].get('VARIABLE_NAME')]=result[i].get('VARIABLE_VALUE')

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
	def get_slave_status(self):
		result={}
		sql="show slave status;"
		self.cur.execute(sql)
		res=self.cur.fetchall()
		result['Slave_SQL_Running']=res[0].get('Slave_SQL_Running')
		result['Slave_IO_Running']=res[0].get('Slave_IO_Running')
		result['Seconds_Behind_Master']=res[0].get('Seconds_Behind_Master')
		result['Last_Error']=res[0].get('Last_Error')
		result['Last_Errno']=res[0].get('Last_Errno')
		result['Master_Host']=res[0].get('Master_Host')
		result['Master_Port']=res[0].get('Master_Port')

		return result
	def get_deadlock(self):
		result={}
		sql="SELECT R.TRX_ID WAITING_TRX_ID,R.TRX_MYSQL_THREAD_ID WAITING_THREAD,R.TRX_QUERY WAITING_QUERY,B.TRX_ID BLOCKING_TRX_ID,B.TRX_MYSQL_THREAD_ID BLOCKING_THREAD,B.TRX_QUERY BLOCKING_QUERY FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS W INNER JOIN INFORMATION_SCHEMA.INNODB_TRX B ON B.TRX_ID=W.BLOCKING_TRX_ID INNER JOIN INFORMATION_SCHEMA.INNODB_TRX R ON R.TRX_ID=W.REQUESTING_TRX_ID;"
		self.cur.execute(sql)
		res=self.cur.fetchall()
		result['Waiting_Trx_Id']=res[0].get('WAITING_TRX_ID')
		result['Waiting_Thread']=res[0].get('WAITING_THREAD')
		result['Waiting_Query']=res[0].get('WAITING_QUERY')
		result['Blocking_Trx_Id']=res[0].get('BLOCKING_TRX_ID')
		result['Blocking_Thread']=res[0].get('Blocking_THREAD')
		result['Blocking_Query']=res[0].get('Blocking_QUERY')
		return result

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

