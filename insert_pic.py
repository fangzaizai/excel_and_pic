# -*-coding:utf-8-*-
import xlwt, xlrd
import sys
from xlutils.copy import copy
import xlsxwriter
from PIL import Image
from ftplib import FTP

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

def insert_pic(file):
	data=open_xls(file)
	table=data.sheets()[0]
	nrows=table.nrows
	ncols=table.ncols
	#print type(table)
	workbook = xlsxwriter.Workbook('3.xls')
	worksheet = workbook.add_worksheet()
	worksheet.set_column(12,13, 25)
	#worksheet.set_column(0,13, 80)
	for i in xrange(nrows):
		worksheet.set_row(i,150)
		for j in xrange(ncols):
			cell_value=table.cell_value(i,j)
			worksheet.write(i,j,cell_value)
	worksheet.insert_image('M6','2.jpg')
	worksheet.insert_image('N6','2.jpg')
	worksheet.insert_image('N5','2.jpg')

	workbook.close()

def resize():
	image=Image.open('1.jpg')
	image_resized=image.resize((200,200),Image.ANTIALIAS)
	image_resized.save('2.jpg')

def ftp_get_image():
	ftp_server='192.168.5.121'
	username='root'
	password='root'
	ftp=FTP()

	ftp.set_debuglevel(2)
	ftp.connect(ftp_server,21)
	ftp.login(username,password)

	pic_path='/home/ubuntu/FTP'+cell_value
	print ftp.gwtwelcome()
	buffersize=1024
	local_pic=cell_value
	fp=open(local_pic,'wb')
	ftp.retrbinary('RETR' + pic_path, fp.write,buffersize)
	ftp.set_debuglevel(0)
	fp.close()
	ftp.quit()
	





if __name__ == '__main__':
	insert_pic('1.xls')