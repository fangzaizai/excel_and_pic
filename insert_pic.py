# -*-coding:utf-8-*-
import xlwt, xlrd
import sys, os
from xlutils.copy import copy
import xlsxwriter
from PIL import Image
from ftplib import FTP

path=os.getcwd()
def open_xls(file):
	try:
		data=xlrd.open_workbook(file,on_demand=True, formatting_info=True)
		return data
	except Exception,e:
		print str(e)
 #formatting
def data_byindex(file):
	data=open_xls(file)
	table=data.sheets()[0]
	#copydata:<class 'xlwt.Workbook.Workbook'>
	copydata=copy(data)
	#tmpdata:<class 'xlwt.Worksheet.Worksheet'>
	tmpdata=copydata.get_sheet(0)  
	#get row nums
	row_num=table.nrows    
	print row_num
	#get values
	cellM0=table.cell(4,12).value
	print cellM0
	tmpdata.col(12).width = 0x0d00 + 6500
	tmpdata.col(13).width = 0x0d00 + 6500
	for i in range(2,row_num):
		row_height=xlwt.easyxf('font:height 1800;')
		tmpdata.row(i).set_style(row_height)
	print table.col(3)[5]
	#return table
	copydata.save('2.xls')
	return table

def format_excel(file):
	data=open_xls(file)
	table=data.sheets()[0]
	#format1 = table.format()
	nrows=table.nrows
	ncols=table.ncols
	#print type(table)
	workbook = xlsxwriter.Workbook('3.xls')
	worksheet = workbook.add_worksheet()
	worksheet.set_column(12,13, 30)
	#worksheet.set_column(0,13, 80)
	ftp=ftp_open('192.168.5.199')
	for i in xrange(nrows):
		worksheet.set_row(i,150)
		for j in xrange(ncols):
			cell_value=table.cell_value(i,j)
			worksheet.write(i,j,cell_value)
			if (j == 12 and i >3):
				pic_path=ftp_get_image(ftp, i, 12, cell_value)
				resize(pic_path)
				worksheet.insert_image('M'+str(i), pic_path)
				print 'insert pic'
			elif (j==13 and i >3):
				pic_path=ftp_get_image(ftp, i, 13, cell_value)
				resize(pic_path)
				worksheet.insert_image('N'+str(i), pic_path)
				print 'insert another pic'			
	ftp_close(ftp)
	workbook.close()

def resize(pic_path):
	image=Image.open(pic_path)
	image_resized=image.resize((200,200),Image.ANTIALIAS)
	image_resized.save(pic_path)
	print 'resize pic'

def ftp_open(server):
	username='ubuntu'
	password='ubuntu'
	ftp=FTP()
	ftp.set_debuglevel(2)
	ftp.connect(server,21)
	ftp.login(username,password)
	return ftp

def ftp_close(ftp):
	ftp.quit()

def ftp_get_image(ftp, row, col, pic_path):
	pic_root_path='/home/ubuntu/FTP/'+ pic_path  #/LINDASceneAlarm/20171107/13/{1C59EA90-9963-4405-849B-200A66F39133}-20171107131802560.jpg'
	buffersize=1024
	local_pic=path+'/pic/'+str(row)+str(col)+'.jpg'
	fp=open(local_pic,'wb')
	ftp.retrbinary('RETR ' + pic_root_path, fp.write,buffersize)
	print 'get pic'
	ftp.set_debuglevel(0)
	fp.close()
	return local_pic

#def insert_pic(rows,pic):



if __name__ == '__main__':
	format_excel('1.xls')
	#ftp_get_image(12,3,'/LINDASceneAlarm/20171107/13/{1C59EA90-9963-4405-849B-200A66F39133}-20171107132929015.jpg')