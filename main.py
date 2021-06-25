import sys
from PyQt5.QtWidgets import QApplication
from Auth import Authorization
from Reg import Registration


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Authorization()
    ex.connection()
    reg = Registration(ex.conn, ex.cur)
    ex.show()
    sys.exit(app.exec())