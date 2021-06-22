import hashlib
import sys
import uuid

import psycopg2
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtWidgets import QDateEdit, QFrame
from PyQt5.QtGui import QFont
from PatReg import PatientReg
from Patient import Patient

class Hospital(QWidget):
    def __init__(self, id, cur, conn):
        super(QWidget, self).__init__()
        self.id = id
        self.cur = cur
        self.conn = conn
        self.setStyleSheet('`/DB/f2.JPG')
        self.setWindowTitle('Hospital')
        self.setGeometry(0, 0, 1000, 700)
        self.cur.execute("select fname, sname, pname, dob, department from pd where doctorid = %s", (str(self.id),))
        q = self.cur.fetchone()
        fname = q[0]
        sname = q[1]
        pname = q[2]
        dob = q[3]
        department = q[4]
        self.font = QFont()
        self.font.setPixelSize(20)
        self.info = QLabel(self)
        self.info.setText('Full name: ' + sname + ' ' + fname + ' ' + pname)
        self.info2 = QLabel(self)
        self.info2.setText('DOB: ' + dob)
        self.info3 = QLabel(self)
        self.info3.setText('Department №: ' + department)
        #self.info.wordWrap()
        self.info.move(5, 5)
        self.info2.move(5, 35)
        self.info3.move(5, 65)
        self.info.setFont(self.font)
        self.info2.setFont(self.font)
        self.info3.setFont(self.font)
        # self.frame = QFrame(self)
        # self.frame.setLineWidth(3)
        # self.frame.setMidLineWidth(3)
        # self.frame.setFrameShape(QFrame.HLine)
        # self.frame.setFrameShadow(QFrame.Sunken)
        # self.frame.setGeometry(0, 30, 1000, 3)

        self.addBut = QPushButton(self)
        self.addBut.setText('Add new patient')
        self.addBut.setGeometry(500, 24, 170, 50)
        self.addBut.setFont(self.font)
        self.addBut.clicked.connect(self.add)
        self.regPatient = PatientReg(cur=self.cur, doctorid=self.id, conn=conn)

        self.updd = QPushButton(self)
        self.updd.setText('Update')
        self.updd.setGeometry(700, 24, 170, 50)
        self.updd.clicked.connect(self.upd)
        self.updd.setFont(self.font)
        #table
        self.grid = QTableWidget(self)
        self.grid.setGeometry(0, 96, 1000, 590)
        self.grid.setColumnCount(6)
        self.grid.setFont(self.font)
        self.grid.verticalHeader().hide()
        for i in range(6):
            self.grid.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.upd()
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.cellClicked.connect(self.openPat)

    def upd(self):
        self.grid.clear()
        self.grid.setRowCount(0)
        self.grid.setHorizontalHeaderLabels(['                 ID                 ',
                                             '              Last name             ',
                                             '              First name             ',
                                             '              Patronymic             ',
                                             '                 Sex                 ',
                                             '                 DOB                  '])
        self.cur.execute("select patientid, sname, fname, pname, sex, dob from patient where doctorid = %s order by sname", (str(self.id),))
        rows = self.cur.fetchall()
        i = 0
        for elem in rows:
            self.grid.setRowCount(self.grid.rowCount() + 1)
            j = 0
            for t in elem:
                self.grid.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
    def add(self):
        self.regPatient.show()


    def openPat(self, row):
        idd = self.grid.item(row, 0).text()
        self.patient = Patient(cur=self.cur, id=str(idd), conn=self.conn)
        self.patient.show()



