from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtGui import QFont


class PatientReg(QWidget):
    def __init__(self, cur, doctorid, conn):
        super(QWidget, self).__init__()
        self.cur = cur
        self.conn = conn
        self.doctorid = doctorid
        self.setWindowTitle('Patient admision')
        self.setGeometry(0, 0, 1000, 700)
        self.font = QFont()
        self.font.setPixelSize(20)

        self.sname = QLineEdit(self)
        self.snameText = QLabel(self)
        self.snameText.setText("Second name")
        self.snameText.setFont(self.font)
        self.sname.setFont(self.font)
        self.snameText.setGeometry(270, 150, 150, 30)
        self.sname.setGeometry(420, 150, 400, 30)

        self.fname = QLineEdit(self)
        self.fnameText = QLabel(self)
        self.fnameText.setText("First name")
        self.fnameText.setFont(self.font)
        self.fname.setFont(self.font)
        self.fnameText.setGeometry(270, 190, 150, 30)
        self.fname.setGeometry(420, 190, 400, 30)

        self.pname = QLineEdit(self)
        self.pnameText = QLabel(self)
        self.pnameText.setText("Patronymic")
        self.pnameText.setFont(self.font)
        self.pname.setFont(self.font)
        self.pnameText.setGeometry(270, 230, 150, 30)
        self.pname.setGeometry(420, 230, 400, 30)

        self.dob = QDateEdit(self)
        self.dobText = QLabel(self)
        self.dobText.setText("Date of birth")
        self.dobText.setFont(self.font)
        self.dob.setFont(self.font)
        self.dobText.setGeometry(270, 270, 150, 30)
        self.dob.setGeometry(420, 270, 400, 30)

        self.sex = QLineEdit(self)
        self.sexText = QLabel(self)
        self.sexText.setText("Sex")
        self.sexText.setFont(self.font)
        self.sex.setFont(self.font)
        self.sexText.setGeometry(270, 310, 150, 30)
        self.sex.setGeometry(420, 310, 400, 30)

        self.pnum = QLineEdit(self)
        self.pnumText = QLabel(self)
        self.pnumText.setText("Phone number")
        self.pnumText.setFont(self.font)
        self.pnum.setFont(self.font)
        self.pnumText.setGeometry(270, 350, 150, 30)
        self.pnum.setGeometry(420, 350, 400, 30)

        self.adr = QLineEdit(self)
        self.adrText = QLabel(self)
        self.adrText.setText("Home address")
        self.adrText.setFont(self.font)
        self.adr.setFont(self.font)
        self.adrText.setGeometry(270, 390, 150, 30)
        self.adr.setGeometry(420, 390, 400, 30)

        self.pol = QLineEdit(self)
        self.polText = QLabel(self)
        self.polText.setText("Policy №")
        self.polText.setFont(self.font)
        self.pol.setFont(self.font)
        self.polText.setGeometry(270, 430, 150, 30)
        self.pol.setGeometry(420, 430, 400, 30)

        self.reg = QPushButton(self)
        self.reg.setText('Sign up')
        self.reg.setFont(self.font)
        self.reg.setGeometry(510, 470, 150, 30)
        self.reg.clicked.connect(self.add)

    def nameExists(self, sname, fname, pname, dob):
        self.cur.execute("select sname, fname, pname, dob from patient ")
        pd = self.cur.fetchall()
        j = 0
        for i in range(len(pd)):
            if str(sname) == pd[i][0] and str(fname) == pd[i][1] and str(pname) == pd[i][2] and str(dob) == pd[i][3]:
                j += 1
        if j >= 1:
            return True
        else:
            return False


    def add(self):
        if self.fname.text() != '' and self.sname.text() != '' \
                and self.dob.text() != '' and self.adr.text() != '' \
                and self.sex.text() != '' and self.pol.text() != '':
            if str(self.fname.text()).isalpha() and str(self.sname.text()).isalpha() \
                    and str(self.sex.text()).isalpha() and str(self.adr.text()).isascii() \
                    and self.pnum.text().isdigit() and self.pol.text().isdigit():
                if len(self.pol.text()) == 16 and len(self.pnum.text()) == 11:
                    if not self.nameExists(self.sname.text(), self.fname.text(), self.pname.text(), self.dob.text()):
                        try:
                            self.cur.execute("insert into patient (fname, sname, pname, dob, sex, doctorid, adr, pol) values (%s, %s, %s, %s, %s, %s, %s, %s) returning patientid",
                                             (str(self.fname.text()), str(self.sname.text()), str(self.pname.text()), str(self.dob.text()), str(self.sex.text()), self.doctorid,
                                              str(self.adr.text()), self.pol.text()))
                            self.patientid = self.cur.fetchone()[0]
                            self.conn.commit()
                            self.close()
                        except Exception as e:
                            print(e)
                            pass
                    else:
                        errMes = QErrorMessage(self)
                        errMes.setWindowTitle("Error")
                        errMes.showMessage("Such patient exists")
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
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Error")
            errMes.showMessage("Wrong data")
            return

