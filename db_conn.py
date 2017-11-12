# -*-coding:utf-8 -*-
import psycopg2, os
import ConfigParser
import time,datetime
from ftplib import FTP

def ConParser():
	conf=ConfigParser.ConfigParser()
	conf.read('config.ini')
	para={}
	para['db_server']=conf.get('database','server')
	para['dbname']=conf.get('database','dbname')
	para['db_username']=conf.get('database','username')
	para['db_password']=conf.get('database','password')
	para['Starttime']=conf.get('interval','Starttime')
	para['Endtime']=conf.get('interval','Endtime')
	para['ftp_server']=conf.get('ftp','ftp_server')
	para['ftp_username']=conf.get('ftp','ftp_username')
	para['ftp_password']=conf.get('ftp','ftp_password')
	para['pic_root_path']=conf.get('ftp','pic_root_path')
	return para


paras=ConParser()
def db_conn():
	print paras['db_server']
	#print paras['Starttime']
	conn = psycopg2.connect(database=paras['dbname'], user=paras['db_username'], password=paras['db_password'], host=paras['db_server'], port='5432')
	return conn

def db_close(conn):
	conn.close()

def db_query(conn):
	#Start_time=datetime.datetime.strptime(paras['Starttime'],"%Y-%m-%d %H:%M:%S")
	#End_time=datetime.datetime.strptime(paras['Endtime'],"%Y-%m-%d %H:%M:%S")
	cur=conn.cursor()
	sql = 'SELECT\
	A.fr_alarmtime,\
	A.fr_alarm_cameraname,\
	A.fr_alarm_similarity,\
	A .person_name,\
	B.photo_path,\
	C.imagepath1 \
FROM ((face_recognize_alarm AS A \
INNER JOIN face_feature_info AS B \
ON A .person_id = B.person_id) \
INNER JOIN face_attri_result AS C \
on A.fr_alarm_id = C.recordid) \
where A.fr_alarmtime between '+paras['Starttime']+' and '+paras['Endtime']+ ' order by A.fr_alarmtime desc'
	print sql
	cur.execute(sql)
	result=cur.fetchall()
	#print result[0][0]
	return result

def ftp_open():
	ftp=FTP()
	ftp.set_debuglevel(2)
	ftp.connect(paras.ftp_server,21)
	ftp.login(paras.ftp_username,paras.ftp_password)
	return ftp

def ftp_close(ftp):
	ftp.quit()

def ftp_get_image(ftp, row, col, pic_path):
	pic_root_path=paras['pic_root_path']+ pic_path  #/LINDASceneAlarm/20171107/13/{1C59EA90-9963-4405-849B-200A66F39133}-20171107131802560.jpg'
	buffersize=1024
	local_pic=path+'\pic\\'+str(row)+str(col)+'.jpg'
	try:
		fp=open(local_pic,'wb')
		ftp.retrbinary('RETR ' + pic_root_path, fp.write,buffersize)
	except IOError as ioerr:
		print 'Error:%s' % (ioerr.errno)
	ftp.set_debuglevel(0)
	fp.close()
	return local_pic

if __name__ == '__main__':
	conn=db_conn()
	db_query(conn)
	db_close(conn)
