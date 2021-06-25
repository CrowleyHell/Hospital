import hashlib
import uuid
from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtGui import QFont


def password(pw):
    hash = uuid.uuid4().hex
    return hashlib.sha256(hash.encode() + pw.encode()).hexdigest() + '-' + hash


def checkpw(hashpw, pw):
    password, hash = hashpw.split('-')
    return password == hashlib.sha256(hash.encode() + pw.encode()).hexdigest()


class Registration(QWidget):
    def __init__(self, conn, cur):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowTitle('Registration')
        self.font = QFont()
        self.font.setPixelSize(20)

        self.sname = QLineEdit(self)
        self.snameText = QLabel(self)
        self.snameText.setText("Second name")
        self.sname.setFont(self.font)
        self.snameText.setFont(self.font)
        self.snameText.setGeometry(270, 150, 150, 30)
        self.sname.setGeometry(420, 150, 400, 30)

        self.fname = QLineEdit(self)
        self.fnameText = QLabel(self)
        self.fnameText.setText("First name")
        self.fname.setFont(self.font)
        self.fnameText.setFont(self.font)
        self.fnameText.setGeometry(270, 190, 150, 30)
        self.fname.setGeometry(420, 190, 400, 30)

        self.pname = QLineEdit(self)
        self.pnameText = QLabel(self)
        self.pnameText.setText("Patronymic")
        self.pname.setFont(self.font)
        self.pnameText.setFont(self.font)
        self.pnameText.setGeometry(270, 230, 150, 30)
        self.pname.setGeometry(420, 230, 400, 30)

        self.log = QLineEdit(self)
        self.logText = QLabel(self)
        self.logText.setText("Login")
        self.log.setFont(self.font)
        self.logText.setFont(self.font)
        self.logText.setGeometry(270, 270, 150, 30)
        self.log.setGeometry(420, 270, 400, 30)

        self.pas = QLineEdit(self)
        self.pasText = QLabel(self)
        self.pasText.setText("Password")
        self.pas.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.pas.setFont(self.font)
        self.pasText.setFont(self.font)
        self.pasText.setGeometry(270, 310, 150, 30)
        self.pas.setGeometry(420, 310, 400, 30)

        self.dob = QDateEdit(self)
        self.dobText = QLabel(self)
        self.dobText.setText("Date of birth")
        self.dobText.setFont(self.font)
        self.dob.setFont(self.font)
        self.dobText.setGeometry(270, 350, 150, 30)
        self.dob.setGeometry(420, 350, 400, 30)

        self.dep = QLineEdit(self)
        self.depText = QLabel(self)
        self.depText.setText("Department")
        self.dep.setFont(self.font)
        self.depText.setFont(self.font)
        self.depText.setGeometry(270, 390, 150, 30)
        self.dep.setGeometry(420, 390, 400, 30)

        self.reg = QPushButton(self)
        self.reg.setText('Sign up')
        self.reg.setFont(self.font)
        self.reg.setGeometry(510, 430, 150, 30)
        self.reg.clicked.connect(self.add)

    def nameExists(self, sname, fname, pname, dob):
        self.cur.execute("select sname, fname, pname, dob from pd ")
        pd = self.cur.fetchall()
        j = 0
        for i in range(len(pd)):
            if sname == pd[i][0] and fname == pd[i][1] and pname == pd[i][2] and dob == pd[i][3]:
                j += 1
        if j >= 1:
            return True
        else:
            return False



    def logExists(self, login):
        self.cur.execute("select log from login")
        log = self.cur.fetchall()
        for i in range(len(log)):
            if login == log[i][0]:
                return True
            else:
                return False

    def add(self):
        if self.fname.text() != '' and self.sname.text() != '' \
                and self.dob.text() != '' and self.pas.text() != '' \
                and self.log.text() != '' and self.dep.text() != '':
            if str(self.fname.text()).isalpha() and str(self.sname.text()).isalpha() \
                    and str(self.pas.text()).isalnum() and str(self.log.text()).isalnum() \
                    and self.dep.text().isdigit():
                if len(self.log.text()) >= 6 and len(self.pas.text()) >= 6:
                    if not self.nameExists(self.sname.text(), self.fname.text(), self.pname.text(), self.dob.text()):
                        if not self.logExists(self.log.text()):
                            ppas = password(self.pas.text())
                            try:
                                self.cur.execute(
                                    "insert into pd (fname, sname, pname, dob, department) values (%s, %s, %s, %s, %s) returning doctorid",
                                    (str(self.fname.text()), str(self.sname.text()), str(self.pname.text()), str(self.dob.text()),
                                    self.dep.text()))
                                self.doctorid = self.cur.fetchone()[0]
                                self.cur.execute("insert into login(log, pw, ownerid) values (%s, %s, %s)",
                                                 (str(self.log.text()), str(ppas), self.doctorid))
                                self.conn.commit()
                                self.close()
                            except Exception as e:
                                print(e)
                                pass
                        else:
                            errMes = QErrorMessage(self)
                            errMes.setWindowTitle("Error")
                            errMes.showMessage("Such login exists")
                            return
                    else:
                        errMes = QErrorMessage(self)
                        errMes.setWindowTitle("Error")
                        errMes.showMessage("Such user exists")
                        return
                else:
                    errMes = QErrorMessage(self)
                    errMes.setWindowTitle("Error")
                    errMes.showMessage("Login and password must be at least 6 symbols")
                    return
            else:
                errMes = QErrorMessage(self)
                errMes.setWindowTitle("Error")
                errMes.showMessage("Wrong data")
                return
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Error")
            errMes.showMessage("Wrong data")
            return
