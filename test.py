# -*- coding: UTF-8 -*-    
# Author:yansh  
# FileName:test  
# DateTime:2021/5/8 10:58  
# SoftWare: PyCharm

import pandas as pd

text = pd.read_csv(r'./MML任务结果_外部关系05081_20210508_104314.txt', encoding='gb18030')
df1 = text(text[])




# 保存数据
# writer = pd.ExcelWriter(r'./mml解析')
# df.to_excel(excel_writer=writer, sheet_name='测试1')
# writer.save()
# writer.close()