import xlsxwriter
book = xlsxwriter.Workbook('pict.xlsx')
sheet = book.add_worksheet('demo')
print type(sheet)