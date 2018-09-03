import json
from json import JSONDecodeError
import os
import xlwt

from xlwt import Workbook
book = Workbook(encoding='utf-8')
sheet1 = book.add_sheet('school_recruit')

row_num = 0
text_file = open('school_recruit_res.txt', 'r', encoding='utf8')
line = text_file.readline()
json_file = json.loads(line.strip())
keys = list(json_file.keys())
print(keys)
while line:
    try:
        for i, f in enumerate(keys):
            sheet1.write(row_num, i, f)
            print('inserted ')
            print(row_num)
        row_num += 1
        line = text_file.readline()
        keys = list(json.loads(line.strip()).values())
        print(keys)
        print(row_num)

    except JSONDecodeError:
        print(" Decode Error !")
print(row_num)
text_file.close()
book.save('demo.xls')









