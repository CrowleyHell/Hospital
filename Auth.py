import hashlib
import sys
import uuid

import psycopg2
from PyQt5.QtWidgets import  QErrorMessage, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QDateEdit, QFrame
from PyQt5.QtGui import QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from Reg import Registration
from Hos import Hospital

def password(pw):
    hash = uuid.uuid4().hex
    return hashlib.sha256(hash.encode() + pw.encode()).hexdigest() + '-' + hash


def checkpw(hashpw, pw):
    password, hash = hashpw.split('-')
    return password == hashlib.sha256(hash.encode() + pw.encode()).hexdigest()


class Authorization(QWidget):
    def __init__(self):
        super(Authorization, self).__init__()
        self.setGeometry(100, 200, 1000, 700)
        self.setWindowTitle('Authorization')
        self.font = QFont()
        self.font.setPixelSize(20)


        self.log = QLineEdit(self)
        self.lText = QLabel(self)
        self.lText.setText('Login')
        self.lText.setFont(self.font)
        self.log.setFont(self.font)
        self.lText.setGeometry(250, 250, 100, 30)
        self.log.setGeometry(350, 250, 400, 30)


        self.pw = QLineEdit(self)
        self.pw.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.pText = QLabel(self)
        self.pText.setText('Password')
        self.pText.setFont(self.font)
        self.pw.setFont(self.font)
        self.pText.setGeometry(250, 290, 100, 30)
        self.pw.setGeometry(350, 290, 400, 30)


        self.enterBut = QPushButton(self)
        self.enterBut.setText('Sign in')
        self.enterBut.setFont(self.font)
        self.enterBut.setGeometry(373, 340, 150, 30)
        self.regBut = QPushButton(self)
        self.regBut.setGeometry(573, 340, 150, 30)
        self.regBut.setText('Sign up')
        self.regBut.setFont(self.font)
        self.enterBut.clicked.connect(self.enterance)
        self.regBut.clicked.connect(self.registration)



        self.show()
        self.conn, self.cur = self.connection()
        self.registrationWindow = Registration(conn=self.conn, cur=self.cur)


    def connection(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="devint56",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="postgres")
        self.cur = self.conn.cursor()
        return self.conn, self.cur


    def enterance(self):
        if self.log.text() == "" or self.pw.text() == "":
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Error")
            errMes.showMessage("Enter data")
            return
        self.cur.execute("select pw, ownerid from login where log = %s", (str(self.log.text()),))
        q = self.cur.fetchone()
        if q is None:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Error")
            errMes.showMessage("Wrong password or login")
            return
        pww = q[0]
        ownerid = q[1]
        if checkpw(pww, self.pw.text()):
            self.hos = Hospital(id=ownerid, cur=self.cur, conn=self.conn)
            self.hos.show()
            self.close()
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Error")
            errMes.showMessage("Wrong password or login")
            return
    def registration(self):
        self.registrationWindow.show()
