import hashlib
import sys
import uuid

import os
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtWidgets import QDateEdit, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PatReg import PatientReg
from Visit import Visit
from VisitOpen import VisitOpen

class Patient(QWidget):
    def __init__(self, cur, id, conn):
        super(QWidget, self).__init__()
        self.cur = cur
        self.id = id
        self.conn = conn
        self.setWindowTitle('Patient')
        #self.setWindowFlag(Qt.WindowStaysOnTopHint)
        print(str(self.id))
        self.setGeometry(300, 300, 1000, 700)
        self.cur.execute("select * from patient where patientid = %s", (str(self.id),))
        self.data = self.cur.fetchall()
        self.font = QFont()
        self.font.setPixelSize(20)
        self.info = QLabel(self)
        self.info.setText(
            'Full name: ' + str(self.data[0][0]) + ' ' + str(self.data[0][1]) + ' ' + str(self.data[0][2])
            + ' Sex: ' + str(self.data[0][5]) + '  DOB: ' + str(self.data[0][8]) + '  Policy №: ' + str(self.data[0][7]))
        self.info2 = QLabel(self)
        self.info2.setText('Address: ' + str(self.data[0][6]))
        self.info.move(5, 5)
        self.info2.move(5, 30)
        self.info.setFont(self.font)
        self.info2.setFont(self.font)
        self.frame = QFrame(self)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(3)
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setGeometry(0, 57, 1000, 3)
        self.addBut = QPushButton(self)
        self.addBut.setText('Add visit')
        self.addBut.setGeometry(5, 65, 170, 40)
        self.addBut.setFont(self.font)
        self.addBut.clicked.connect(self.add)
        self.vis = Visit(conn=self.conn, cur=self.cur, id=self.data[0][3])

        self.picbut = QPushButton(self)
        self.picbut.setText('Download files')
        self.picbut.setFont(self.font)
        self.picbut.setGeometry(430, 65, 170, 40)
        self.picbut.clicked.connect(self.download)

        self.updd = QPushButton(self)
        self.updd.setText('Update')
        self.updd.setFont(self.font)
        self.updd.setGeometry(825, 65, 170, 40)
        self.updd.clicked.connect(self.upd)

        self.grid = QTableWidget(self)
        self.grid.setGeometry(0, 110, 1000, 590)
        self.grid.setColumnCount(3)
        self.grid.verticalHeader().hide()
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.cellClicked.connect(self.openVis)
        for i in range(3):
            self.grid.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.upd()

    def openVis(self, row):
        idd = self.grid.item(row, 0).text()
        self.openVis = VisitOpen(conn=self.conn, cur=self.cur, id=str(idd), pid=str(self.data[0][3]))
        self.openVis.show()

    def add(self):
        self.vis.show()

    def download(self):
        self.cur.execute("select pathh from files where patientid = %s", (str(self.data[0][3]),))
        addr = self.cur.fetchall()
        for i in addr:
            print(i[0])
            os.system('eog -n ' + str(i[0]) +'&')

    def upd(self):
        self.grid.clear()
        self.grid.setRowCount(0)
        self.grid.setHorizontalHeaderLabels(['                                          ID                                         ',
                                             '                                         Date                                        ',
                                             '                                       Diagnosis                                     '])
        self.cur.execute("select fileid, ddate, diag from medfile where patientid = %s order by ddate", (self.data[0][3],))
        rows = self.cur.fetchall()
        i = 0
        for elem in rows:
            self.grid.setRowCount(self.grid.rowCount() + 1)
            j = 0
            for t in elem:
                self.grid.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1

