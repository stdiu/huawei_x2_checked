# -*- coding: UTF-8 -*-    
# Author:yansh  
# FileName:main  
# DateTime:2021/5/7 9:52  
# SoftWare: PyCharm

# 注意ui和运行分离
import pandas
import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, QTimer
from PyQt5.uic import loadUi
import pandas as pd

class X2(QWidget):
    def __init__(self):
        super(X2, self).__init__()
        self.fextern = r'./data/外部小区.xlsx'
        self.fx2 = r'./data/x2.xlsx'
        self.initUI()

    def initUI(self):
        self.ui = loadUi(r'./huawei_x2.ui')

        self.ui.btn_extern.clicked.connect(self.OpenExtern)
        self.ui.btn_x2.clicked.connect(self.OpenX2)

        self.ui.btn_check.clicked.connect(self.Check)
        self.ui.btn_save.clicked.connect(self.Save)

        self.ui.progressBar.hide()

    def OpenExtern(self):
        self.fextern,_ = QFileDialog.getOpenFileName(
            self.ui,
            "选择外部文件为",
            r'./data/',
            '*.xlsx'
        )
        self.ui.lineEdit_extern.setText(self.fextern)

    def OpenX2(self):
        self.fx2, _ = QFileDialog.getOpenFileName(
            self.ui,
            "选择lte侧x2文件为",
            r'./data/',
            '*.xlsx'
        )
        self.ui.lineEdit_x2.setText(self.fx2)

    def Openfile(self):
        if self.fextern.strip() == "":
            self.flag = False
        elif self.fx2.strip() == "":
            self.flag = False
        else:
            self.flag = True
        if self.flag == False:
            QMessageBox.critical(
                self.ui,
                "错误",
                "没有打开需要文件"
            )

    def Check(self):
        try:
            self.Openfile() #检查是否打开文件
            self.mywork = workthread(self.ui, self.fextern, self.fx2)
            self.mywork.start()
            self.mywork.finishsignal.connect(self.workend)
        except:
            pass

    def Save(self):
        pass

    def workend(self,ins):

        if ins == 100:
            print('get=%d'%ins)
        elif ins == 20:
            QMessageBox.critical(self.ui, '文件错误', '请打开正确的外部文件')
        elif ins == 30:
            QMessageBox.critical(self.ui, '文件错误', '请打开正确的链路文件')



class workthread(QThread):
    finishsignal = QtCore.pyqtSignal(int)
    # 声明一个信号，同时返回一个int
    def __init__(self, ui, fextern, fx2):
        super(workthread, self).__init__()
        self.ui = ui
        self.fextern = fextern
        self.fx2 = fx2

    def run(self):
        print('子线程现在开始')
        try:
            df_extern = pd.read_excel(self.fextern, sheet_name='查询NR外部小区', usecols=['NAME', '移动网络码', '基站标识'])
        except:
            self.finishsignal.emit(20)
        try:
            df_x2 = pd.read_excel(self.fx2, sheet_name='查询X2接口链路', usecols={'NAME', '邻基站标识', '邻基站PLMN标识', 'X2接口状态信息'})
        except:
            self.finishsignal.emit(30)
        print('读取完成')
        df_extern = df_extern[(df_extern['移动网络码'].apply(str) =="11") | (df_extern['移动网络码'].apply(str) =="3")]
        # 默认格式为数字，要转换为字符类型
        df_extern['索引'] = df_extern['NAME'].apply(str) + '_'+ df_extern['基站标识'].apply(str)
        # 默认格式为字符，不需要转换为字符类型
        df_x2 = df_x2[(df_x2['邻基站PLMN标识'] == 'MCC:460 MNC:11') & (df_x2['X2接口状态信息'] == '正常')]
        df_x2['索引'] = df_x2['NAME'] + '_' + df_x2['邻基站标识'].apply(lambda x:x[6:])  # 记住这个切片用法

        # 冗余链路
        df_redundant = df_x2[~df_x2['索引'].isin(df_extern['索引'])]
        # 缺失链路
        df_lack = df_extern[~df_extern['索引'].isin(df_x2['索引'])]
        print('缺失链路')
        print(df_lack)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = X2()
    main.ui.show()
    sys.exit(app.exec_())