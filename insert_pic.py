# -*-coding:utf-8-*-
import xlwt, xlrd
import sys
from xlutils.copy import copy
import xlsxwriter
from PIL import Image

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
	worksheet.set_column(12,13, 40)
	#worksheet.set_column(0,13, 80)
	for i in xrange(nrows):
		worksheet.set_row(i,160)
		for j in xrange(ncol):
			cell_value=table.cell_value(i,j)
			worksheet.write(i,j,cell_value)
	worksheet.insert_image('M5','1.jpg')
	worksheet.insert_image('N5','1.jpg')
	workbook.close()



if __name__ == '__main__':
	insert_pic('1.xls')