import hashlib
import sys
import uuid

import psycopg2
from PyQt5.QtWidgets import QPushButton, QFileDialog, QInputDialog, QWidget
from PyQt5.QtWidgets import QTextEdit, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtWidgets import QDateEdit, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDir

class Visit(QWidget):
    def __init__(self, conn, cur, id):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        self.id = id
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.font = QFont()
        self.font.setPixelSize(20)
        self.setWindowTitle('Visit')

        self.date = QDateEdit(self)
        self.dateText = QLabel(self)
        self.dateText.setText("Date of visit")
        self.date.setFont(self.font)
        self.dateText.setFont(self.font)
        self.dateText.setGeometry(70, 30, 150, 30)
        self.date.setGeometry(250, 30, 400, 30)

        self.com = QTextEdit(self)
        self.comText = QLabel(self)
        self.comText.setText("Complaint")
        self.com.setFont(self.font)
        self.comText.setFont(self.font)
        self.comText.setGeometry(70, 110, 150, 30)
        self.com.setGeometry(250, 80, 400, 100)

        self.ch = QTextEdit(self)
        self.chText = QLabel(self)
        self.chText.setText("Chronic diseases")
        self.ch.setFont(self.font)
        self.chText.setFont(self.font)
        self.chText.setGeometry(70, 230, 150, 30)
        self.ch.setGeometry(250, 200, 400, 100)

        self.diag = QTextEdit(self)
        self.diagText = QLabel(self)
        self.diagText.setText("Diagnosis")
        self.diag.setFont(self.font)
        self.diagText.setFont(self.font)
        self.diagText.setGeometry(70, 350, 100, 30)
        self.diag.setGeometry(250, 320, 400, 100)

        self.pr = QTextEdit(self)
        self.prText = QLabel(self)
        self.prText.setText("Prescription")
        self.pr.setFont(self.font)
        self.prText.setFont(self.font)
        self.prText.setGeometry(70, 470, 120, 30)
        self.pr.setGeometry(250, 440, 400, 100)

        self.addBut = QPushButton(self)
        self.addBut.setText('Add visit')
        self.addBut.setFont(self.font)
        self.addBut.setGeometry(500, 560, 150, 30)
        self.addBut.clicked.connect(self.add)

        self.picBut = QPushButton(self)
        self.picBut.setText('Upload file')
        self.picBut.setFont(self.font)
        self.picBut.setGeometry(250, 560, 150, 30)
        self.picBut.clicked.connect(self.upload)
        self.filenames = ''
        # self.cont = QTextEdit(self)
        # self.cont.setGeometry(800, 120, 50, 50)


    def upload(self):
        file = QFileDialog(self)
        file.setGeometry(850, 120, 150, 30)
        file.setFileMode(QFileDialog.ExistingFiles)
        file.setNameFilter("*.jpg")
        file.setDirectory(QDir.homePath())
        if file.exec_():
            self.filenames = file.selectedFiles()
        #print(self.filenames)
        for i in self.filenames:
            print(str(i))

    def add(self):
        if self.date.text() != '' and self.com.toPlainText() != '' \
                and self.ch.toPlainText() != '' and self.diag.toPlainText() != '' \
                and self.pr.toPlainText() != '':
            try:
                self.cur.execute("insert into medfile (diag, chronic, prescr, compl, ddate, patientid) "
                                 "values (%s, %s, %s, %s, %s, %s) returning fileid",
                                 (str(self.diag.toPlainText()), str(self.ch.toPlainText()), str(self.pr.toPlainText()), str(self.com.toPlainText()),
                                  str(self.date.text()), self.id))
                self.fileid = self.cur.fetchone()[0]
                for i in self.filenames:
                    self.cur.execute("insert into files (patientid, pathh, fileid) values (%s, %s, %s)", (self.id, str(i), str(self.fileid)))
                self.conn.commit()
                self.close()
            except Exception as e:
                print(e)
                pass

