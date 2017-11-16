# -*-coding:utf-8-*-
import xlwt, xlrd
import os
from xlutils.copy import copy
import xlsxwriter
from PIL import Image
from ftplib import FTP
import datetime
import db_conn
import sys
reload(sys)
sys.setdefaultencoding('utf8')

path=os.getcwd()
def open_xls(file):
	try:
		data=xlrd.open_workbook(file,on_demand=True, formatting_info=True)
		return data
	except Exception,e:
		print str(e)
 #formatting

def format_excel():
	paras=db_conn.ConParser()
	create_time=str(datetime.datetime.now()).replace('-','').replace(' ','_').replace(':','').split('.')[0]
	workbook = xlsxwriter.Workbook('Alarm'+create_time+'.xls')
	date_format = workbook.add_format({'num_format':'yyyy-mm-dd hh:mm:ss','align':'center','valign':'vcenter'})
	center_format = workbook.add_format({'align':'center','valign':'vcenter'})
	bold_center_format = workbook.add_format({'align':'center','valign':'vcenter','bold':'True','font_size':18})
	worksheet = workbook.add_worksheet()
	worksheet.set_column(0,5, 27)
	#connect db and close
	print 'start connect database'
	conn=db_conn.db_conn()
	print 'start query data'
	result=db_conn.db_query(conn)
	print 'start close database'
	db_conn.db_close(conn)

	ncols=len(result)
	print 'start connect ftp'
	ftp=db_conn.ftp_open()
	print 'ftp conn over'

	title=paras['db_server']+'  '+paras['Starttime']+'--'+paras['Endtime']
	worksheet.merge_range('A1:F1',title,bold_center_format)
	worksheet.set_row(0,75)
	worksheet.write(1,0,u'报警时间', center_format)
	worksheet.write(1,1,u'相机名称', center_format)
	worksheet.write(1,2,u'相似度', center_format)
	worksheet.write(1,3,u'姓名', center_format)
	worksheet.write(1,4,u'底库图片', center_format)
	worksheet.write(1,5,u'抓拍图片', center_format)
	worksheet.freeze_panes(2,0)

	for i in range(2, ncols+2):  #针对每一行，依次填充列值
		worksheet.set_row(i,150)
		for j in xrange(6):
			cell_value=result[i-2][j]
			if j == 4:
				pic_path=db_conn.ftp_get_image(ftp, i, 4, cell_value)
				resize(pic_path)
				worksheet.insert_image(i,j, pic_path)
			elif j==5:
				pic_path=db_conn.ftp_get_image(ftp, i, 5, cell_value)
				resize(pic_path)
				worksheet.insert_image(i,j, pic_path)
				print 'insert another pic'
			elif j == 0:
				worksheet.write(i,j,cell_value, date_format)
			else:
				worksheet.write(i,j,cell_value,center_format)		
	db_conn.ftp_close(ftp)
	workbook.close()

def resize(pic_path):
	image=Image.open(pic_path)
	image_resized=image.resize((200,200),Image.ANTIALIAS)
	image_resized.save(pic_path)
	print 'resize pic'


if __name__ == '__main__':
	format_excel()