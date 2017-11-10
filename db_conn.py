# -*-coding:utf-8 -*-
import psycopg2, os
import ConfigParser

def db_conn():
	conf=ConfigParser.ConfigParser()
	conf.read('config.ini')
	server=conf.get('database','server')
	dbname=conf.get('database','dbname')
	username=conf.get('database','username')
	password=conf.get('database','password')
	print server
	conn = psycopg2.connect(database=dbname, user=username, password=password, host=server, port='5432')
	return conn

def db_close(conn):
	conn.close()

def db_query(conn):
	cur=conn.cursor()
	sql='''SELECT
	A.fr_alarmtime, 
	A.fr_alarm_cameraname,
	A.fr_alarm_similarity,
	A .person_name,
	B.photo_path,
	C.imagepath1
FROM ((face_recognize_alarm AS A
INNER JOIN face_feature_info AS B
ON A .person_id = B.person_id)
INNER JOIN face_attri_result AS C
on A.fr_alarm_id = C.recordid)
where A.fr_alarmtime between '2017-11-10 16:55:00' and '2017-11-10 17:00:00'
'''
	cur.execute(sql)
	result=cur.fetchall()
	#file = open('1.txt','wb')
	#file.write(str(result))
	#file.close()
	print result[0][0]
	return result

if __name__ == '__main__':
	conn=db_conn()
	db_query(conn)
	db_close(conn)
