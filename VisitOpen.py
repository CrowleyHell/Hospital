import hashlib
import sys
import uuid

import psycopg2
from PyQt5.QtWidgets import QTextEdit, QTableWidgetItem, QErrorMessage, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtWidgets import QDateEdit, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
from PatReg import PatientReg
from PIL import Image

class VisitOpen(QWidget):
    def __init__(self, conn, cur, id, pid):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        self.id = id
        self.pid = pid
        self.setWindowTitle('Visits')
        self.setGeometry(300, 300, 1000, 700)
        self.cur.execute("select * from medfile where fileid = %s", (str(self.id),))
        self.data = self.cur.fetchall()
        self.font = QFont()
        self.font.setPixelSize(20)
        self.ddate = QLabel(self)
        print(self.data)
        self.ddate.setText('Date: ' + str(self.data[0][5]))
        self.ddate.setGeometry(10, 10, 400, 30)
        self.ddate.setFont(self.font)

        self.com = QTextEdit(self)
        self.com1 = QLabel(self)
        self.com1.setFont(self.font)
        self.com1.setText('Complaint: ')
        self.com1.setGeometry(10, 50, 200, 30)
        self.com.setFont(self.font)
        self.com.setText(self.data[0][4])
        self.com.setGeometry(230, 50, 600, 100)
        self.com.setReadOnly(True)

        self.diag = QTextEdit(self)
        self.diag.setFont(self.font)
        self.diag.setGeometry(230, 160, 600, 100)
        self.diag.setText(self.data[0][1])
        self.diag.setReadOnly(True)
        self.diag1 = QLabel(self)
        self.diag1.setFont(self.font)
        self.diag1.setText('Diagnosis: ')
        self.diag1.setGeometry(10, 160, 200, 30)

        self.pr = QTextEdit(self)
        self.pr.setGeometry(230, 270, 600, 100)
        self.pr.setText(self.data[0][3])
        self.pr.setFont(self.font)
        self.pr.setReadOnly(True)
        self.pr1 = QLabel(self)
        self.pr1.setFont(self.font)
        self.pr1.setText('Prescription: ')
        self.pr1.setGeometry(10, 270, 200, 30)

        self.ch = QTextEdit(self)
        self.ch.setGeometry(230, 380, 600, 100)
        self.ch.setText(self.data[0][2])
        self.ch.setFont(self.font)
        self.ch.setReadOnly(True)
        self.ch1 = QLabel(self)
        self.ch1.setFont(self.font)
        self.ch1.setText('Chronic disease: ')
        self.ch1.setGeometry(10, 380, 200, 30)

        self.picbut = QPushButton(self)
        self.picbut.setText('Download file')
        self.picbut.setGeometry(10, 490, 200, 30)
        self.picbut.clicked.connect(self.download)

    def download(self):
        self.cur.execute("select pathh from files where fileid = %s", (str(self.id),))
        addr = self.cur.fetchall()
        for i in addr:
            print(i[0])
            os.system('eog -n ' + str(i[0]) +'&')


